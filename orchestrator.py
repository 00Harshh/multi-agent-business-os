"""
Master Orchestrator — central entry point for all Business OS crews.
Trigger via: CLI, REST API (api.py), or cron scheduler.
"""
from business_os.storage.database import init_db
from business_os.crews.lead_generation_crew import build_lead_gen_crew
from business_os.crews.task_management_crew import build_task_management_crew
from business_os.crews.employee_ops_crew import build_employee_ops_crew
from business_os.crews.market_research_crew import build_market_research_crew
from business_os.crews.recruitment_crew import build_recruitment_crew
from business_os.crews.finance_crew import build_finance_crew
from business_os.crews.customer_success_crew import build_customer_success_crew

CREW_REGISTRY = {
    "lead_gen": {
        "description": "Generate leads, find potential clients, and draft custom cold outreach",
        "params": "target_industry (str), num_leads (int, default 10)",
        "builder": build_lead_gen_crew,
    },
    "market_research": {
        "description": "Research a market topic, track competitors and trends",
        "params": "topic (str)",
        "builder": build_market_research_crew,
    },
    "recruitment": {
        "description": "Write JD, source and screen candidates for an open role",
        "params": "role (str), requirements (str)",
        "builder": build_recruitment_crew,
    },
    "task_management": {
        "description": "Assign unassigned tasks, track progress, escalate blockers",
        "params": "none",
        "builder": build_task_management_crew,
    },
    "employee_ops": {
        "description": "Run daily standups, collect progress, flag at-risk employees",
        "params": "none",
        "builder": build_employee_ops_crew,
    },
    "finance": {
        "description": "Categorize expenses, generate invoices, build weekly KPI dashboard",
        "params": "period_days (int, default 7)",
        "builder": build_finance_crew,
    },
    "customer_success": {
        "description": "Score customer health, detect churn risk, draft NPS outreach",
        "params": "health_threshold (int, default 40)",
        "builder": build_customer_success_crew,
    },
}

def run_crew(crew_name: str, **kwargs) -> str:
    """Launch a crew by name with optional keyword parameters."""
    if crew_name == "lead_gen":
        from business_os.flows import run_lead_gen_flow
        industry = kwargs.get("target_industry", "B2B SaaS")
        num_leads = kwargs.get("num_leads", 5)
        return run_lead_gen_flow(industry=industry, num_leads=num_leads)

    if crew_name not in CREW_REGISTRY:
        return f"Unknown crew '{crew_name}'. Available: {', '.join(CREW_REGISTRY.keys())}"
    crew = CREW_REGISTRY[crew_name]["builder"](**kwargs)
    return str(crew.kickoff())

def run_all_daily_ops():
    """Full daily operations cycle — call this from cron."""
    print("Business OS: Daily Ops Cycle")
    run_crew("task_management")
    run_crew("employee_ops")
    print("Daily ops complete.")

if __name__ == "__main__":
    init_db()
    import sys
    if len(sys.argv) < 2:
        print("\nBusiness OS — Available crews:")
        for name, meta in CREW_REGISTRY.items():
            print(f"  {name:20} {meta['description']}")
            print(f"  {'':20} Params: {meta['params']}")
        sys.exit(0)
    crew_name = sys.argv[1]
    kwargs = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            kwargs[k] = int(v) if v.isdigit() else v
    print(f"Launching crew: {crew_name} with {kwargs}")
    result = run_crew(crew_name, **kwargs)
    print("\nResult:\n", result)
