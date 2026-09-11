from app.database.db import engine, Base, SessionLocal
from app.models.case_model import CaseModel
from app.services.case_manager import CaseManager

def test_db_persistence():
    print("Initializing SQLite database...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # 1. Create a case
    print("Creating a new persistent case...")
    case = CaseManager.create_case(
        db=db,
        user_id="user_123",
        goal="Start a micro-business",
        service="Demo Micro-Enterprise Starter Grant (BIZ-GRT-002)",
        required_docs=["Identity proof", "Income certificate"],
        missing_docs=["Income certificate"]
    )
    print(f"SUCCESS: Created Case ID -> {case.case_id}")
    
    # 2. Simulate returning later ("What is left?")
    print("Simulating citizen returning later to check case...")
    retrieved_case = CaseManager.get_case(db, case.case_id)
    
    print(f"\n--- RETRIEVED CASE RECORD ---")
    print(f"Case ID: {retrieved_case.case_id}")
    print(f"Goal: {retrieved_case.citizen_goal}")
    print(f"Service: {retrieved_case.selected_service}")
    print(f"Progress: {retrieved_case.progress_percentage}%")
    print(f"Missing Documents / What is Left: {retrieved_case.missing_documents}")
    print(f"Current Status: {retrieved_case.status}")
    
    db.close()

if __name__ == "__main__":
    test_db_persistence()