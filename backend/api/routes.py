from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import io
import uuid
import os
from pydantic import BaseModel
from backend.data_quality.profiler import profile_dataset
from backend.data_quality.checks import run_quality_checks
from backend.data_quality.scoring import calculate_quality_score
from backend.llm.llm_analyzer import LLMAnalyzer
from backend.database.vector_store import VectorStore
from backend.chatbot.rag_chatbot import RAGChatbot

router = APIRouter()

# In-memory storage for simplicity (In production, use Redis or a DB)
data_store = {}
vector_store = VectorStore()
llm_analyzer = LLMAnalyzer()
chatbot = RAGChatbot(vector_store)

class ChatRequest(BaseModel):
    dataset_id: str
    question: str

@router.post("/upload_dataset")
async def upload_dataset(file: UploadFile = File(...)):
    try:
        content = await file.read()
        filename = file.filename
        
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(content))
        elif filename.endswith('.json'):
            df = pd.read_json(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        dataset_id = str(uuid.uuid4())
        
        # Profile, Checks, Scoring
        profile = profile_dataset(df)
        issues = run_quality_checks(df)
        score = calculate_quality_score(df, issues)
        
        # Add context to Vector Store for Chat
        context_text = f"Dataset: {filename}\nSummary: {str(profile)}\nIssues: {str(issues)}\nScore: {str(score)}"
        vector_store.add_dataset_context(dataset_id, context_text)
        
        # Get AI Analysis
        ai_analysis = await llm_analyzer.analyze_summary(profile, issues, score)
        
        data_store[dataset_id] = {
            "id": dataset_id,
            "filename": filename,
            "profile": profile,
            "issues": issues,
            "score": score,
            "ai_analysis": ai_analysis
        }
        
        return {"dataset_id": dataset_id, "message": "File uploaded and analyzed successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dataset_profile/{dataset_id}")
async def get_dataset_profile(dataset_id: str):
    if dataset_id not in data_store:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return data_store[dataset_id]["profile"]

@router.get("/quality_report/{dataset_id}")
async def get_quality_report(dataset_id: str):
    if dataset_id not in data_store:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return {
        "issues": data_store[dataset_id]["issues"],
        "ai_analysis": data_store[dataset_id]["ai_analysis"]
    }

@router.get("/quality_score/{dataset_id}")
async def get_quality_score(dataset_id: str):
    if dataset_id not in data_store:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return data_store[dataset_id]["score"]

@router.post("/chat")
async def chat(request: ChatRequest):
    if request.dataset_id not in data_store:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    response = await chatbot.get_response(request.dataset_id, request.question)
    return {"response": response}
