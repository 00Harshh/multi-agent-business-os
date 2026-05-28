"""
CrewAI Flows for the Business OS rebuild.
Coordinates cross-crew execution sequentially and shares state context.
"""
from pydantic import BaseModel
from crewai.flow.flow import Flow, start, listen
from business_os.crews.market_research_crew import build_market_research_crew
from business_os.crews.lead_generation_crew import build_lead_gen_crew
from business_os.config.settings import settings


class LeadGenState(BaseModel):
    industry: str = "B2B SaaS"
    num_leads: int = 5
    market_research_report: str = ""
    pipeline_result: str = ""


class BusinessOSLeadGenFlow(Flow[LeadGenState]):

    @start()
    def conduct_market_research(self) -> str:
        """Step 1: Discover trends, competitors, and pain points in the target industry."""
        print(f"\n🌊 [Flow] Step 1: Conducting market research on: {self.state.industry}")
        
        crew = build_market_research_crew(topic=f"{self.state.industry} industry trends and pain points")
        result = crew.kickoff()
        
        self.state.market_research_report = str(result)
        print("🌊 [Flow] Market research completed and saved to flow state.")
        return self.state.market_research_report

    @listen(conduct_market_research)
    def discover_high_margin_leads(self, research_report: str) -> str:
        """Step 2: Use the market trends report to scrape and discover qualified high-margin leads."""
        print(f"\n🌊 [Flow] Step 2: Discovering high-margin B2B leads in: {self.state.industry}")
        
        # Build lead gen crew
        crew = build_lead_gen_crew(target_industry=self.state.industry, num_leads=self.state.num_leads)
        
        # Inject the market research insights as context into the first task of the crew
        if self.state.market_research_report:
            prospector_task = crew.tasks[0]
            prospector_task.description = (
                f"{prospector_task.description}\n\n"
                f"Use this newly generated market research context to identify the best niches, "
                f"problems, and target company profiles:\n"
                f"{self.state.market_research_report}"
            )
            
        result = crew.kickoff()
        self.state.pipeline_result = str(result)
        
        # Save the qualified lead to CRM deterministically in Python
        if hasattr(result, 'pydantic') and result.pydantic:
            try:
                lead_data = result.pydantic
                print(f"🌊 [Flow] Saving qualified lead '{lead_data.company}' to CRM deterministically in Python...")
                from business_os.crews.lead_generation_crew import save_qualified_lead
                save_res = save_qualified_lead.func(
                    company=lead_data.company,
                    contact_name=lead_data.contact_name,
                    email=lead_data.email,
                    linkedin_url=lead_data.linkedin_url,
                    icp_score=lead_data.icp_score,
                    high_margin_indicators=lead_data.high_margin_indicators,
                    notes=lead_data.notes,
                    outreach_email=lead_data.outreach_email
                )
                print(f"🌊 [Flow] Database save result: {save_res}")
            except Exception as ex:
                print(f"⚠️ [Flow] Error saving lead deterministically: {ex}")
        else:
            print("⚠️ [Flow] No structured Pydantic output received from Lead Gen crew.")
            
        print("🌊 [Flow] High-margin lead discovery completed!")
        return self.state.pipeline_result


def run_lead_gen_flow(industry: str = "B2B SaaS", num_leads: int = 5) -> str:
    """Entry point to run the end-to-end B2B Lead Gen Flow."""
    print(f"Initializing Lead Gen Flow for '{industry}' (target: {num_leads} leads)...")
    
    flow = BusinessOSLeadGenFlow()
    flow.state.industry = industry
    flow.state.num_leads = num_leads
    
    flow.kickoff()
    return flow.state.pipeline_result


if __name__ == "__main__":
    import sys
    industry = "B2B SaaS"
    num_leads = 5
    if len(sys.argv) > 1:
        industry = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2].isdigit():
        num_leads = int(sys.argv[2])
        
    result = run_lead_gen_flow(industry, num_leads)
    print("\n🌊 Flow Execution Summary:")
    print(result)
