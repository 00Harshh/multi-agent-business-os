"""
Unified SQLAlchemy database layer.
SQLite by default (dev). Switch to PostgreSQL via DATABASE_URL env var.
"""
from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer, Float, JSON
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime, timezone
import uuid

from business_os.config.settings import settings


def utcnow():
    return datetime.now(timezone.utc)


engine = create_engine(settings.db_url, echo=False)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Lead(Base):
    __tablename__ = "leads"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company = Column(String)
    contact_name = Column(String)
    email = Column(String)
    linkedin_url = Column(String)
    icp_score = Column(Integer, default=0)    # 0–100
    status = Column(String, default="new")    # new | contacted | qualified | closed
    source = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)


class Employee(Base):
    __tablename__ = "employees"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String)
    role = Column(String)
    department = Column(String)
    slack_id = Column(String)
    status = Column(String, default="active")  # active | on_leave | offboarded
    created_at = Column(DateTime, default=utcnow)


class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    description = Column(Text)
    assignee_id = Column(String)               # FK -> Employee.id
    assigned_by = Column(String)
    priority = Column(String, default="medium")  # low | medium | high | critical
    status = Column(String, default="todo")    # todo | in_progress | blocked | done
    deadline = Column(DateTime)
    progress_pct = Column(Integer, default=0)
    last_update = Column(DateTime, nullable=True)
    last_update_notes = Column(Text, default="")
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)
class ProgressUpdate(Base):
    __tablename__ = "progress_updates"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String)
    employee_id = Column(String)
    update_text = Column(Text)
    progress_pct = Column(Integer)
    blockers = Column(Text)
    created_at = Column(DateTime, default=utcnow)


class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String)
    role_applied = Column(String)
    linkedin_url = Column(String)
    resume_text = Column(Text)
    fit_score = Column(Integer, default=0)
    stage = Column(String, default="sourced")  # sourced | screened | interview | offer | hired | rejected
    notes = Column(Text)
    created_at = Column(DateTime, default=utcnow)


class Report(Base):
    __tablename__ = "reports"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    report_type = Column(String)               # market | kpi | lead_summary | task_summary
    title = Column(String)
    content = Column(Text)
    metadata_json = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime, default=utcnow)


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    vendor = Column(String)
    amount = Column(Float)
    currency = Column(String, default="USD")
    category = Column(String, nullable=True)    # travel | saas | payroll | marketing | misc
    description = Column(Text)
    status = Column(String, default="uncategorized")  # uncategorized | categorized | approved
    date = Column(DateTime)
    created_at = Column(DateTime, default=utcnow)


class Customer(Base):
    __tablename__ = "customers"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company = Column(String)
    contact_name = Column(String)
    email = Column(String)
    plan = Column(String)                       # free | starter | pro | enterprise
    mrr = Column(Float, default=0.0)
    health_score = Column(Integer, default=100)
    last_activity = Column(DateTime, nullable=True)
    churn_risk = Column(String, default="low")  # low | medium | high | churned
    notes = Column(Text)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)


class AuditLog(Base):
    """Every agent action is written here — full traceability."""
    __tablename__ = "audit_log"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_name = Column(String)
    crew_name = Column(String)
    action = Column(String)
    entity_type = Column(String)
    entity_id = Column(String)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=utcnow)


def init_db():
    Base.metadata.create_all(engine)
    print("✅ Database initialized")


def get_session():
    return Session()
