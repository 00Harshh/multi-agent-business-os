from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

from business_os.tools.shared_tools import db_query, save_expense, get_expenses_summary, save_report, log_action
from business_os.storage.database import get_session, Expense
from business_os.config.settings import settings


@tool("Categorize Expense")
def categorize_expense(expense_id: str, category: str, description: str) -> str:
    """Update an existing expense category, status, and description."""
    db = get_session()
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        db.close()
        return f"Expense {expense_id} not found."
    expense.category = category
    expense.status = "categorized"
    expense.description = description
    db.commit()
    db.close()
    log_action("finance_agent", "finance", "categorize_expense", "expense", expense_id,
               {"category": category})
    return f"Expense categorized -> ID: {expense_id} | Category: {category}"


def build_finance_crew(period_days: int = 7) -> Crew:
    llm = settings.build_llm()
    expense_tracker = Agent(
        role="Expense Tracker",
        goal="Categorize all uncategorized expenses and flag any that exceed category thresholds",
        backstory="A meticulous finance analyst who keeps every transaction clean and categorized.",
        tools=[db_query, save_expense, get_expenses_summary, categorize_expense],
        llm=llm,
        verbose=True,
    )
    invoice_generator = Agent(
        role="Invoice Generator",
        goal="Generate invoice drafts for all qualified leads and save them as reports",
        backstory="An experienced billing specialist who creates professional, accurate invoices.",
        tools=[db_query, save_report],
        llm=llm,
        verbose=True,
    )
    kpi_builder = Agent(
        role="KPI Dashboard Builder",
        goal="Compute weekly business KPIs and save a dashboard report",
        backstory="A data analyst who transforms raw database metrics into actionable business intelligence.",
        tools=[db_query, get_expenses_summary, save_report],
        llm=llm,
        verbose=True,
    )

    return Crew(
        agents=[expense_tracker, invoice_generator, kpi_builder],
        process=Process.sequential,
        verbose=True,
        tasks=[
            Task(
                description=(
                    "Query all expenses with status='uncategorized'. For each one, use the vendor "
                    "name and description to determine the correct category: travel, saas, payroll, "
                    "marketing, or misc. Update the existing expense with Categorize Expense, setting "
                    "status='categorized'. If a single expense is above $5000, append a clear flag note "
                    "to its description. Return a summary of how many were categorized and any flagged items."
                ),
                expected_output="Summary with count categorized and any flagged expense IDs",
                agent=expense_tracker,
            ),
            Task(
                description=(
                    "Query all leads where status='qualified'. For each lead, generate a professional "
                    "invoice as plain text including: invoice number (INV-{lead_id[:8]}), company name, "
                    "contact name, line items (consulting services, platform access fee), subtotal, "
                    "tax at 18%, total, and due date 30 days from today. Save each invoice as a Report "
                    "with report_type='invoice' and title='Invoice for {company}'. Return count of invoices generated."
                ),
                expected_output="Count of invoices generated and saved",
                agent=invoice_generator,
            ),
            Task(
                description=(
                    f"Query the database to compute these KPIs for the past {period_days} days: "
                    "total new leads added and their average ICP score; number of tasks completed vs "
                    "number of tasks overdue; total candidates in pipeline by stage; weekly burn rate "
                    "from expenses; and number of active employees. Format all of this into a clean "
                    "plain-text KPI report. Save it as a Report with report_type='kpi_weekly' and "
                    "title='Weekly KPI Report - {today date}'. Return the full report text."
                ),
                expected_output="Full plain-text weekly KPI report",
                agent=kpi_builder,
            ),
        ],
    )
