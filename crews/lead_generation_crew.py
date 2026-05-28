from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from business_os.tools.shared_tools import (
    web_search,
    db_query,
    log_action,
    _looks_like_real_linkedin,
    _looks_like_real_email,
)
from business_os.tools.pinecone_tools import query_pinecone_knowledge, scrape_and_learn_website
from business_os.storage.database import get_session, Lead
from business_os.config.settings import settings

# 1. Structured Output Model
class LeadOutput(BaseModel):
    company: str = Field(description="Name of the company/business")
    contact_name: str = Field(description="Name of the verified decision maker or contact person, or 'not found'")
    email: str = Field(description="Verified email address found from search, or 'not found'")
    linkedin_url: str = Field(description="Verified LinkedIn URL found from search, or 'not found'")
    icp_score: int = Field(description="ICP Match score between 0 and 100")
    high_margin_indicators: str = Field(description="Indicators demonstrating that the company sells high-ticket or high-margin products/services")
    notes: str = Field(description="Deep research notes summarizing their business model, tech stack, and pain points")
    outreach_email: str = Field(description="A highly personalized cold outreach email tailored to their pain points, mentioning specific details scraped from their website.")


# 2. CRM Persistence Tool
@tool("Save Qualified Lead to CRM")
def save_qualified_lead(
    company: str,
    contact_name: str,
    email: str,
    linkedin_url: str,
    icp_score: int,
    high_margin_indicators: str,
    notes: str,
    outreach_email: str
) -> str:
    """Save a qualified high-margin lead and personalized cold email draft to the CRM database."""
    # Strict validation to prevent hallucinated placeholders
    verified_email = email if _looks_like_real_email(email) else ''
    verified_linkedin = linkedin_url if _looks_like_real_linkedin(linkedin_url) else ''

    warnings = []
    if email and email.lower() != 'not found' and not verified_email:
        warnings.append(f"Email '{email}' failed validation — cleared.")
    if linkedin_url and linkedin_url.lower() != 'not found' and not verified_linkedin:
        warnings.append(f"LinkedIn URL '{linkedin_url}' failed validation — cleared.")

    formatted_notes = f"""
Business Model & Pain Points:
{notes}

High-Margin Indicators:
{high_margin_indicators}

--- CUSTOM COLD OUTREACH EMAIL ---
{outreach_email}
"""

    db = get_session()
    try:
        # Check if lead already exists
        existing_lead = None
        if verified_email:
            existing_lead = db.query(Lead).filter(Lead.email == verified_email).first()
        if not existing_lead:
            existing_lead = db.query(Lead).filter(Lead.company == company).first()

        if existing_lead:
            existing_lead.contact_name = contact_name if contact_name.lower() != 'not found' else existing_lead.contact_name
            existing_lead.email = verified_email or existing_lead.email
            existing_lead.linkedin_url = verified_linkedin or existing_lead.linkedin_url
            existing_lead.icp_score = icp_score
            existing_lead.notes = formatted_notes
            existing_lead.source = "crawl4ai_pinecone_pipeline"
            lead_id = existing_lead.id
        else:
            new_lead = Lead(
                company=company,
                contact_name=contact_name if contact_name.lower() != 'not found' else '',
                email=verified_email,
                linkedin_url=verified_linkedin,
                icp_score=icp_score,
                status="new",
                source="crawl4ai_pinecone_pipeline",
                notes=formatted_notes
            )
            db.add(new_lead)
            db.commit()
            lead_id = new_lead.id
        
        db.commit()
    except Exception as e:
        db.rollback()
        return f"Error saving lead: {e}"
    finally:
        db.close()

    log_action("lead_saver", "lead_generation", "save_lead", "lead", lead_id, {
        "company": company,
        "icp_score": icp_score,
        "has_email": bool(verified_email),
        "has_linkedin": bool(verified_linkedin)
    })

    result = f"Lead '{company}' successfully saved (ID: {lead_id}, ICP Score: {icp_score}/100)"
    if warnings:
        result += "\n⚠️ " + "\n⚠️ ".join(warnings)
    return result


# 3. Dynamic Lead Scoring Function (deterministic Python, no LLM math)
@tool("Score Lead Quality Deterministically")
def score_lead_deterministically(
    company_description: str,
    company_size: int,
    has_high_margin_indicators: bool,
    has_verified_email: bool,
    has_verified_linkedin: bool
) -> str:
    """Evaluate a lead against our Ideal Customer Profile (ICP) deterministically.
    - company_size: actual count of employees
    - has_high_margin_indicators: True if company sells enterprise/high-ticket or high-margin products/services
    """
    score = 0
    desc = company_description.lower()
    
    # 1. Target industry / business models fit (up to 35 points)
    if "saas" in desc or "software" in desc or "platform" in desc or "technology" in desc:
        score += 25
    elif "consulting" in desc or "agency" in desc or "services" in desc:
        score += 15
        
    # 2. High Margin Premium (up to 30 points)
    if has_high_margin_indicators:
        score += 30
        
    # 3. Target size fit (10-200 employees) (up to 20 points)
    if 10 <= company_size <= 200:
        score += 20
    elif 201 <= company_size <= 1000:
        score += 10 # slightly too large but good
        
    # 4. Verified Contact Data bonus (up to 15 points)
    if has_verified_email:
        score += 10
    if has_verified_linkedin:
        score += 5
        
    return f"ICP Score: {score}/100"


def build_lead_gen_crew(target_industry: str = "SaaS", num_leads: int = 5) -> Crew:
    llm = settings.build_llm()

    # Rule injected to stop hallucinations
    NO_HALLUCINATION = (
        "CRITICAL: Do NOT guess, invent, or fabricate emails, URLs, or LinkedIn pages. "
        "Only report contact details if you found them literally in actual search results "
        "or scraped website contents. If you cannot find them, write 'not found'."
    )

    # Enable throttling only on Gemini to stay under the 5 RPM free tier limit
    max_rpm = 3 if settings.llm_provider.lower() == "gemini" else None

    # 1. Lead Prospector Agent
    prospector = Agent(
        role="B2B Enterprise Lead Prospector",
        goal=f"Discover {num_leads} high-quality, real business prospects in the {target_industry} sector",
        backstory=(
            "You are a master business discovery researcher. You use web search to locate real, active "
            "companies in the target industry. Once you find a target company, you immediately use the "
            "'Scrape and Index Website to Pinecone' tool to scrape and load their website homepage/pricing pages "
            "into vector memory. You never make up company names or websites."
        ),
        tools=[web_search, scrape_and_learn_website],
        llm=llm,
        verbose=True,
        max_rpm=max_rpm,
    )

    # 2. Deep Intelligence Researcher
    researcher = Agent(
        role="B2B High-Margin Intelligence Analyst",
        goal="Extract high-margin business indicators, tech stack details, decision makers, and verified contact info",
        backstory=(
            "You are a data analyst who digs deep into target companies. You query the Pinecone knowledge base "
            "using 'Query Pinecone Knowledge Base' for each prospect company. Your mission is to locate proof "
            "that the company operates a high-margin or high-ticket business model (e.g., enterprise pricing tier, "
            "premium consultancy packages, expensive proprietary tech, large B2B sales). You also search for "
            "factual emails, LinkedIn URLs, and decision-maker names. "
            f"{NO_HALLUCINATION}"
        ),
        tools=[query_pinecone_knowledge, web_search],
        llm=llm,
        verbose=True,
        max_rpm=max_rpm,
    )

    # 3. CRM Writer & Outreach Strategist (Drafting and Scoring Only)
    saver = Agent(
        role="Outreach Personalization & CRM Manager",
        goal="Score leads deterministically and draft custom hyper-personalized cold outreach emails based on website facts",
        backstory=(
            "You are an elite sales outbound copywriter. You take deep research notes and score "
            "the lead deterministically using the 'Score Lead Quality Deterministically' tool. You write custom, "
            "extremely tailored cold outreach emails based on specific facts extracted from their website. "
            "You focus purely on the messaging, personalization, and relevance of the CTA. "
            f"{NO_HALLUCINATION}"
        ),
        tools=[score_lead_deterministically, db_query],
        llm=llm,
        verbose=True,
        max_rpm=max_rpm,
    )

    # 4. B2B Lead Compliance Auditor (Evaluator-Optimizer Loop)
    auditor = Agent(
        role="B2B Lead Quality Compliance Auditor",
        goal="Audit and refine lead profiles, scores, and outreach drafts, and save approved, high-margin leads to the CRM",
        backstory=(
            "You are a meticulous sales quality controller. You analyze lead data and personalized cold emails "
            "drafted by the Outreach Manager. Your job is to enforce that every email contains concrete, factual details "
            "scraped from the target's website and has a clear 15-minute value CTA. You strictly check for "
            "placeholders (like [Your Name], [Insert plan name], or [Date]) and reject drafts that are generic, "
            "refining them using professional sales engineering defaults (e.g., 'Acme Sales Integration Team'). "
            "Once you have polished and approved the lead, you save it to the CRM database using the "
            "'Save Qualified Lead to CRM' tool. "
            f"{NO_HALLUCINATION}"
        ),
        tools=[save_qualified_lead, db_query],
        llm=llm,
        verbose=True,
        max_rpm=max_rpm,
    )

    # Elite Few-Shot Example to guide cheaper models
    FEW_SHOT_PROMPT = (
        "\n\nHere is an example of an elite, hyper-personalized outreach email that you should model your output after:\n"
        "--- START EXAMPLE ---\n"
        "Subject: Scaling Zendesk's healthcare compliance outreach 🤝\n\n"
        "Hi Mikkel,\n\n"
        "I recently came across Zendesk and was impressed by your dedicated focus on providing HIPAA-compliant, "
        "verticalized solutions for healthcare networks. It's clear that providing personalized pricing based on "
        "custom quotes is a major driver of your high-margin Enterprise sales growth.\n\n"
        "At Acme Corp, we specialize in automating structured data ingestion that complements customer service platforms like "
        "Zendesk. We've helped enterprise teams scale their customer success integrations by up to 40% with zero data loss.\n\n"
        "I'd love to schedule a brief 15-minute call next Tuesday at 10 AM to discuss how our automation could assist your "
        "sales engineering team. Do you have a few minutes to connect?\n\n"
        "Best regards,\n"
        "Acme Sales Integration Team\n"
        "--- END EXAMPLE ---\n"
    )

    # Tasks
    tasks = [
        Task(
            description=(
                f"Use 'Web Search Tool' to find {num_leads} REAL active companies in the {target_industry} "
                "industry that fit our Ideal Customer Profile (B2B SaaS/Services). "
                "For each company found, immediately trigger 'Scrape and Index Website to Pinecone' with their website "
                "URL to scrape and ingest their website. "
                "Return a structured list of these target companies with their URLs."
            ),
            expected_output="Numbered list of real target companies with name and website URL, all indexed in Pinecone.",
            agent=prospector,
        ),
        Task(
            description=(
                "For each of the target companies, use the 'Query Pinecone Knowledge Base' tool to search vector memory. "
                "Extract the following information:\n"
                "1. Their core business offering and target audience.\n"
                "2. Proof of high-margin B2B offerings (e.g., enterprise packages, high-ticket services, custom quotes).\n"
                "3. Verified contact email and LinkedIn URL (search web if missing in vector memory, but DO NOT FABRICATE).\n"
                "4. Name and title of the founder, CEO, or high-level decision maker.\n"
                "5. Estimate their company size (employee count).\n"
                "Format this deep research into a comprehensive report for each prospect."
            ),
            expected_output="Detailed intelligence profiles for all prospects detailing business model, high-margin proofs, and verified contact details.",
            agent=researcher,
        ),
        Task(
            description=(
                "For each enriched lead:\n"
                "1. Score the lead deterministically using 'Score Lead Quality Deterministically'.\n"
                "2. Write a highly personalized cold outreach email draft to the decision maker. Reference specific offerings or "
                "tech details discovered from their scraped website (retrieved from Pinecone) to make the email feel organic "
                "and completely custom. Provide a clear 15-minute value CTA connecting their business needs to Acme Corp.\n"
                f"{FEW_SHOT_PROMPT}\n"
                "Do NOT call any CRM saving tools. Simply output a structured draft profile for the lead."
            ),
            expected_output="Bespoke outreach email drafts and deterministic scores for each prospect lead.",
            agent=saver,
        ),
        Task(
            description=(
                "Thoroughly audit and refine the drafted lead profile and outreach email generated in the previous step. "
                "Verify and enforce the following compliance rules:\n"
                "1. The email must be highly tailored, referring to specific scraped B2B offerings or custom plan indicators.\n"
                "2. There must be ZERO generic placeholders (e.g., [Your Name], [CEO Name], [Date], [Contact Info]). Rewrite all "
                "placeholders with concrete professional defaults (e.g., 'Acme Sales Integration Team').\n"
                "3. If the email is generic or poorly structured, edit and rewrite it to a world-class bespoke standard.\n"
                "4. Verify the deterministic score. If the score is 40 or higher, call 'Save Qualified Lead to CRM' to "
                "persist the lead to the CRM database.\n"
                "Report which leads passed compliance and were successfully saved to the CRM."
            ),
            expected_output="Polished lead outreach data with verified CRM database save confirmation.",
            agent=auditor,
            output_pydantic=LeadOutput
        ),
    ]

    return Crew(
        agents=[prospector, researcher, saver, auditor],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        max_rpm=max_rpm,
    )
