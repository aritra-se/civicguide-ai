from sqlalchemy.orm import Session
from app.models.case_model import CaseModel
import uuid

class CaseManager:
    @staticmethod
    def create_case(db: Session, user_id: str, goal: str, service: str, required_docs: list, missing_docs: list) -> CaseModel:
        case_id = f"CG-{uuid.uuid4().hex[:6].upper()}"
        new_case = CaseModel(
            case_id=case_id,
            user_id=user_id,
            citizen_goal=goal,
            selected_service=service,
            eligibility_status="potentially_eligible",
            required_documents=",".join(required_docs),
            missing_documents=",".join(missing_docs),
            progress_percentage=40.0,
            current_step="Obtain missing documents",
            status="ACTION_REQUIRED"
        )
        db.add(new_case)
        db.commit()
        db.refresh(new_case)
        return new_case

    @staticmethod
    def get_case(db: Session, case_id: str) -> CaseModel:
        return db.query(CaseModel).filter(CaseModel.case_id == case_id).first()