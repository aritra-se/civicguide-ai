from pydantic import BaseModel, Field
from typing import List

class ServiceRecommendation(BaseModel):
    recommended_services: List[str] = Field(description="List of recommended service IDs")
    reason: str = Field(description="Detailed explanation of why these services match the user's problem")
    confidence: str = Field(description="Confidence level: High, Medium, or Low")
    source_urls: List[str] = Field(description="List of official source URLs for the recommended services")

class EligibilityAssessment(BaseModel):
    status: str = Field(description="Status: 'potentially_eligible', 'information_required', or 'not_eligible'")
    matched_requirements: List[str] = Field(description="List of eligibility rules satisfied by the citizen")
    missing_information: List[str] = Field(description="List of details or documents still required to fully assess eligibility")
    failed_requirements: List[str] = Field(description="List of rules the citizen explicitly fails")
    explanation: str = Field(description="Clear explanation using the required disclaimer: AI guidance only, not an official approval.")

class DocumentAnalysis(BaseModel):
    document_type: str = Field(description="Detected type of document, e.g., 'Income Certificate', 'Identity Proof', 'Unknown'")
    detected_information: dict = Field(description="Key-value pairs of extracted text or details from the document")
    requirements_matched: List[str] = Field(description="List of checklist requirements this document satisfies")
    issues: List[str] = Field(description="Any issues found, such as blurriness, missing signatures, or incomplete fields")
    confidence: str = Field(description="Confidence level of analysis: High, Medium, or Low")
    disclaimer: str = Field(description="Mandatory disclaimer: AI analysis does not prove legal authenticity or official validity.")