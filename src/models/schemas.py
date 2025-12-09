from pydantic import BaseModel
from typing import List, Optional

class TextAnalysisRequest(BaseModel):
    text: str
    instruction: str = "Summarize this text."

class ChatRequest(BaseModel):
    session_id: int
    message: str

class CreateSessionRequest(BaseModel):
    title: str

class ReportSection(BaseModel):
    title: Optional[str] = None
    body: str

class ReportRequest(BaseModel):
    filename: str
    display_title: str
    sections: List[ReportSection]
