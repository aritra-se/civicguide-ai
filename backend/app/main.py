from fastapi import FastAPI, Depends, Request, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json
import os

from app.database.db import engine, Base, get_db
from app.models.case_model import CaseModel
from app.services.case_manager import CaseManager
from app.agents.root_agent import create_root_agent
from app.agents.document_agent import create_document_agent

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CivicGuide AI API",
    description="Multilingual AI public-service navigator and personal case manager.",
    version="1.0.0"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

master_agent = create_root_agent()
document_agent = create_document_agent()

# Load localizations
LOCALES = {}
for lang in ["en", "bn", "hi"]:
    loc_path = os.path.join(os.path.dirname(__file__), "locales", f"{lang}.json")
    if os.path.exists(loc_path):
        with open(loc_path, "r", encoding="utf-8") as f:
            LOCALES[lang] = json.load(f)

@app.get("/health")
def health_check():
    return {"status": "ok", "system": "CivicGuide AI Backend Operational"}

@app.get("/api/localize/{lang}")
def get_localization(lang: str):
    return LOCALES.get(lang, LOCALES.get("en"))

@app.post("/api/chat")
async def chat_inquiry(request: Request):
    try:
        content_type = request.headers.get("content-type", "")
        if content_type.startswith("application/json"):
            payload = await request.json()
            query = payload.get("query")
            profile = payload.get("profile", payload.get("citizen_profile"))
            language = payload.get("language", "en")
        else:
            form = await request.form()
            query = form.get("query")
            profile = form.get("profile")
            language = form.get("language", "en")

        if not isinstance(query, str) or not query.strip():
            raise HTTPException(status_code=422, detail="query is required")

        result = master_agent.process_citizen_inquiry(query, profile)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/documents/analyze")
async def analyze_uploaded_document(file: UploadFile = File(...), checklist: str = Form(...)):
    try:
        file_bytes = await file.read()
        checklist_items = json.loads(checklist)
        analysis_str = document_agent.analyze_document(file_bytes, file.content_type, checklist_items)
        return json.loads(analysis_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cases/create")
def create_case_endpoint(
    user_id: str = Form(...),
    goal: str = Form(...),
    service: str = Form(...),
    required_docs: str = Form(...),
    missing_docs: str = Form(...),
    db: Session = Depends(get_db)
):
    req_list = json.loads(required_docs)
    miss_list = json.loads(missing_docs)
    case = CaseManager.create_case(db, user_id, goal, service, req_list, miss_list)
    return {"status": "success", "case": {
        "case_id": case.case_id,
        "selected_service": case.selected_service,
        "missing_documents": case.missing_documents,
        "progress_percentage": case.progress_percentage,
        "status": case.status
    }}

@app.get("/api/cases/{case_id}")
@app.get("/api/case/{case_id}")
def get_case_endpoint(case_id: str, db: Session = Depends(get_db)):
    case = CaseManager.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return {
        "case_id": case.case_id,
        "citizen_goal": case.citizen_goal,
        "selected_service": case.selected_service,
        "progress_percentage": case.progress_percentage,
        "missing_documents": case.missing_documents,
        "status": case.status,
        "updated_at": case.updated_at
    }