import os
from groq import Groq
from dotenv import load_dotenv
from app.agents.service_finder import create_service_finder_agent
from app.agents.eligibility import create_eligibility_agent
from app.agents.document_agent import create_document_agent

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

class MasterCivicGuideAgent:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not configured")
        self.client = Groq(api_key=api_key)
        self.model = "openai/gpt-oss-20b"
        self.service_finder = create_service_finder_agent()
        self.eligibility_agent = create_eligibility_agent()
        self.document_agent = create_document_agent()

    def process_citizen_inquiry(self, query: str, citizen_profile: str = None) -> dict:
        print(f"[Master Agent] Received inquiry via Groq: {query}")
        
        # Delegate to the sub-agents
        service_rec = self.service_finder.run(query)
        
        eligibility_result = None
        if citizen_profile:
            print("[Master Agent] Citizen profile provided. Running eligibility check...")
            eligibility_result = self.eligibility_agent.run("BIZ-GRT-002", citizen_profile)

        return {
            "status": "success",
            "service_recommendation": service_rec,
            "eligibility_assessment": eligibility_result or "Please provide your profile details (age, income, etc.) for a detailed eligibility check.",
            "next_action": "Please review the recommended services and upload required documents to establish your case."
        }

def create_root_agent():
    return MasterCivicGuideAgent()