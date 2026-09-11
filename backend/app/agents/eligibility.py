import os
from groq import Groq
from app.services.service_registry import ServiceRegistry
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
registry = ServiceRegistry()

class EligibilityAgent:
    def __init__(self):
        # Initialize Groq client directly with your API key
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "openai/gpt-oss-20b"

    def run(self, service_id: str, citizen_profile: str) -> str:
        services = registry.get_all_services()
        service_info = next((s for s in services if s["service_id"] == service_id), {"error": "Service not found"})
        
        prompt = f"""
        Evaluate the eligibility of the citizen for the following service:
        Service Details: {service_info}
        Citizen Profile/Statement: "{citizen_profile}"
        
        Compare the citizen's profile against the official requirements. 
        Provide a clear, structured assessment. Clearly distinguish potential eligibility from official approval. Never state they are officially approved.
        """
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
        )
        
        return chat_completion.choices[0].message.content

def create_eligibility_agent():
    return EligibilityAgent()