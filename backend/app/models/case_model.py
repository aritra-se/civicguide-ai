from sqlalchemy import Column, String, Float, Text, DateTime
from datetime import datetime
from app.database.db import Base

class CaseModel(Base):
    __tablename__ = "cases"

    case_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    preferred_language = Column(String, default="en")
    citizen_goal = Column(Text)
    selected_service = Column(String)
    eligibility_status = Column(String)
    required_documents = Column(Text) # Stored as comma-separated or JSON string
    missing_documents = Column(Text)
    progress_percentage = Column(Float, default=0.0)
    current_step = Column(String)
    status = Column(String, default="NEW") # NEW, IN_PROGRESS, COMPLETED