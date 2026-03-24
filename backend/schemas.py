# backend/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime


# ─── AUTH ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserOut(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True


# ─── SECTIONS ──────────────────────────────────────────────────────────────────

class SectionOut(BaseModel):
    id: int
    order_index: int
    title: str
    content: str
    feedback: str
    comment: str
    revision_history: List[Any]

    class Config:
        from_attributes = True

class SectionUpdate(BaseModel):
    feedback: Optional[str] = None
    comment: Optional[str] = None


# ─── PROJECTS ──────────────────────────────────────────────────────────────────

class ProjectCreate(BaseModel):
    title: str
    doc_type: str          # "docx" or "pptx"
    topic: str
    sections: List[str]    # List of section titles/slide titles

class ProjectOut(BaseModel):
    id: int
    title: str
    doc_type: str
    topic: str
    created_at: datetime
    sections: List[SectionOut] = []

    class Config:
        from_attributes = True


# ─── AI ────────────────────────────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    project_id: int

class RefineRequest(BaseModel):
    section_id: int
    prompt: str             # e.g., "Make this more formal"

class SuggestOutlineRequest(BaseModel):
    topic: str
    doc_type: str           # "docx" or "pptx"
