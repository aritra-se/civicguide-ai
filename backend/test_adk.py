import os
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent

load_dotenv()

# In ADK 2.0+, tools are standard Python functions with type hints and docstrings.
# No @tool decorator is required.
def check_core_system() -> dict:
    """Returns the initialization status of the CivicGuide system."""
    return {"status": "success", "message": "CivicGuide core systems are initialized and ready."}

def test_adk():
    print("Testing Google ADK 2.x Agent initialization...")
    
    try:
        # Initialize the Agent using the current API schema
        test_agent = Agent(
            name="system_check_agent",
            model="gemini-3.6-flash",
            tools=[check_core_system],
            instruction="You are a system diagnostic agent. Call the provided tool to get the status, then format the response nicely."
        )
        
        print("\nSUCCESS: Agent initialized correctly!")
        print(f"Agent Name: {test_agent.name}")
        print(f"Tools loaded: {[t.__name__ for t in test_agent.tools]}")
        
    except Exception as e:
        print("\nADK Error:", str(e))

if __name__ == "__main__":
    test_adk()