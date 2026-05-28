from crewai import Agent, Task, Crew, Process

from business_os.tools.shared_tools import db_query, update_customer_health, send_slack, save_report
from business_os.config.settings import settings


def build_customer_success_crew(health_threshold: int = 40) -> Crew:
    llm = settings.build_llm()
    health_scorer = Agent(
        role="Customer Health Scorer",
        goal="Compute and update a health score for every active customer",
        backstory="A customer success analyst who monitors account health using behavioral signals.",
        tools=[db_query, update_customer_health],
        llm=llm,
        verbose=True,
    )
    churn_detector = Agent(
        role="Churn Detector",
        goal="Identify at-risk customers and alert the team on Slack",
        backstory="A proactive risk manager who catches churn signals before they become lost revenue.",
        tools=[db_query, send_slack, save_report],
        llm=llm,
        verbose=True,
    )
    nps_agent = Agent(
        role="NPS Outreach Agent",
        goal="Draft personalized check-in emails for healthy customers to collect feedback",
        backstory="A customer success manager who builds loyalty through timely, personal outreach.",
        tools=[db_query, save_report],
        llm=llm,
        verbose=True,
    )

    return Crew(
        agents=[health_scorer, churn_detector, nps_agent],
        process=Process.sequential,
        verbose=True,
        tasks=[
            Task(
                description=(
                    "Query all customers where churn_risk != 'churned'. For each customer compute "
                    "a health score 0-100 using this logic: start at 100; if last_activity is null, "
                    "subtract 30; if last_activity is more than 30 days ago, subtract 25; if "
                    "last_activity is more than 14 days ago, subtract 10; if plan is 'free', subtract "
                    "10; if plan is 'enterprise', add 5; if mrr > 500, add 10; if mrr == 0, subtract "
                    "20. Clamp the final score between 0 and 100. Set churn_risk based on final score: "
                    "score < 30 = 'high', score < 60 = 'medium', score >= 60 = 'low'. Call "
                    "update_customer_health for each customer. Return a summary of all updates."
                ),
                expected_output="Summary listing customer IDs, health scores, and churn risk updates",
                agent=health_scorer,
            ),
            Task(
                description=(
                    f"Query all customers where health_score < {health_threshold} or churn_risk in "
                    "('high', 'medium'). Format a Slack alert listing each at-risk customer with "
                    "their company name, plan, MRR, health score, and churn risk level. Send this to "
                    "channel #customer-success. Also save the alert as a Report with "
                    "report_type='churn_alert'. Return the number of at-risk accounts found."
                ),
                expected_output="Number of at-risk accounts found and alert/report confirmation",
                agent=churn_detector,
            ),
            Task(
                description=(
                    "Query all customers where health_score > 70. For each one, write a personalized "
                    "plain-text check-in email that mentions their plan tier by name, thanks them for "
                    "being a customer, asks one specific open-ended question about their experience, "
                    "and invites them to book a 15-minute call. Do not send the email. Save each draft "
                    "as a Report with report_type='nps_outreach' and title='NPS Outreach - {company}'. "
                    "Return count of drafts saved."
                ),
                expected_output="Count of NPS outreach drafts saved",
                agent=nps_agent,
            ),
        ],
    )
