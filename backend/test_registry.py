from app.services.service_registry import ServiceRegistry

def test_data_load():
    registry = ServiceRegistry()
    services = registry.get_all_services()
    
    if not services:
        print("Failed to load services. Check file path.")
        return
        
    print(f"SUCCESS: Loaded {len(services)} demo services.")
    print(f"First service name: {services[0]['service_name']}")
    print(f"First service disclaimer: {services[0]['disclaimer']}")

if __name__ == "__main__":
    test_data_load()