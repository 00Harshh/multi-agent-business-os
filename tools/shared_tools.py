"""
Shared CrewAI tools available to all crews.
"""
import re
from urllib.parse import urlparse
from crewai.tools import tool
from business_os.storage.database import get_session, AuditLog, Task, Expense, Report, Customer, Lead, utcnow
from business_os.config.settings import settings
from datetime import datetime, timedelta
import requests

# ---------------------------------------------------------------------------
# Validation helpers — prevent agents from saving hallucinated data
# ---------------------------------------------------------------------------

def _looks_like_real_linkedin(url: str) -> bool:
    """Return True only if the URL is a plausible, non-fabricated LinkedIn URL."""
    if not url or url.lower() in ('', 'n/a', 'none', 'unknown', 'not found'):
        return False
    parsed = urlparse(url)
    if parsed.hostname not in ('www.linkedin.com', 'linkedin.com'):
        return False
    
    path = parsed.path.rstrip('/').lower()
    # Reject generic placeholders
    placeholders = ('yourname', 'your-name', 'placeholder', 'username', 'company-name', 'example')
    if any(p in path for p in placeholders):
        return False
        
    return True

def _looks_like_real_email(email: str) -> bool:
    """Return True only if the email is plausible and not obviously templated."""
    if not email or email.lower() in ('', 'n/a', 'none', 'unknown', 'not found'):
        return False
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return False
        
    local, domain = email.rsplit('@', 1)
    local_lower = local.lower()
    domain_lower = domain.lower()
    
    # Reject common placeholder domains and usernames
    placeholders = ('email', 'name', 'yourname', 'your-name', 'placeholder', 'example', 'domain', 'test')
    if any(p == local_lower or p in local_lower for p in placeholders):
        return False
    if any(p in domain_lower for p in ('example.com', 'email.com', 'domain.com', 'test.com')):
        return False
        
    return True


def _validate_url(url: str, expected_domain: str = None) -> bool:
    """Return the URL if it looks valid, or empty string if not."""
    if not url or url.lower() in ('', 'n/a', 'none', 'unknown', 'not found'):
        return ''
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.hostname:
        return ''
    if expected_domain and expected_domain not in parsed.hostname:
        return ''
    return url


def log_action(agent_name: str, crew_name: str, action: str,
               entity_type: str = "", entity_id: str = "", details: dict = {}):
    """Write every significant agent action to the immutable audit log."""
    db = get_session()
    entry = AuditLog(
        agent_name=agent_name, crew_name=crew_name, action=action,
        entity_type=entity_type, entity_id=entity_id, details=details,
    )
    db.add(entry)
    db.commit()
    db.close()


@tool("Web Search Tool")
def web_search(query: str) -> str:
    """Search the web for current information using Serper API."""
    if not settings.serper_api_key:
        return f"[MOCK] Web search results for: {query}"
    headers = {"X-API-KEY": settings.serper_api_key, "Content-Type": "application/json"}
    try:
        resp = requests.post("https://google.serper.dev/search",
                             json={"q": query, "num": 5}, headers=headers, timeout=10)
        results = resp.json().get("organic", [])
        return "\n\n".join(
            f"**{r['title']}**\n{r.get('snippet', '')}\n{r['link']}" for r in results[:5]
        )
    except Exception as e:
        return f"Search error: {e}"


@tool("Database Query Tool")
def db_query(sql: str) -> str:
    """Run a read-only SQL query against the business database."""
    from sqlalchemy import text
    db = get_session()
    try:
        result = db.execute(text(sql))
        rows = result.fetchall()
        if not rows:
            return "No results."
        headers = list(result.keys())
        lines = [" | ".join(headers)] + [" | ".join(str(v) for v in row) for row in rows[:50]]
        return "\n".join(lines)
    except Exception as e:
        return f"Query error: {e}"
    finally:
        db.close()


def send_slack_func(channel: str, message: str) -> str:
    """Send a message to a Slack channel or user ID."""
    if not settings.slack_token:
        return f"[MOCK] Slack -> {channel}: {message}"
    resp = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {settings.slack_token}"},
        json={"channel": channel, "text": message},
    )
    return "Sent ✓" if resp.json().get("ok") else f"Error: {resp.json().get('error')}"


@tool("Send Slack Message")
def send_slack(channel: str, message: str) -> str:
    """Send a message to a Slack channel or user ID."""
    return send_slack_func(channel, message)


@tool("Get All Tasks for Employee")
def get_employee_tasks(employee_id: str) -> str:
    """Retrieve all tasks assigned to a specific employee with progress."""
    db = get_session()
    tasks = db.query(Task).filter(Task.assignee_id == employee_id).all()
    db.close()
    if not tasks:
        return "No tasks found."
    return "\n".join(
        f"[{t.status.upper()}] {t.title} | {t.priority} | {t.progress_pct}% | "
        f"Deadline: {t.deadline} | Last: {t.last_update or 'none'}"
        for t in tasks
    )


@tool("Update Task Progress")
def update_task_progress(task_id: str, progress_pct: int, status: str, update_text: str) -> str:
    """Update a task's progress percentage, status, and latest note."""
    db = get_session()
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        db.close()
        return f"Task {task_id} not found."
    task.progress_pct = progress_pct
    task.status = status
    task.last_update = update_text
    db.commit()
    db.close()
    log_action("system", "task_mgmt", "update_progress", "task", task_id,
               {"progress": progress_pct, "status": status})
    return f"Task updated: {progress_pct}% | status={status}"


@tool("Save Expense")
def save_expense(vendor: str, amount: float, currency: str, category: str,
                 description: str, date_iso: str) -> str:
    """Create an expense record from an ISO 8601 date string."""
    db = get_session()
    expense = Expense(
        vendor=vendor,
        amount=amount,
        currency=currency or "USD",
        category=category,
        description=description,
        status="categorized" if category else "uncategorized",
        date=datetime.fromisoformat(date_iso),
    )
    db.add(expense)
    db.commit()
    expense_id = expense.id
    db.close()
    log_action("finance_agent", "finance", "save_expense", "expense", expense_id,
               {"vendor": vendor, "amount": amount, "currency": currency, "category": category})
    return f"Expense saved -> ID: {expense_id} | {vendor} | {amount} {currency}"


@tool("Get Expenses Summary")
def get_expenses_summary(days_back: int = 7) -> str:
    """Summarize expense totals by category for the requested lookback window."""
    db = get_session()
    start_date = utcnow() - timedelta(days=days_back)
    expenses = db.query(Expense).filter(Expense.date >= start_date).all()
    db.close()
    if not expenses:
        return f"No expenses found in the last {days_back} days."

    totals = {}
    grand_total = 0.0
    for expense in expenses:
        category = expense.category or "uncategorized"
        amount = float(expense.amount or 0.0)
        totals[category] = totals.get(category, 0.0) + amount
        grand_total += amount

    lines = [f"Expense summary for last {days_back} days:"]
    for category in sorted(totals):
        lines.append(f"- {category}: {totals[category]:.2f}")
    lines.append(f"Grand total: {grand_total:.2f}")
    return "\n".join(lines)


@tool("Save Report")
def save_report(report_type: str, title: str, content: str, metadata_dict: dict = {}) -> str:
    """Persist a report to the database."""
    db = get_session()
    report = Report(
        report_type=report_type,
        title=title,
        content=content,
        metadata_json=metadata_dict or {},
    )
    db.add(report)
    db.commit()
    report_id = report.id
    db.close()
    log_action("report_agent", report_type, "save_report", "report", report_id,
               {"title": title, "type": report_type})
    return f"Report saved -> ID: {report_id} | Type: {report_type}"


@tool("Update Customer Health")
def update_customer_health(customer_id: str, health_score: int, churn_risk: str) -> str:
    """Update a customer's health score and churn risk."""
    db = get_session()
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        db.close()
        return f"Customer {customer_id} not found."
    customer.health_score = max(0, min(100, health_score))
    customer.churn_risk = churn_risk
    db.commit()
    db.close()
    log_action("customer_success_agent", "customer_success", "update_health",
               "customer", customer_id, {"health_score": health_score, "churn_risk": churn_risk})
    return f"Customer {customer_id} updated -> health={health_score} risk={churn_risk}"


@tool("Get Business Context")
def get_business_context(include_leads: bool = True, include_market_reports: bool = True) -> str:
    """Return company ICP, existing leads, and recent market research as shared memory."""
    db = get_session()
    lines = [
        f"Company: {settings.company_name}",
        f"Ideal Customer Profile: {settings.icp_description}",
    ]

    if include_leads:
        leads = db.query(Lead).order_by(Lead.created_at.desc()).limit(25).all()
        lines.append("\nKnown leads and CRM memory:")
        if leads:
            for lead in leads:
                lines.append(
                    f"- {lead.company} | Contact: {lead.contact_name or 'unknown'} | "
                    f"Email: {lead.email or 'unknown'} | Score: {lead.icp_score} | "
                    f"Status: {lead.status} | Source: {lead.source or 'unknown'}"
                )
        else:
            lines.append("- No leads saved yet.")

    if include_market_reports:
        reports = db.query(Report).filter(
            Report.report_type.in_(["market", "market_research", "kpi_weekly"])
        ).order_by(Report.created_at.desc()).limit(5).all()
        lines.append("\nRecent market research memory:")
        if reports:
            for report in reports:
                preview = (report.content or "")[:500].replace("\n", " ")
                lines.append(f"- {report.title} ({report.report_type}): {preview}")
        else:
            lines.append("- No market research reports saved yet.")

    db.close()
    return "\n".join(lines)


@tool("Save Potential Client")
def save_potential_client(business_name: str, what_it_does: str, email: str,
                          contact_name: str, linkedin_url: str, crunchbase_url: str,
                          icp_score: int, cold_email: str) -> str:
    """Save a potential client lead with research notes and a custom cold email draft.
    IMPORTANT: Only provide email and linkedin_url values that you obtained from
    actual web search results. Do NOT fabricate or guess these values.
    If you don't have a verified email, pass 'not found'.
    If you don't have a verified LinkedIn URL, pass 'not found'.
    """
    # Validate LinkedIn URL — reject hallucinated patterns
    verified_linkedin = ''
    if _looks_like_real_linkedin(linkedin_url):
        verified_linkedin = linkedin_url

    # Validate email — reject hallucinated patterns
    verified_email = ''
    if _looks_like_real_email(email):
        verified_email = email

    # Validate Crunchbase URL
    verified_crunchbase = _validate_url(crunchbase_url, 'crunchbase.com')

    warnings = []
    if linkedin_url and not verified_linkedin:
        warnings.append(f"LinkedIn URL '{linkedin_url}' looks fabricated — not saved. Use web search to find the real URL.")
    if email and not verified_email:
        warnings.append(f"Email '{email}' looks fabricated — not saved. Use web search to find the real email.")

    db = get_session()
    try:
        lead = None
        if verified_email:
            lead = db.query(Lead).filter(Lead.email == verified_email).first()
        if not lead:
            lead = db.query(Lead).filter(Lead.company == business_name).first()

        notes = (
            f"What it does: {what_it_does}\n"
            f"Crunchbase URL: {verified_crunchbase or 'not verified'}\n"
            f"Custom cold email draft:\n{cold_email}"
        )
        if lead:
            lead.contact_name = contact_name or lead.contact_name
            lead.email = verified_email or lead.email
            lead.linkedin_url = verified_linkedin or lead.linkedin_url
            lead.icp_score = icp_score
            lead.source = "linkedin_crunchbase_research"
            lead.notes = notes
        else:
            lead = Lead(
                company=business_name,
                contact_name=contact_name,
                email=verified_email,
                linkedin_url=verified_linkedin,
                icp_score=icp_score,
                status="new",
                source="linkedin_crunchbase_research",
                notes=notes,
            )
            db.add(lead)

        db.commit()
        lead_id = lead.id
    finally:
        db.close()

    log_action("client_researcher", "lead_generation", "save_potential_client", "lead", lead_id,
               {"company": business_name, "score": icp_score, "email": verified_email})
    result = f"Potential client saved -> ID: {lead_id} | {business_name} | Score: {icp_score}/100"
    if warnings:
        result += "\n⚠️ " + "\n⚠️ ".join(warnings)
    return result
