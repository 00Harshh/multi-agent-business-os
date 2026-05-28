"""
Optional FastAPI REST layer for Business OS.
Run: uvicorn business_os.api:app --reload
Docs: http://localhost:8000/docs
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from business_os.orchestrator import run_crew, CREW_REGISTRY
from business_os.storage.database import (
    init_db, get_session, Lead, Task, Employee, Candidate, AuditLog, Expense, Customer, Report
)

app = FastAPI(title="Business OS API", version="1.0.0")


@app.on_event("startup")
def startup():
    init_db()


class CrewRequest(BaseModel):
    crew_name: str
    params: Optional[dict] = {}


@app.get("/")
def root():
    return {"service": "Business OS", "status": "running", "crews": list(CREW_REGISTRY.keys())}


@app.get("/crews")
def list_crews():
    return {k: {"description": v["description"], "params": v["params"]}
            for k, v in CREW_REGISTRY.items()}


@app.post("/run")
def run(req: CrewRequest):
    if req.crew_name not in CREW_REGISTRY:
        raise HTTPException(404, detail=f"Crew '{req.crew_name}' not found")
    result = run_crew(req.crew_name, **(req.params or {}))
    return {"crew": req.crew_name, "result": result}


@app.get("/leads")
def get_leads(status: Optional[str] = None, min_score: int = 0, limit: int = 20):
    db = get_session()
    q = db.query(Lead).filter(Lead.icp_score >= min_score)
    if status:
        q = q.filter(Lead.status == status)
    leads = q.order_by(Lead.icp_score.desc()).limit(limit).all()
    db.close()
    return [{"id": l.id, "company": l.company, "contact": l.contact_name,
             "email": l.email, "score": l.icp_score, "status": l.status} for l in leads]


@app.get("/tasks")
def get_tasks(status: Optional[str] = None, assignee_id: Optional[str] = None, limit: int = 50):
    db = get_session()
    q = db.query(Task)
    if status:
        q = q.filter(Task.status == status)
    if assignee_id:
        q = q.filter(Task.assignee_id == assignee_id)
    tasks = q.order_by(Task.priority.desc(), Task.deadline).limit(limit).all()
    db.close()
    return [{"id": t.id, "title": t.title, "assignee": t.assignee_id, "status": t.status,
             "priority": t.priority, "progress": t.progress_pct,
             "deadline": str(t.deadline), "last_update": t.last_update} for t in tasks]


@app.get("/employees")
def get_employees():
    db = get_session()
    employees = db.query(Employee).filter(Employee.status == "active").all()
    db.close()
    return [{"id": e.id, "name": e.name, "role": e.role,
             "department": e.department, "slack_id": e.slack_id} for e in employees]


@app.get("/candidates")
def get_candidates(role: Optional[str] = None, min_score: int = 0):
    db = get_session()
    q = db.query(Candidate).filter(Candidate.fit_score >= min_score)
    if role:
        q = q.filter(Candidate.role_applied == role)
    candidates = q.order_by(Candidate.fit_score.desc()).all()
    db.close()
    return [{"id": c.id, "name": c.name, "role": c.role_applied,
             "score": c.fit_score, "stage": c.stage, "linkedin": c.linkedin_url} for c in candidates]


@app.get("/audit-log")
def get_audit_log(crew: Optional[str] = None, limit: int = 100):
    db = get_session()
    q = db.query(AuditLog)
    if crew:
        q = q.filter(AuditLog.crew_name == crew)
    logs = q.order_by(AuditLog.created_at.desc()).limit(limit).all()
    db.close()
    return [{"agent": l.agent_name, "crew": l.crew_name, "action": l.action,
             "entity": l.entity_type, "id": l.entity_id,
             "details": l.details, "at": str(l.created_at)} for l in logs]


@app.get("/expenses")
def get_expenses(category: Optional[str] = None, status: Optional[str] = None, limit: int = 50):
    db = get_session()
    q = db.query(Expense)
    if category:
        q = q.filter(Expense.category == category)
    if status:
        q = q.filter(Expense.status == status)
    expenses = q.order_by(Expense.date.desc()).limit(limit).all()
    db.close()
    return [{"id": e.id, "vendor": e.vendor, "amount": e.amount, "currency": e.currency,
             "category": e.category, "status": e.status, "date": str(e.date),
             "description": e.description} for e in expenses]


@app.get("/customers")
def get_customers(churn_risk: Optional[str] = None, min_mrr: float = 0, limit: int = 50):
    db = get_session()
    q = db.query(Customer).filter(Customer.mrr >= min_mrr)
    if churn_risk:
        q = q.filter(Customer.churn_risk == churn_risk)
    customers = q.order_by(Customer.health_score.asc()).limit(limit).all()
    db.close()
    return [{"id": c.id, "company": c.company, "contact_name": c.contact_name,
             "email": c.email, "plan": c.plan, "mrr": c.mrr,
             "health_score": c.health_score, "churn_risk": c.churn_risk,
             "last_activity": str(c.last_activity)} for c in customers]


@app.get("/reports")
def get_reports(report_type: Optional[str] = None, limit: int = 20):
    db = get_session()
    q = db.query(Report)
    if report_type:
        q = q.filter(Report.report_type == report_type)
    reports = q.order_by(Report.created_at.desc()).limit(limit).all()
    db.close()
    rows = []
    for report in reports:
        content = report.content or ""
        if len(content) > 300:
            content = content[:300] + "..."
        rows.append({
            "id": report.id,
            "report_type": report.report_type,
            "title": report.title,
            "created_at": str(report.created_at),
            "content": content,
        })
    return rows
