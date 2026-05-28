"""
Development seed data for Business OS.
Run: python -m business_os.storage.seed
"""
from datetime import timedelta

from business_os.storage.database import (
    init_db,
    get_session,
    utcnow,
    Employee,
    Lead,
    Task,
    Customer,
    Expense,
)


def add_if_missing(db, model, lookup: dict, values: dict):
    existing = db.query(model).filter_by(**lookup).first()
    if existing:
        return existing
    record = model(**values)
    db.add(record)
    db.flush()
    return record


def seed_employees(db):
    employees = [
        ("Arjun Mehta", "arjun@company.com", "Backend Engineer", "Engineering", "U001", "active"),
        ("Priya Sharma", "priya@company.com", "Sales Rep", "Sales", "U002", "active"),
        ("Rohan Das", "rohan@company.com", "Designer", "Product", "U003", "active"),
        ("Ananya Singh", "ananya@company.com", "Marketing Manager", "Marketing", "U004", "active"),
        ("Vikram Nair", "vikram@company.com", "DevOps Engineer", "Engineering", "U005", "active"),
    ]
    records = {}
    for name, email, role, department, slack_id, status in employees:
        records[email] = add_if_missing(db, Employee, {"email": email}, {
            "name": name,
            "email": email,
            "role": role,
            "department": department,
            "slack_id": slack_id,
            "status": status,
        })
    return records


def seed_leads(db):
    """Seed demo leads. Emails and LinkedIn URLs are left empty because
    they were previously fabricated placeholders (e.g. 'firstname@company.com',
    'linkedin.com/in/firstname-lastname'). Real data should be populated by
    the lead generation agent using actual web search results."""
    leads = [
        ("Northstar Analytics", "Maya Rao", 20, "new"),
        ("FinPilot Labs", "Kabir Malhotra", 35, "new"),
        ("CloudLedger", "Sara Kapoor", 45, "new"),
        ("OpsHive", "Neel Iyer", 55, "new"),
        ("BrightCart", "Tara Shah", 60, "contacted"),
        ("MetricFlow AI", "Dev Menon", 65, "contacted"),
        ("ScaleStack", "Isha Verma", 72, "qualified"),
        ("RevenueLoop", "Aditya Bose", 78, "qualified"),
        ("PulseDesk", "Meera Nair", 85, "qualified"),
        ("NovaOps", "Rahul Sethi", 91, "closed"),
    ]
    for company, contact_name, icp_score, status in leads:
        add_if_missing(db, Lead, {"company": company}, {
            "company": company,
            "contact_name": contact_name,
            "email": "",
            "linkedin_url": "",
            "icp_score": icp_score,
            "status": status,
            "source": "seed",
            "notes": f"Seed lead for {company} — email and LinkedIn need verification via web search",
        })


def seed_tasks(db, employees):
    now = utcnow()
    task_rows = [
        ("Build auth service", "Implement API authentication middleware.", employees["arjun@company.com"].id,
         "high", "todo", now + timedelta(days=5), 0),
        ("Optimize database indexes", "Review slow queries and add indexes.", employees["arjun@company.com"].id,
         "high", "todo", now + timedelta(days=4), 0),
        ("Follow up qualified leads", "Contact qualified leads with the new pitch.", employees["priya@company.com"].id,
         "medium", "in_progress", now + timedelta(days=3), 45),
        ("Prepare sales pipeline notes", "Update CRM notes for active opportunities.", employees["priya@company.com"].id,
         "medium", "in_progress", now + timedelta(days=2), 55),
        ("Refresh dashboard UI", "Polish the analytics dashboard layout.", employees["rohan@company.com"].id,
         "low", "done", now - timedelta(days=1), 100),
        ("Export design tokens", "Publish updated tokens for engineering.", employees["rohan@company.com"].id,
         "low", "done", now - timedelta(days=1), 100),
        ("Fix production alerting", "Resolve missing alerts for payment failures.", employees["vikram@company.com"].id,
         "critical", "in_progress", now - timedelta(days=2), 35),
        ("Patch deployment pipeline", "Fix flaky deployment step for backend services.", employees["vikram@company.com"].id,
         "critical", "in_progress", now - timedelta(days=2), 40),
    ]
    for title, description, assignee_id, priority, status, deadline, progress_pct in task_rows:
        add_if_missing(db, Task, {"title": title}, {
            "title": title,
            "description": description,
            "assignee_id": assignee_id,
            "assigned_by": "seed",
            "priority": priority,
            "status": status,
            "deadline": deadline,
            "progress_pct": progress_pct,
            "last_update": "Seeded task",
            "tags": ["seed"],
        })


def seed_customers(db):
    now = utcnow()
    customers = [
        ("TechFlow Inc", "Nisha Patel", "nisha@techflow.com", "pro", 450, 85, "low", now - timedelta(days=3)),
        ("BuildRight Co", "Harsh Jain", "harsh@buildright.com", "starter", 120, 58, "medium", now - timedelta(days=18)),
        ("DataNest Ltd", "Aarav Kulkarni", "aarav@datanest.com", "enterprise", 1200, 28, "high", now - timedelta(days=45)),
        ("Omega Systems", "Leela Thomas", "leela@omegasystems.com", "free", 0, 10, "churned", now - timedelta(days=90)),
    ]
    for company, contact_name, email, plan, mrr, health_score, churn_risk, last_activity in customers:
        add_if_missing(db, Customer, {"company": company}, {
            "company": company,
            "contact_name": contact_name,
            "email": email,
            "plan": plan,
            "mrr": mrr,
            "health_score": health_score,
            "churn_risk": churn_risk,
            "last_activity": last_activity,
            "notes": f"Seed customer for {company}",
        })


def seed_expenses(db):
    now = utcnow()
    expenses = [
        ("AWS", 340.00, "USD", "saas", "Cloud infrastructure", "categorized", now - timedelta(days=5)),
        ("Uber", 85.50, "USD", None, "Airport ride for sales meeting", "uncategorized", now - timedelta(days=3)),
        ("Unknown Vendor XYZ", 1200.00, "USD", None, "Unclassified business charge", "uncategorized", now - timedelta(days=1)),
    ]
    for vendor, amount, currency, category, description, status, date in expenses:
        existing = db.query(Expense).filter(
            Expense.vendor == vendor,
            Expense.amount == amount,
        ).first()
        if existing:
            continue
        db.add(Expense(
            vendor=vendor,
            amount=amount,
            currency=currency,
            category=category,
            description=description,
            status=status,
            date=date,
        ))


def main():
    init_db()
    db = get_session()
    try:
        employees = seed_employees(db)
        seed_leads(db)
        seed_tasks(db, employees)
        seed_customers(db)
        seed_expenses(db)
        db.commit()
    finally:
        db.close()
    print("Seeded: 5 employees, 10 leads, 8 tasks, 4 customers, 3 expenses")


if __name__ == "__main__":
    main()
