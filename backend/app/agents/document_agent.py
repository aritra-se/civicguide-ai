import base64
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

class DocumentAgent:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not configured")
        self.client = Groq(api_key=api_key)
        self.model = "qwen/qwen3.6-27b"

    def analyze_document(self, file_bytes: bytes, mime_type: str, required_checklist: list[str]) -> str:
        prompt = f"""
        Analyze this uploaded document for a public service application.
        The required document checklist includes: {required_checklist}
        
        You must return your response strictly as a JSON object with the following keys:
        - "document_type": Detected type of document (e.g., "Income Certificate", "Identity Proof", "Unknown")
        - "detected_information": A dictionary of key-value pairs of extracted text or details from the document
        - "requirements_matched": List of checklist requirements this document satisfies
        - "issues": Any issues found, such as blurriness, missing signatures, or incomplete fields
        - "confidence": Confidence level of analysis ("High", "Medium", or "Low")
        - "disclaimer": Mandatory disclaimer: "AI analysis does not prove legal authenticity or official validity."
        """
        
        encoded_file = base64.b64encode(file_bytes).decode("ascii")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are the CivicGuide Document Review Agent. Inspect documents for informational completeness only and always return pure JSON.",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{encoded_file}"
                            },
                        },
                    ],
                },
            ],
            response_format={"type": "json_object"},
            max_tokens=900,
        )
        return response.choices[0].message.content

def create_document_agent():
    return DocumentAgent()