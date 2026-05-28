from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

from business_os.tools.shared_tools import web_search, log_action
from business_os.storage.database import get_session, Report
from business_os.config.settings import settings


@tool("Save Research Report")
def save_report(title: str, report_type: str, content: str) -> str:
    """Persist a market research report to the database."""
    db = get_session()
    report = Report(title=title, report_type=report_type, content=content)
    db.add(report)
    db.commit()
    report_id = report.id
    db.close()
    log_action("reporter", "market_research", "save_report", "report", report_id,
               {"title": title, "type": report_type})
    return f"Report saved -> ID: {report_id}"


def build_market_research_crew(topic: str = "AI software market") -> Crew:
    llm = settings.build_llm(model_name="gemini/gemini-flash-latest")
    
    # Enable throttling only on Gemini to stay under the 5 RPM free tier limit
    max_rpm = 3 if settings.llm_provider.lower() == "gemini" else None

    analyst = Agent(
        role="Market Analyst",
        goal=f"Research the current state of {topic}: key players, market size, recent news",
        backstory="Senior market analyst specialising in competitive intelligence and industry mapping.",
        tools=[web_search],
        llm=llm,
        verbose=True,
        max_rpm=max_rpm,
    )
    trend_scout = Agent(
        role="Trend Scout",
        goal=f"Identify the 5 most significant emerging trends in {topic} over the last 90 days",
        backstory="Forward-thinking researcher who spots early signals before they become mainstream.",
        tools=[web_search],
        llm=llm,
        verbose=True,
        max_rpm=max_rpm,
    )
    reporter = Agent(
        role="Research Reporter",
        goal="Synthesize all research into a single actionable report and save it to the database",
        backstory="Business writer who turns raw intelligence into concise, executive-ready insights.",
        tools=[save_report],
        llm=llm,
        verbose=True,
        max_rpm=max_rpm,
    )

    return Crew(
        agents=[analyst, trend_scout, reporter],
        process=Process.sequential,
        verbose=True,
        max_rpm=max_rpm,
        tasks=[
            Task(
                description=(
                    f"Research {topic}. Cover: (1) estimated market size, (2) top 5 competitors "
                    f"with brief profiles, (3) recent funding rounds or M&A activity, "
                    f"(4) customer segments being targeted."
                ),
                expected_output="Structured market overview with sources and URLs",
                agent=analyst,
            ),
            Task(
                description=(
                    f"Find the 5 biggest trends shaping {topic} right now. "
                    f"For each trend: name it, explain the driver, cite evidence, "
                    f"and estimate its relevance horizon (3 months / 1 year / 3 years)."
                ),
                expected_output="Numbered list of 5 trends with evidence and time horizons",
                agent=trend_scout,
            ),
            Task(
                description=(
                    "Combine the market overview and trends into one well-structured report. "
                    "Include: executive summary, market snapshot, top 5 trends, and 3 actionable "
                    "recommendations for our business. Save it to the database."
                ),
                expected_output="Confirmation that the report was saved with its database ID",
                agent=reporter,
            ),
        ],
    )
