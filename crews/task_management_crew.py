from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

from business_os.tools.shared_tools import db_query, send_slack, get_employee_tasks, log_action
from business_os.storage.database import get_session, Task as TaskModel, Employee, ProgressUpdate
from business_os.config.settings import settings
from datetime import datetime, timezone


@tool("Assign Task to Employee")
def assign_task(title: str, description: str, employee_id: str,
                priority: str, deadline_iso: str) -> str:
    """Create and assign a new task to an employee. deadline_iso = ISO 8601 string."""
    db = get_session()
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        db.close()
        return f"Employee {employee_id} not found."
    task = TaskModel(
        title=title, description=description, assignee_id=employee_id,
        assigned_by="task_mgmt_crew", priority=priority,
        deadline=datetime.fromisoformat(deadline_iso),
    )
    db.add(task)
    db.commit()
    task_id = task.id
    db.close()
    log_action("assigner", "task_management", "assign_task", "task", task_id,
               {"title": title, "employee": employee_id, "priority": priority})
    return f"Task '{title}' assigned to {emp.name} -> ID: {task_id}"


@tool("Log Employee Progress Update")
def log_progress(task_id: str, employee_id: str, update_text: str,
                 progress_pct: int, blockers: str = "") -> str:
    """Record a progress update from an employee on a task."""
    db = get_session()
    update = ProgressUpdate(
        task_id=task_id, employee_id=employee_id,
        update_text=update_text, progress_pct=progress_pct, blockers=blockers,
    )
    db.add(update)
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task:
        task.progress_pct = progress_pct
        task.last_update = update_text
        if progress_pct >= 100:
            task.status = "done"
        elif blockers:
            task.status = "blocked"
    db.commit()
    db.close()
    return f"Progress logged: {progress_pct}% | Blockers: {blockers or 'none'}"


@tool("Get Overdue Tasks")
def get_overdue_tasks() -> str:
    """List all tasks that are past their deadline and not yet completed."""
    db = get_session()
    now = datetime.now(timezone.utc)
    overdue = db.query(TaskModel).filter(
        TaskModel.deadline < now,
        TaskModel.status != "done",
    ).all()
    db.close()
    if not overdue:
        return "No overdue tasks."
    return "\n".join(
        f"[{t.id[:8]}] {t.title} | Assignee: {t.assignee_id} | "
        f"Deadline: {t.deadline} | Progress: {t.progress_pct}%"
        for t in overdue
    )


def build_task_management_crew() -> Crew:
    llm = settings.build_llm()
    assigner = Agent(
        role="Task Assigner",
        goal="Assign unassigned tasks to the right employees based on their role and workload",
        backstory="Experienced project manager who matches work to the right people at the right time.",
        tools=[assign_task, db_query],
        llm=llm,
        verbose=True,
    )
    tracker = Agent(
        role="Progress Tracker",
        goal="Monitor all active tasks and surface any that are falling behind",
        backstory="Operations analyst who keeps a precise eye on every task in the system.",
        tools=[get_employee_tasks, get_overdue_tasks, db_query],
        llm=llm,
        verbose=True,
    )
    escalator = Agent(
        role="Escalation Agent",
        goal="Identify blocked or overdue tasks and notify the right people via Slack",
        backstory="Risk manager who ensures no task falls through the cracks without human awareness.",
        tools=[get_overdue_tasks, send_slack, log_progress],
        llm=llm,
        verbose=True,
    )

    return Crew(
        agents=[assigner, tracker, escalator],
        process=Process.sequential,
        verbose=True,
        tasks=[
            Task(
                description=(
                    "Query the database for tasks with status='todo' and no assignee, "
                    "especially those marked high or critical priority. Assign them to "
                    "employees whose role matches the task requirements."
                ),
                expected_output="List of tasks assigned, including employee name and deadline",
                agent=assigner,
            ),
            Task(
                description=(
                    "Review all tasks with status='in_progress'. Calculate how much of the "
                    "deadline has elapsed vs. the progress percentage. Flag any task where "
                    "progress_pct < (time_elapsed_pct - 20)."
                ),
                expected_output="Progress health report listing at-risk tasks",
                agent=tracker,
            ),
            Task(
                description=(
                    "For all overdue tasks and blocked tasks, send a Slack alert to the assignee "
                    "with: task name, deadline, current progress, and a request for an update."
                ),
                expected_output="List of Slack notifications sent",
                agent=escalator,
            ),
        ],
    )
