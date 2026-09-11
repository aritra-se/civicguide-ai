from pydantic import BaseModel
from typing import List

class CivicService(BaseModel):
    service_id: str
    service_name: str
    description: str
    purpose: str
    eligibility_rules: List[str]
    required_documents: List[str]
    application_steps: List[str]
    official_source_url: str
    source_name: str
    last_verified_at: str
    region_state: str
    languages: List[str]
    disclaimer: str