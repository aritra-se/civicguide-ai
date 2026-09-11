import os
from groq import Groq
from app.services.service_registry import ServiceRegistry
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

registry = ServiceRegistry()

class ServiceFinderAgent:
    def __init__(self):
        # Initialize Groq client
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        # Use openai/gpt-oss-20b or another active model
        self.model = "openai/gpt-oss-20b"

    def run(self, query: str) -> str:
        services = registry.get_all_services()
        
        prompt = f"""
        You are the CivicGuide Service Finder Agent. 
        Available government services: {services}
        
        Analyze the citizen's problem: "{query}"
        Match the most relevant service(s) from the available list and provide a clear, structured recommendation. Never invent government services.
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

def create_service_finder_agent():
    return ServiceFinderAgent()