from app.agents.eligibility import create_eligibility_agent

def test_eligibility():
    print("Initializing Eligibility Agent...")
    agent = create_eligibility_agent()
    
    service_id = "BIZ-GRT-002"
    citizen_profile = "I am 25 years old, unemployed, and have completed 10th standard."
    
    print(f"\nEvaluating Service: {service_id}")
    print(f"Citizen Profile: '{citizen_profile}'\n")
    
    try:
        response_json = agent.run(service_id, citizen_profile)
        print("--- ELIGIBILITY ASSESSMENT ---")
        print(response_json)
    except Exception as e:
        print(f"Error during eligibility check: {e}")

if __name__ == "__main__":
    test_eligibility()