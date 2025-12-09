from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.services.image_service import ImageService
from src.services.audio_service import AudioService
from src.services.text_service import TextService
from src.services.chat_service import ChatService
from src.services.report_service import ReportService
from src.db.vector_store import vector_store
from src.models.schemas import TextAnalysisRequest, ChatRequest, CreateSessionRequest, ReportRequest
from src.models.models import UploadedFile
from src.config import config
import shutil
import os
import uuid

router = APIRouter()

@router.post("/analyze/image")
async def analyze_image(
    file: UploadFile = File(...), 
    prompt: str = Form("Describe this image."),
    db: Session = Depends(get_db)
):
    # Save file
    file_id = str(uuid.uuid4())
    ext = file.filename.split('.')[-1]
    file_path = os.path.join(config.UPLOAD_DIR, f"{file_id}.{ext}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Analyze
    analysis = await ImageService.analyze_image(file_path, prompt)
    
    # Store metadata & vector
    db_file = UploadedFile(filename=file.filename, file_path=file_path, file_type="image", description=analysis)
    db.add(db_file)
    db.commit()
    
    # Add to Vector DB for retrieval
    vector_store.add_document(
        doc_id=file_id, 
        text=analysis, 
        metadata={"filename": file.filename, "type": "image"}
    )
    
    return {"analysis": analysis, "file_path": file_path}

@router.post("/analyze/audio")
async def analyze_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_id = str(uuid.uuid4())
    ext = file.filename.split('.')[-1]
    file_path = os.path.join(config.UPLOAD_DIR, f"{file_id}.{ext}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    transcript = await AudioService.transcribe_audio(file_path)
    analysis = await AudioService.analyze_audio_content(transcript)
    
    full_text = f"Transcript: {transcript}\n\nAnalysis: {analysis}"
    
    # Store
    db_file = UploadedFile(filename=file.filename, file_path=file_path, file_type="audio", description=full_text)
    db.add(db_file)
    db.commit()
    
    vector_store.add_document(
        doc_id=file_id,
        text=full_text,
        metadata={"filename": file.filename, "type": "audio"}
    )
    
    return {"transcript": transcript, "analysis": analysis}

@router.post("/analyze/text")
async def analyze_text(request: TextAnalysisRequest):
    try:
        result = await TextService.analyze_text(request.text, request.instruction)
        return {"result": result}
    except Exception as e:
        import traceback
        print(f"Error in analyze_text: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/sessions")
def create_session(request: CreateSessionRequest, db: Session = Depends(get_db)):
    session = ChatService.create_session(request.title, db)
    return {"session_id": session.id, "title": session.title}

@router.get("/chat/sessions")
def get_sessions(db: Session = Depends(get_db)):
    return ChatService.get_sessions(db)

@router.post("/chat/message")
async def chat_message(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        response = await ChatService.get_response(request.session_id, request.message, db)
        return {"response": response}
    except Exception as e:
        import traceback
        error_detail = str(e)
        print(f"Chat error: {error_detail}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Chat error: {error_detail}")

@router.get("/chat/history/{session_id}")
def get_history(session_id: int, db: Session = Depends(get_db)):
    return ChatService.get_chat_history(session_id, db)

@router.post("/report")
def generate_report(request: ReportRequest):
    output_path = os.path.join(config.UPLOAD_DIR, request.filename)
    # Convert Pydantic models to dicts
    sections_data = [s.model_dump() for s in request.sections]
    ReportService.generate_pdf(output_path, request.display_title, sections_data)
    return {"file_path": output_path, "url": f"/files/{request.filename}"}
