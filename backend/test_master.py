from app.agents.root_agent import create_root_agent

def test_master():
    print("Initializing Master CivicGuide Orchestrator...")
    master = create_root_agent()
    
    query = "I want to start a micro-business and need financial assistance."
    profile = "I am 25 years old, unemployed, with 10th standard education."
    
    result = master.process_citizen_inquiry(query, profile)
    print("\n--- MASTER AGENT ORCHESTRATION RESULT ---")
    import json
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_master()