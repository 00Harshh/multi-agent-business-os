from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

from business_os.tools.shared_tools import send_slack, db_query, log_action, send_slack_func
from business_os.storage.database import get_session, Employee, Task as TaskModel
from business_os.config.settings import settings


@tool("Send Daily Standup Request")
def send_standup_request(employee_slack_id: str, employee_name: str) -> str:
    """Send a standup prompt to an employee via Slack."""
    message = (
        f"Good morning {employee_name}! Time for your daily standup.\n\n"
        f"Please share:\n"
        f"1. What did you complete yesterday?\n"
        f"2. What are you working on today?\n"
        f"3. Any blockers or help needed?\n\n"
        f"Reply here or update your tasks in the dashboard."
    )
    return send_slack_func(employee_slack_id, message)


@tool("Get All Active Employees")
def get_active_employees() -> str:
    """Return all active employees with their IDs, names, roles, and Slack IDs."""
    db = get_session()
    employees = db.query(Employee).filter(Employee.status == "active").all()
    db.close()
    if not employees:
        return "No active employees found."
    return "\n".join(
        f"ID: {e.id} | {e.name} | {e.role} | {e.department} | Slack: {e.slack_id or 'N/A'}"
        for e in employees
    )


@tool("Generate Employee Task Report")
def employee_task_report(employee_id: str) -> str:
    """Generate a full task and progress summary for one employee."""
    db = get_session()
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    tasks = db.query(TaskModel).filter(TaskModel.assignee_id == employee_id).all()
    db.close()
    if not emp:
        return "Employee not found."
    lines = [f"=== {emp.name} ({emp.role} / {emp.department}) ==="]
    if not tasks:
        lines.append("No tasks assigned.")
    for t in tasks:
        lines.append(
            f"\n  [{t.status.upper()}] {t.title}\n"
            f"  Priority: {t.priority} | Progress: {t.progress_pct}%\n"
            f"  Deadline: {t.deadline}\n"
            f"  Last update: {t.last_update or 'No update yet'}"
        )
    return "\n".join(lines)


def build_employee_ops_crew() -> Crew:
    llm = settings.build_llm()
    checkin_agent = Agent(
        role="Employee Check-in Bot",
        goal="Send daily standup prompts to all active employees",
        backstory="Friendly HR bot that keeps the team communicating and aligned.",
        tools=[get_active_employees, send_standup_request],
        llm=llm,
        verbose=True,
    )
    logger = Agent(
        role="Progress Logger",
        goal="Compile task reports for every employee and identify those with stale updates",
        backstory="Meticulous record keeper who ensures every progress signal is captured.",
        tools=[db_query, employee_task_report],
        llm=llm,
        verbose=True,
    )
    hr_bot = Agent(
        role="HR Operations Bot",
        goal="Proactively flag overloaded employees and those showing disengagement signals",
        backstory="Empathetic HR analyst who watches for burnout and productivity risks.",
        tools=[get_active_employees, employee_task_report, send_slack, db_query],
        llm=llm,
        verbose=True,
    )

    return Crew(
        agents=[checkin_agent, logger, hr_bot],
        process=Process.sequential,
        verbose=True,
        tasks=[
            Task(
                description="Get all active employees and send each a daily standup request via Slack.",
                expected_output="Confirmation that standup messages were sent to all active employees",
                agent=checkin_agent,
            ),
            Task(
                description=(
                    "Generate task reports for all employees. Identify who has not submitted "
                    "any progress update in the last 48 hours. List them by name and task count."
                ),
                expected_output="List of employees with stale updates, sorted by days since last update",
                agent=logger,
            ),
            Task(
                description=(
                    "For any employee with 5 or more in-progress tasks and no update in 48+ hours, "
                    "send a caring follow-up Slack message checking in on them. "
                    "Also flag any employee with 0 tasks assigned as potentially under-utilized."
                ),
                expected_output="Follow-up messages sent. Summary of at-risk and under-utilized employees.",
                agent=hr_bot,
            ),
        ],
    )
