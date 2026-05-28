from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

from business_os.tools.shared_tools import web_search, send_slack, log_action
from business_os.storage.database import get_session, Candidate
from business_os.config.settings import settings


@tool("Save Candidate to Pipeline")
def save_candidate(name: str, email: str, role_applied: str,
                   linkedin_url: str, fit_score: int, notes: str) -> str:
    """Save a sourced and scored candidate to the recruitment pipeline."""
    db = get_session()
    candidate = Candidate(
        name=name, email=email, role_applied=role_applied,
        linkedin_url=linkedin_url, fit_score=fit_score, notes=notes,
    )
    db.add(candidate)
    db.commit()
    cid = candidate.id
    db.close()
    log_action("screener", "recruitment", "save_candidate", "candidate", cid,
               {"name": name, "role": role_applied, "score": fit_score})
    return f"Candidate {name} saved -> ID: {cid} | Fit score: {fit_score}/100"


def build_recruitment_crew(role: str = "Software Engineer",
                           requirements: str = "3+ years Python, FastAPI, PostgreSQL") -> Crew:
    llm = settings.build_llm()
    jd_writer = Agent(
        role="Job Description Writer",
        goal=f"Write a compelling, clear job description for {role} that attracts top talent",
        backstory="Talent acquisition specialist who crafts job descriptions that resonate with great candidates.",
        tools=[],
        llm=llm,
        verbose=True,
    )
    sourcer = Agent(
        role="Talent Sourcer",
        goal=f"Find 10 qualified candidates for {role} using web and LinkedIn research",
        backstory="Experienced recruiter with deep expertise in sourcing passive candidates.",
        tools=[web_search],
        llm=llm,
        verbose=True,
    )
    screener = Agent(
        role="Resume Screener",
        goal=f"Score each candidate against the requirements for {role} and save qualified ones",
        backstory="Technical recruiter who evaluates candidate fit objectively and consistently.",
        tools=[save_candidate],
        llm=llm,
        verbose=True,
    )

    return Crew(
        agents=[jd_writer, sourcer, screener],
        process=Process.sequential,
        verbose=True,
        tasks=[
            Task(
                description=(
                    f"Write a complete job description for {role}. "
                    f"Requirements: {requirements}. "
                    f"Include: role overview, key responsibilities (6-8 bullets), "
                    f"must-have qualifications, nice-to-haves, and benefits."
                ),
                expected_output="Full job description ready to post",
                agent=jd_writer,
            ),
            Task(
                description=(
                    f"Search LinkedIn, GitHub, and tech communities for 10 candidates "
                    f"who match {role} with: {requirements}. "
                    f"For each: full name, email (if findable), LinkedIn URL, and a 2-sentence profile summary."
                ),
                expected_output="List of 10 candidates with name, URL, email, and profile summary",
                agent=sourcer,
            ),
            Task(
                description=(
                    f"Score each candidate 0-100 against these requirements: {requirements}. "
                    f"Factors: years of relevant experience (40%), skill match (40%), "
                    f"communication signals from profile (20%). "
                    f"Save candidates scoring 60 or above to the pipeline."
                ),
                expected_output="Summary: X candidates saved, top 3 candidates with scores",
                agent=screener,
            ),
        ],
    )
