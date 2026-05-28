"""
Cron-style scheduler for Business OS crews.
Run: python -m business_os.triggers.scheduler
Dry run: python -m business_os.triggers.scheduler --dry-run
"""
import argparse
import time

import schedule

from business_os.orchestrator import run_crew


SCHEDULED_JOBS = [
    ("daily", "07:00", "task_management", {}),
    ("daily", "07:15", "employee_ops", {}),
    ("monday", "09:00", "market_research", {"topic": "AI automation tools weekly digest"}),
    ("monday", "09:30", "lead_gen", {"target_industry": "B2B SaaS", "num_leads": 10}),
    ("friday", "18:00", "finance", {"period_days": 7}),
    ("friday", "18:30", "customer_success", {"health_threshold": 40}),
]


def run_scheduled_crew(crew_name: str, **kwargs):
    try:
        print(f"Running crew: {crew_name} with {kwargs}")
        result = run_crew(crew_name, **kwargs)
        print(result)
    except Exception as exc:
        print(f"Scheduler error for {crew_name}: {exc}")


def register_jobs():
    for cadence, run_time, crew_name, kwargs in SCHEDULED_JOBS:
        job = lambda crew_name=crew_name, kwargs=kwargs: run_scheduled_crew(crew_name, **kwargs)
        if cadence == "daily":
            schedule.every().day.at(run_time).do(job)
        elif cadence == "monday":
            schedule.every().monday.at(run_time).do(job)
        elif cadence == "friday":
            schedule.every().friday.at(run_time).do(job)


def print_dry_run():
    for cadence, run_time, crew_name, kwargs in SCHEDULED_JOBS:
        params = f" {kwargs}" if kwargs else ""
        print(f"{cadence} at {run_time} -> {crew_name}{params}")


def main():
    parser = argparse.ArgumentParser(description="Business OS cron scheduler")
    parser.add_argument("--dry-run", action="store_true", help="Print scheduled jobs and exit")
    args = parser.parse_args()

    register_jobs()
    if args.dry_run:
        print_dry_run()
        return

    print("Business OS Scheduler started")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
