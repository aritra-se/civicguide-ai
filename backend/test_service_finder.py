from app.agents.service_finder import create_service_finder_agent

def test_finder():
    print("Initializing Service Finder Agent...")
    agent = create_service_finder_agent()
    
    citizen_query = "I am a 25-year-old unemployed man looking to start a small business. Is there any financial help?"
    print(f"\nUser Query: '{citizen_query}'")
    print("Agent is thinking and searching services...\n")
    
    try:
        response_json = agent.run(citizen_query)
        print("--- STRUCTURED RESPONSE ---")
        print(response_json)
        
    except Exception as e:
        print(f"Error during agent execution: {e}")

if __name__ == "__main__":
    test_finder()