# 🚀 AI-Assisted Document Authoring Platform — Complete Beginner Guide

> **Who this is for:** A frontend developer with little/no backend experience.
> We'll go step by step — every command, every file, every explanation.

---

## 📋 Table of Contents

1. [What We're Building](#what-were-building)
2. [Tech Stack Decisions](#tech-stack-decisions)
3. [Prerequisites — Install These First](#prerequisites)
4. [GitHub Repository Setup](#github-setup)
5. [Project Folder Structure](#folder-structure)
6. [Backend Setup (FastAPI)](#backend-setup)
   - [Install Python dependencies](#backend-dependencies)
   - [Database models](#database-models)
   - [Authentication (JWT)](#authentication)
   - [All API routes](#api-routes)
   - [AI service](#ai-service)
   - [Export service (docx/pptx)](#export-service)
7. [Frontend Setup (React + Vite)](#frontend-setup)
   - [All pages and components](#frontend-components)
8. [Environment Variables](#environment-variables)
9. [Running the Project](#running-the-project)
10. [Useful Docs & Links](#useful-links)

---

## 1. What We're Building <a name="what-were-building"></a>

A web app where users can:
1. **Register/Login** (accounts stored in a database)
2. **Create a project** → choose Word (.docx) or PowerPoint (.pptx)
3. **Configure the structure** (section headers for Word, slide titles for PPT)
4. **Generate content** using an AI (Claude API)
5. **Refine content** section by section (ask AI to rewrite, like/dislike, add comments)
6. **Export** the final document as a real .docx or .pptx file

Think of it like Google Docs but with an AI writing assistant baked in.

---

## 2. Tech Stack Decisions <a name="tech-stack-decisions"></a>

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | **FastAPI** (Python) | Fast, modern, automatic docs at `/docs` |
| Database | **SQLite** (via SQLAlchemy) | Zero setup, file-based, perfect for dev |
| Auth | **JWT tokens** | Industry standard, stateless |
| Frontend | **React + Vite** | Fast dev server, modern React |
| HTTP client | **Axios** | Easier than fetch for API calls |
| Styling | **Tailwind CSS** | Utility classes, fast to build UI |
| AI | **Claude API (Anthropic)** | Powerful, easy to call |
| Word export | **python-docx** | Python library for .docx files |
| PPT export | **python-pptx** | Python library for .pptx files |

---

## 3. Prerequisites — Install These First <a name="prerequisites"></a>

### Step 1: Install Python 3.10+
Go to https://www.python.org/downloads/ → download and install.

After install, verify:
```bash
python --version
# Should show Python 3.10.x or higher
```

### Step 2: Install Node.js 18+
Go to https://nodejs.org/ → download LTS version.

After install, verify:
```bash
node --version   # v18.x.x or higher
npm --version    # 9.x.x or higher
```

### Step 3: Install Git
Go to https://git-scm.com/downloads → install.

After install, verify:
```bash
git --version
```

### Step 4: Get a Code Editor
Download **VS Code**: https://code.visualstudio.com/

### Step 5: Get your Anthropic API Key
Go to https://console.anthropic.com/ → sign up → go to "API Keys" → create a key.
Copy and save it somewhere safe. It looks like: `sk-ant-api03-...`

---

## 4. GitHub Repository Setup <a name="github-setup"></a>

### Step 1: Create a GitHub account
Go to https://github.com and sign up if you don't have an account.

### Step 2: Create a new repository
1. Click the **+** icon in top-right → "New repository"
2. Name it: `ai-doc-platform`
3. Set to **Public** (or Private)
4. Check "Add a README file"
5. Click **Create repository**

### Step 3: Clone it to your computer
```bash
# Replace YOUR_USERNAME with your GitHub username
git clone https://github.com/YOUR_USERNAME/ai-doc-platform.git
cd ai-doc-platform
```

### Step 4: Set up your Git identity (first time only)
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Step 5: Create a .gitignore file
Inside the `ai-doc-platform` folder, create a file called `.gitignore` with this content:

```
# Python
__pycache__/
*.py[cod]
.env
venv/
*.db

# Node
node_modules/
dist/
.env.local
```

---

## 5. Project Folder Structure <a name="folder-structure"></a>

After everything is set up, your project will look like this:

```
ai-doc-platform/
├── backend/
│   ├── main.py              ← FastAPI app entry point
│   ├── database.py          ← SQLite connection setup
│   ├── models.py            ← Database table definitions
│   ├── schemas.py           ← Data shape definitions (Pydantic)
│   ├── auth.py              ← JWT token logic
│   ├── routes/
│   │   ├── auth_routes.py   ← /register, /login endpoints
│   │   ├── project_routes.py← /projects CRUD endpoints
│   │   ├── ai_routes.py     ← /generate, /refine endpoints
│   │   └── export_routes.py ← /export endpoint
│   ├── services/
│   │   ├── ai_service.py    ← Claude API calls
│   │   ├── docx_service.py  ← Build .docx files
│   │   └── pptx_service.py  ← Build .pptx files
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── RegisterPage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── ConfigurePage.jsx
│   │   │   └── EditorPage.jsx
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   └── SectionCard.jsx
│   │   ├── context/
│   │   │   └── AuthContext.jsx  ← Stores user login state
│   │   ├── api.js               ← Axios setup
│   │   └── App.jsx
│   ├── index.html
│   └── package.json
├── .gitignore
└── README.md
```

Let's now create everything.

---

## 6. Backend Setup <a name="backend-setup"></a>

### Step 1: Create the backend folder and virtual environment

```bash
# From the ai-doc-platform root folder:
mkdir backend
cd backend

# Create a Python virtual environment (like a sandboxed Python install)
python -m venv venv

# Activate it:
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Your terminal prompt should now show (venv) at the start
```

### Step 2: Install dependencies <a name="backend-dependencies"></a>

```bash
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart python-dotenv anthropic python-docx python-pptx
```

What each package does:
- `fastapi` — our backend framework
- `uvicorn` — runs the FastAPI server
- `sqlalchemy` — talks to our SQLite database
- `python-jose[cryptography]` — creates/verifies JWT tokens
- `passlib[bcrypt]` — hashes passwords securely
- `python-multipart` — handles form data
- `python-dotenv` — reads .env file
- `anthropic` — Claude AI SDK
- `python-docx` — creates Word documents
- `python-pptx` — creates PowerPoint files

Now save these to a file:
```bash
pip freeze > requirements.txt
```

### Step 3: Create the .env file

Inside the `backend/` folder, create a file named `.env`:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production-make-it-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

> ⚠️ **Never commit this file to GitHub.** The .gitignore we created already excludes it.

---

### Step 4: database.py

This file sets up our SQLite database connection.

```python
# backend/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This creates a file called "app.db" in the backend folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# This function gives us a database session for each API request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### Step 5: models.py — Database Tables <a name="database-models"></a>

Think of models as table definitions. Each class = one table in the database.

```python
# backend/models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    projects = relationship("Project", back_populates="owner")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    doc_type = Column(String, nullable=False)  # "docx" or "pptx"
    topic = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="projects")
    sections = relationship("Section", back_populates="project", cascade="all, delete")


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    order_index = Column(Integer, nullable=False)   # Position in document
    title = Column(String, nullable=False)           # Section header or slide title
    content = Column(Text, default="")               # AI-generated content
    feedback = Column(String, default="none")        # "liked", "disliked", or "none"
    comment = Column(Text, default="")               # User's note
    revision_history = Column(JSON, default=list)    # List of past content versions

    project = relationship("Project", back_populates="sections")
```

---

### Step 6: schemas.py — Data Shapes

Schemas define what data looks like when it goes in/out of the API.

```python
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
```

---

### Step 7: auth.py — JWT Token Logic <a name="authentication"></a>

This handles password hashing and creating/reading JWT tokens.

```python
# backend/auth.py

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from database import get_db
import models

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 10080))

# This handles password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# This tells FastAPI where to find the token (in the Authorization header)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def hash_password(password: str) -> str:
    """Turn plain text password into a hash"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if plain text matches the hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """Extract user from JWT token — used as a dependency in protected routes"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
```

---

### Step 8: routes/auth_routes.py

```python
# backend/routes/auth_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
import models, schemas
from auth import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=schemas.UserOut)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists
    if db.query(models.User).filter(models.User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Create new user with hashed password
    new_user = models.User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create and return JWT token
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

---

### Step 9: routes/project_routes.py <a name="api-routes"></a>

```python
# backend/routes/project_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models, schemas
from auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=schemas.ProjectOut)
def create_project(
    project_data: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new project with sections"""
    # Create the project
    new_project = models.Project(
        title=project_data.title,
        doc_type=project_data.doc_type,
        topic=project_data.topic,
        owner_id=current_user.id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    # Create sections for each title provided
    for i, section_title in enumerate(project_data.sections):
        section = models.Section(
            project_id=new_project.id,
            order_index=i,
            title=section_title,
            content="",
            revision_history=[]
        )
        db.add(section)
    
    db.commit()
    db.refresh(new_project)
    return new_project


@router.get("/", response_model=List[schemas.ProjectOut])
def get_all_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all projects for the logged-in user"""
    return db.query(models.Project).filter(
        models.Project.owner_id == current_user.id
    ).all()


@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get a single project with all sections"""
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a project"""
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}


@router.patch("/sections/{section_id}", response_model=schemas.SectionOut)
def update_section_feedback(
    section_id: int,
    update_data: schemas.SectionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update feedback or comment on a section"""
    section = db.query(models.Section).filter(
        models.Section.id == section_id
    ).first()
    
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    if update_data.feedback is not None:
        section.feedback = update_data.feedback
    if update_data.comment is not None:
        section.comment = update_data.comment
    
    db.commit()
    db.refresh(section)
    return section
```

---

### Step 10: services/ai_service.py <a name="ai-service"></a>

```python
# backend/services/ai_service.py

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def generate_section_content(topic: str, section_title: str, doc_type: str) -> str:
    """
    Ask Claude to write content for one section of a document.
    
    topic: The main document topic (e.g., "EV market analysis 2025")
    section_title: The specific section (e.g., "Market Overview")
    doc_type: "docx" or "pptx"
    """
    if doc_type == "pptx":
        prompt = f"""You are creating content for a PowerPoint slide.

Document topic: {topic}
Slide title: {section_title}

Write concise bullet points for this slide (4-6 bullet points).
Each bullet point should be 1-2 sentences max.
Do NOT include the slide title in your response.
Start directly with the bullet points using "•" as the bullet character."""
    else:
        prompt = f"""You are writing a section of a business document.

Document topic: {topic}
Section title: {section_title}

Write 2-3 paragraphs of professional content for this section.
Do NOT include the section title in your response.
Write in a clear, professional business writing style."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text


def refine_section_content(
    current_content: str,
    section_title: str,
    refinement_prompt: str,
    doc_type: str
) -> str:
    """
    Refine existing content based on user's instruction.
    
    current_content: What's already written
    refinement_prompt: User's instruction (e.g., "Make this more formal")
    """
    prompt = f"""You are editing a section of a {'PowerPoint slide' if doc_type == 'pptx' else 'business document'}.

Section title: {section_title}

Current content:
{current_content}

User's refinement request: {refinement_prompt}

Please rewrite the content according to the user's request.
Maintain the same format (bullet points for slides, paragraphs for documents).
Return ONLY the rewritten content, nothing else."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text


def suggest_outline(topic: str, doc_type: str) -> list:
    """
    Bonus feature: AI suggests section/slide titles for a topic.
    Returns a list of strings.
    """
    if doc_type == "pptx":
        prompt = f"""Suggest 8-10 slide titles for a PowerPoint presentation about: {topic}

Return ONLY a JSON array of strings, no other text.
Example: ["Introduction", "Market Overview", "Key Findings"]"""
    else:
        prompt = f"""Suggest 6-8 section headers for a business document about: {topic}

Return ONLY a JSON array of strings, no other text.
Example: ["Executive Summary", "Introduction", "Market Analysis"]"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    import json
    raw = message.content[0].text.strip()
    # Clean up if Claude wrapped it in markdown code blocks
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())
```

---

### Step 11: routes/ai_routes.py

```python
# backend/routes/ai_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models, schemas
from auth import get_current_user
from services.ai_service import generate_section_content, refine_section_content, suggest_outline

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/generate/{project_id}")
def generate_all_content(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Generate AI content for ALL sections of a project"""
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Generate content for each section one by one
    for section in project.sections:
        generated_text = generate_section_content(
            topic=project.topic,
            section_title=section.title,
            doc_type=project.doc_type
        )
        section.content = generated_text
        section.revision_history = []  # Reset history on new generation
    
    db.commit()
    
    # Return updated project
    db.refresh(project)
    return {"message": "Content generated", "project_id": project_id}


@router.post("/refine", response_model=schemas.SectionOut)
def refine_content(
    refine_data: schemas.RefineRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Refine a single section's content"""
    section = db.query(models.Section).filter(
        models.Section.id == refine_data.section_id
    ).first()
    
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    # Save current content to history before overwriting
    history = list(section.revision_history or [])
    history.append(section.content)
    section.revision_history = history

    # Get the project for context
    project = db.query(models.Project).filter(
        models.Project.id == section.project_id
    ).first()

    # Call AI to refine
    new_content = refine_section_content(
        current_content=section.content,
        section_title=section.title,
        refinement_prompt=refine_data.prompt,
        doc_type=project.doc_type
    )
    section.content = new_content
    
    db.commit()
    db.refresh(section)
    return section


@router.post("/suggest-outline")
def get_suggested_outline(
    request: schemas.SuggestOutlineRequest,
    current_user: models.User = Depends(get_current_user)
):
    """Bonus: AI suggests section/slide titles"""
    titles = suggest_outline(request.topic, request.doc_type)
    return {"titles": titles}
```

---

### Step 12: services/docx_service.py <a name="export-service"></a>

```python
# backend/services/docx_service.py

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io


def build_docx(project_title: str, topic: str, sections: list) -> bytes:
    """
    Build a .docx file from project sections.
    Returns file as bytes.
    """
    doc = Document()

    # ── Title page ────────────────────────────────────────────────────────────
    title_para = doc.add_heading(project_title, level=0)
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    topic_para = doc.add_paragraph(f"Topic: {topic}")
    topic_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_page_break()

    # ── Table of Contents (simple text list) ──────────────────────────────────
    doc.add_heading("Table of Contents", level=1)
    for section in sections:
        doc.add_paragraph(section["title"], style="List Number")
    doc.add_page_break()

    # ── Sections ──────────────────────────────────────────────────────────────
    for section in sections:
        # Section heading
        doc.add_heading(section["title"], level=1)

        # Section content
        content = section.get("content", "")
        if content:
            for paragraph in content.split("\n"):
                paragraph = paragraph.strip()
                if paragraph:
                    doc.add_paragraph(paragraph)
        
        doc.add_paragraph()  # Blank line between sections

    # ── Save to bytes ─────────────────────────────────────────────────────────
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
```

---

### Step 13: services/pptx_service.py

```python
# backend/services/pptx_service.py

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import io


def build_pptx(project_title: str, topic: str, sections: list) -> bytes:
    """
    Build a .pptx file from project sections.
    Returns file as bytes.
    """
    prs = Presentation()

    # Slide dimensions (widescreen 16:9)
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    # ── Title slide ───────────────────────────────────────────────────────────
    title_layout = prs.slide_layouts[0]  # Title slide layout
    slide = prs.slides.add_slide(title_layout)

    slide.shapes.title.text = project_title
    slide.placeholders[1].text = topic

    # ── Content slides ────────────────────────────────────────────────────────
    content_layout = prs.slide_layouts[1]  # Title and Content layout

    for section in sections:
        slide = prs.slides.add_slide(content_layout)
        
        # Set slide title
        slide.shapes.title.text = section["title"]

        # Set slide content
        content = section.get("content", "")
        tf = slide.placeholders[1].text_frame
        tf.clear()

        if content:
            lines = [line.strip() for line in content.split("\n") if line.strip()]
            for i, line in enumerate(lines):
                # Remove bullet character if AI included it
                clean_line = line.lstrip("•-* ").strip()
                if i == 0:
                    tf.paragraphs[0].text = clean_line
                else:
                    p = tf.add_paragraph()
                    p.text = clean_line
                    p.level = 0

    # ── Save to bytes ─────────────────────────────────────────────────────────
    buffer = io.BytesIO()
    prs.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
```

---

### Step 14: routes/export_routes.py

```python
# backend/routes/export_routes.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from database import get_db
import models
from auth import get_current_user
from services.docx_service import build_docx
from services.pptx_service import build_pptx

router = APIRouter(prefix="/export", tags=["Export"])


@router.get("/{project_id}")
def export_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Export the project as a .docx or .pptx file"""
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Build sections list for the export service
    sections_data = [
        {
            "title": s.title,
            "content": s.content
        }
        for s in sorted(project.sections, key=lambda x: x.order_index)
    ]

    if project.doc_type == "docx":
        file_bytes = build_docx(project.title, project.topic, sections_data)
        filename = f"{project.title.replace(' ', '_')}.docx"
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:
        file_bytes = build_pptx(project.title, project.topic, sections_data)
        filename = f"{project.title.replace(' ', '_')}.pptx"
        media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

    return Response(
        content=file_bytes,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
```

---

### Step 15: main.py — Putting it all together

```python
# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
import models

# Import all routers
from routes.auth_routes import router as auth_router
from routes.project_routes import router as project_router
from routes.ai_routes import router as ai_router
from routes.export_routes import router as export_router

# Create all database tables (runs once on startup)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Document Platform API",
    description="Generate and export AI-powered Word & PowerPoint documents",
    version="1.0.0"
)

# ── CORS Setup ────────────────────────────────────────────────────────────────
# This allows the frontend (running on localhost:5173) to call our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register all routes ───────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(ai_router)
app.include_router(export_router)


@app.get("/")
def root():
    return {"message": "AI Document Platform API is running!"}
```

### Step 16: Run the backend

```bash
# Make sure you're in the backend/ folder with venv activated
cd backend
uvicorn main:app --reload

# You should see:
# INFO: Uvicorn running on http://127.0.0.1:8000
```

Visit http://localhost:8000/docs — you'll see your auto-generated API documentation!

---

## 7. Frontend Setup <a name="frontend-setup"></a>

Open a new terminal (keep the backend running).

### Step 1: Create React app with Vite

```bash
# Go back to the root folder
cd ..   # Now you're in ai-doc-platform/

# Create React app
npm create vite@latest frontend -- --template react
cd frontend
npm install

# Install extra packages
npm install axios react-router-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Step 2: Configure Tailwind

Open `frontend/tailwind.config.js` and replace with:

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Open `frontend/src/index.css` and replace ALL content with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

### Step 3: src/api.js — Axios Setup

```js
// frontend/src/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

// Automatically attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

---

### Step 4: src/context/AuthContext.jsx

This stores the user's login state across the whole app.

```jsx
// frontend/src/context/AuthContext.jsx
import { createContext, useContext, useState, useEffect } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"));

  const login = (accessToken) => {
    localStorage.setItem("token", accessToken);
    setToken(accessToken);
    setIsLoggedIn(true);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setIsLoggedIn(false);
  };

  return (
    <AuthContext.Provider value={{ token, isLoggedIn, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook — use this anywhere: const { isLoggedIn } = useAuth()
export function useAuth() {
  return useContext(AuthContext);
}
```

---

### Step 5: src/pages/LoginPage.jsx

```jsx
// frontend/src/pages/LoginPage.jsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await api.post("/auth/login", { email, password });
      login(res.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-md">
        <h1 className="text-3xl font-bold text-center text-blue-600 mb-2">DocAI</h1>
        <p className="text-center text-gray-500 mb-6">Sign in to your account</p>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="••••••••"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 transition"
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <p className="text-center text-sm text-gray-500 mt-4">
          Don't have an account?{" "}
          <Link to="/register" className="text-blue-600 font-medium hover:underline">
            Register
          </Link>
        </p>
      </div>
    </div>
  );
}
```

---

### Step 6: src/pages/RegisterPage.jsx

```jsx
// frontend/src/pages/RegisterPage.jsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api";

export default function RegisterPage() {
  const [form, setForm] = useState({ email: "", username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await api.post("/auth/register", form);
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-md">
        <h1 className="text-3xl font-bold text-center text-blue-600 mb-2">DocAI</h1>
        <p className="text-center text-gray-500 mb-6">Create your account</p>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {["email", "username", "password"].map((field) => (
            <div key={field}>
              <label className="block text-sm font-medium text-gray-700 mb-1 capitalize">
                {field}
              </label>
              <input
                type={field === "password" ? "password" : field === "email" ? "email" : "text"}
                name={field}
                value={form[field]}
                onChange={handleChange}
                required
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          ))}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 transition"
          >
            {loading ? "Creating account..." : "Create Account"}
          </button>
        </form>

        <p className="text-center text-sm text-gray-500 mt-4">
          Already have an account?{" "}
          <Link to="/login" className="text-blue-600 font-medium hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
```

---

### Step 7: src/pages/DashboardPage.jsx

```jsx
// frontend/src/pages/DashboardPage.jsx
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { useAuth } from "../context/AuthContext";

export default function DashboardPage() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const { logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const res = await api.get("/projects/");
      setProjects(res.data);
    } catch (err) {
      console.error("Failed to fetch projects", err);
    } finally {
      setLoading(false);
    }
  };

  const deleteProject = async (id) => {
    if (!confirm("Delete this project?")) return;
    await api.delete(`/projects/${id}`);
    setProjects(projects.filter((p) => p.id !== id));
  };

  const docTypeLabel = (type) =>
    type === "docx" ? "📄 Word Document" : "📊 PowerPoint";

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="bg-white border-b px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-blue-600">DocAI</h1>
        <div className="flex gap-3">
          <button
            onClick={() => navigate("/configure")}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition"
          >
            + New Project
          </button>
          <button
            onClick={logout}
            className="text-gray-500 px-4 py-2 rounded-lg text-sm hover:bg-gray-100 transition"
          >
            Logout
          </button>
        </div>
      </nav>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-6 py-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">My Projects</h2>

        {loading ? (
          <p className="text-gray-500">Loading...</p>
        ) : projects.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-2xl border border-dashed border-gray-300">
            <p className="text-gray-400 text-lg mb-4">No projects yet</p>
            <button
              onClick={() => navigate("/configure")}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition"
            >
              Create your first project
            </button>
          </div>
        ) : (
          <div className="grid gap-4">
            {projects.map((project) => (
              <div
                key={project.id}
                className="bg-white rounded-xl shadow-sm border p-5 flex justify-between items-center"
              >
                <div>
                  <h3 className="font-semibold text-gray-800 text-lg">{project.title}</h3>
                  <p className="text-gray-500 text-sm mt-1">
                    {docTypeLabel(project.doc_type)} · {project.sections.length} sections
                  </p>
                  <p className="text-gray-400 text-xs mt-1">
                    {new Date(project.created_at).toLocaleDateString()}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => navigate(`/editor/${project.id}`)}
                    className="bg-blue-50 text-blue-600 px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-100 transition"
                  >
                    Open
                  </button>
                  <button
                    onClick={() => deleteProject(project.id)}
                    className="bg-red-50 text-red-500 px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-100 transition"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
```

---

### Step 8: src/pages/ConfigurePage.jsx

```jsx
// frontend/src/pages/ConfigurePage.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

export default function ConfigurePage() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [docType, setDocType] = useState("docx");
  const [title, setTitle] = useState("");
  const [topic, setTopic] = useState("");
  const [sections, setSections] = useState(["Introduction", "Main Body", "Conclusion"]);
  const [newSection, setNewSection] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggesting, setSuggesting] = useState(false);

  // Add a new section/slide title
  const addSection = () => {
    if (newSection.trim()) {
      setSections([...sections, newSection.trim()]);
      setNewSection("");
    }
  };

  // Remove a section
  const removeSection = (index) => {
    setSections(sections.filter((_, i) => i !== index));
  };

  // Move section up
  const moveUp = (index) => {
    if (index === 0) return;
    const arr = [...sections];
    [arr[index - 1], arr[index]] = [arr[index], arr[index - 1]];
    setSections(arr);
  };

  // AI Suggest Outline (Bonus Feature)
  const suggestOutline = async () => {
    if (!topic.trim()) {
      alert("Please enter a topic first");
      return;
    }
    setSuggesting(true);
    try {
      const res = await api.post("/ai/suggest-outline", { topic, doc_type: docType });
      setSections(res.data.titles);
    } catch (err) {
      alert("Failed to suggest outline. Please try again.");
    } finally {
      setSuggesting(false);
    }
  };

  // Create the project
  const handleCreate = async () => {
    if (!title.trim() || !topic.trim() || sections.length === 0) {
      alert("Please fill all fields and add at least one section.");
      return;
    }
    setLoading(true);
    try {
      const res = await api.post("/projects/", {
        title,
        doc_type: docType,
        topic,
        sections,
      });
      navigate(`/editor/${res.data.id}`);
    } catch (err) {
      alert("Failed to create project");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-blue-600">DocAI</h1>
        <button onClick={() => navigate("/dashboard")} className="text-gray-500 text-sm hover:text-gray-700">
          ← Back to Dashboard
        </button>
      </nav>

      <div className="max-w-2xl mx-auto px-6 py-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Create New Project</h2>

        {/* Step 1: Choose doc type */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-4">
          <h3 className="font-semibold text-gray-700 mb-3">1. Choose Document Type</h3>
          <div className="grid grid-cols-2 gap-3">
            {[
              { value: "docx", label: "📄 Word Document", desc: ".docx" },
              { value: "pptx", label: "📊 PowerPoint", desc: ".pptx" },
            ].map((opt) => (
              <button
                key={opt.value}
                onClick={() => setDocType(opt.value)}
                className={`p-4 rounded-lg border-2 text-left transition ${
                  docType === opt.value
                    ? "border-blue-500 bg-blue-50"
                    : "border-gray-200 hover:border-gray-300"
                }`}
              >
                <div className="font-semibold">{opt.label}</div>
                <div className="text-sm text-gray-500">{opt.desc}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Step 2: Title and Topic */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-4">
          <h3 className="font-semibold text-gray-700 mb-3">2. Project Details</h3>
          <div className="space-y-3">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Project Title</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g., EV Market Analysis 2025"
                className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Main Topic / Prompt</label>
              <textarea
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g., A comprehensive market analysis of the electric vehicle industry in 2025, focusing on growth trends and key players"
                rows={3}
                className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Step 3: Sections */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-6">
          <div className="flex justify-between items-center mb-3">
            <h3 className="font-semibold text-gray-700">
              3. {docType === "pptx" ? "Slide Titles" : "Section Headers"}
            </h3>
            <button
              onClick={suggestOutline}
              disabled={suggesting}
              className="text-sm bg-purple-50 text-purple-600 px-3 py-1 rounded-lg hover:bg-purple-100 transition disabled:opacity-50"
            >
              {suggesting ? "Generating..." : "✨ AI Suggest"}
            </button>
          </div>

          <div className="space-y-2 mb-3">
            {sections.map((s, i) => (
              <div key={i} className="flex items-center gap-2 bg-gray-50 rounded-lg px-3 py-2">
                <span className="text-gray-400 text-sm w-6">{i + 1}.</span>
                <span className="flex-1 text-gray-700">{s}</span>
                <button onClick={() => moveUp(i)} className="text-gray-400 hover:text-gray-600 text-sm px-1">
                  ↑
                </button>
                <button onClick={() => removeSection(i)} className="text-red-400 hover:text-red-600 text-sm px-1">
                  ✕
                </button>
              </div>
            ))}
          </div>

          <div className="flex gap-2">
            <input
              type="text"
              value={newSection}
              onChange={(e) => setNewSection(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && addSection()}
              placeholder="Add a new section title..."
              className="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={addSection}
              className="bg-gray-100 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition"
            >
              Add
            </button>
          </div>
        </div>

        <button
          onClick={handleCreate}
          disabled={loading}
          className="w-full bg-blue-600 text-white py-3 rounded-xl font-semibold text-lg hover:bg-blue-700 disabled:opacity-50 transition"
        >
          {loading ? "Creating..." : "Create Project & Generate Content →"}
        </button>
      </div>
    </div>
  );
}
```

---

### Step 9: src/components/SectionCard.jsx <a name="frontend-components"></a>

```jsx
// frontend/src/components/SectionCard.jsx
import { useState } from "react";
import api from "../api";

export default function SectionCard({ section, projectDocType, onUpdate }) {
  const [refinePrompt, setRefinePrompt] = useState("");
  const [comment, setComment] = useState(section.comment || "");
  const [loading, setLoading] = useState(false);
  const [isExpanded, setIsExpanded] = useState(true);

  const handleRefine = async () => {
    if (!refinePrompt.trim()) return;
    setLoading(true);
    try {
      const res = await api.post("/ai/refine", {
        section_id: section.id,
        prompt: refinePrompt,
      });
      onUpdate(res.data);
      setRefinePrompt("");
    } catch (err) {
      alert("Refinement failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (feedback) => {
    const newFeedback = section.feedback === feedback ? "none" : feedback;
    const res = await api.patch(`/projects/sections/${section.id}`, { feedback: newFeedback });
    onUpdate(res.data);
  };

  const handleCommentSave = async () => {
    const res = await api.patch(`/projects/sections/${section.id}`, { comment });
    onUpdate(res.data);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border overflow-hidden mb-4">
      {/* Header */}
      <div
        className="flex justify-between items-center p-4 cursor-pointer hover:bg-gray-50"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center gap-3">
          <span className="text-blue-600 font-bold text-sm bg-blue-50 px-2 py-1 rounded">
            {projectDocType === "pptx" ? "Slide" : "Section"}
          </span>
          <h3 className="font-semibold text-gray-800">{section.title}</h3>
        </div>
        <div className="flex items-center gap-2">
          {section.feedback === "liked" && <span className="text-green-500">👍</span>}
          {section.feedback === "disliked" && <span className="text-red-500">👎</span>}
          <span className="text-gray-400 text-sm">{isExpanded ? "▲" : "▼"}</span>
        </div>
      </div>

      {isExpanded && (
        <div className="px-4 pb-4 space-y-4">
          {/* Content Display */}
          <div className="bg-gray-50 rounded-lg p-4 min-h-20">
            {section.content ? (
              <p className="text-gray-700 whitespace-pre-wrap text-sm leading-relaxed">
                {section.content}
              </p>
            ) : (
              <p className="text-gray-400 italic text-sm">No content yet. Generate content from the top.</p>
            )}
          </div>

          {/* Feedback Buttons */}
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-500">Feedback:</span>
            <button
              onClick={() => handleFeedback("liked")}
              className={`px-3 py-1 rounded-lg text-sm transition ${
                section.feedback === "liked"
                  ? "bg-green-100 text-green-600 font-medium"
                  : "bg-gray-100 text-gray-500 hover:bg-green-50"
              }`}
            >
              👍 Like
            </button>
            <button
              onClick={() => handleFeedback("disliked")}
              className={`px-3 py-1 rounded-lg text-sm transition ${
                section.feedback === "disliked"
                  ? "bg-red-100 text-red-600 font-medium"
                  : "bg-gray-100 text-gray-500 hover:bg-red-50"
              }`}
            >
              👎 Dislike
            </button>
            {section.revision_history?.length > 0 && (
              <span className="text-xs text-gray-400">
                {section.revision_history.length} revision(s)
              </span>
            )}
          </div>

          {/* AI Refine Prompt */}
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">
              ✨ Refine with AI
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={refinePrompt}
                onChange={(e) => setRefinePrompt(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && !loading && handleRefine()}
                placeholder='e.g., "Make this more formal" or "Convert to bullet points"'
                className="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                onClick={handleRefine}
                disabled={loading || !refinePrompt.trim()}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 transition"
              >
                {loading ? "..." : "Refine"}
              </button>
            </div>
          </div>

          {/* Comment Box */}
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">
              💬 Notes / Comments
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Add a note about this section..."
                className="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                onClick={handleCommentSave}
                className="bg-gray-100 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

---

### Step 10: src/pages/EditorPage.jsx

```jsx
// frontend/src/pages/EditorPage.jsx
import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";
import SectionCard from "../components/SectionCard";

export default function EditorPage() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [sections, setSections] = useState([]);
  const [generating, setGenerating] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProject();
  }, [projectId]);

  const fetchProject = async () => {
    try {
      const res = await api.get(`/projects/${projectId}`);
      setProject(res.data);
      setSections(res.data.sections.sort((a, b) => a.order_index - b.order_index));
    } catch (err) {
      alert("Failed to load project");
      navigate("/dashboard");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAll = async () => {
    const hasContent = sections.some((s) => s.content);
    if (hasContent && !confirm("Regenerate all content? This will overwrite existing content.")) {
      return;
    }
    setGenerating(true);
    try {
      await api.post(`/ai/generate/${projectId}`);
      await fetchProject(); // Reload with new content
    } catch (err) {
      alert("Generation failed. Check your API key.");
    } finally {
      setGenerating(false);
    }
  };

  const handleExport = async () => {
    setExporting(true);
    try {
      const res = await api.get(`/export/${projectId}`, {
        responseType: "blob", // Important: tells axios to handle binary data
      });
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        `${project.title.replace(/\s+/g, "_")}.${project.doc_type}`
      );
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      alert("Export failed");
    } finally {
      setExporting(false);
    }
  };

  // Update a section in our local state after refinement
  const updateSection = (updatedSection) => {
    setSections((prev) =>
      prev.map((s) => (s.id === updatedSection.id ? updatedSection : s))
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Loading project...</p>
      </div>
    );
  }

  const allHaveContent = sections.every((s) => s.content);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Bar */}
      <nav className="bg-white border-b px-6 py-4 flex justify-between items-center sticky top-0 z-10">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate("/dashboard")}
            className="text-gray-400 hover:text-gray-600 text-sm"
          >
            ← Dashboard
          </button>
          <div>
            <h1 className="font-bold text-gray-800">{project?.title}</h1>
            <p className="text-xs text-gray-400">
              {project?.doc_type === "docx" ? "📄 Word Document" : "📊 PowerPoint"} · {sections.length} sections
            </p>
          </div>
        </div>
        <div className="flex gap-3">
          <button
            onClick={handleGenerateAll}
            disabled={generating}
            className="bg-purple-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-purple-700 disabled:opacity-50 transition"
          >
            {generating ? "⏳ Generating..." : "✨ Generate All Content"}
          </button>
          {allHaveContent && (
            <button
              onClick={handleExport}
              disabled={exporting}
              className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50 transition"
            >
              {exporting ? "Preparing..." : `⬇️ Export .${project?.doc_type}`}
            </button>
          )}
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-3xl mx-auto px-6 py-8">
        {!allHaveContent && (
          <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6 text-center">
            <p className="text-blue-700 text-sm">
              Click <strong>✨ Generate All Content</strong> to have AI write content for each section.
            </p>
          </div>
        )}

        {sections.map((section) => (
          <SectionCard
            key={section.id}
            section={section}
            projectDocType={project?.doc_type}
            onUpdate={updateSection}
          />
        ))}
      </div>
    </div>
  );
}
```

---

### Step 11: src/App.jsx — Routing

```jsx
// frontend/src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";

import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";
import ConfigurePage from "./pages/ConfigurePage";
import EditorPage from "./pages/EditorPage";

// Protects routes that require login
function ProtectedRoute({ children }) {
  const { isLoggedIn } = useAuth();
  return isLoggedIn ? children : <Navigate to="/login" />;
}

function AppRoutes() {
  const { isLoggedIn } = useAuth();

  return (
    <Routes>
      <Route path="/login" element={isLoggedIn ? <Navigate to="/dashboard" /> : <LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/dashboard"
        element={<ProtectedRoute><DashboardPage /></ProtectedRoute>}
      />
      <Route
        path="/configure"
        element={<ProtectedRoute><ConfigurePage /></ProtectedRoute>}
      />
      <Route
        path="/editor/:projectId"
        element={<ProtectedRoute><EditorPage /></ProtectedRoute>}
      />
      <Route path="*" element={<Navigate to={isLoggedIn ? "/dashboard" : "/login"} />} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}
```

---

### Step 12: Update frontend/src/main.jsx

```jsx
// frontend/src/main.jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

---

## 8. Environment Variables <a name="environment-variables"></a>

### backend/.env
```env
SECRET_KEY=make-this-very-long-and-random-like-abc123xyz789...
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```

### frontend/.env.local (optional, for deployment)
```env
VITE_API_URL=http://localhost:8000
```

---

## 9. Running the Project <a name="running-the-project"></a>

### Terminal 1 — Backend
```bash
cd ai-doc-platform/backend
source venv/bin/activate    # Mac/Linux
# venv\Scripts\activate     # Windows
uvicorn main:app --reload
```
Backend runs at: http://localhost:8000
API docs at: http://localhost:8000/docs

### Terminal 2 — Frontend
```bash
cd ai-doc-platform/frontend
npm run dev
```
Frontend runs at: http://localhost:5173

### Push to GitHub
```bash
cd ai-doc-platform
git add .
git commit -m "Initial project setup"
git push origin main
```

---

## 10. README.md Template

Replace your README.md with this:

```markdown
# AI-Assisted Document Authoring Platform

A full-stack web application for generating and exporting AI-powered business documents.

## Tech Stack
- **Backend**: FastAPI + SQLite + SQLAlchemy
- **Frontend**: React + Vite + Tailwind CSS
- **AI**: Anthropic Claude API
- **Export**: python-docx + python-pptx

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- Anthropic API key (https://console.anthropic.com)

### Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

Create backend/.env:
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ANTHROPIC_API_KEY=your-anthropic-key

Run backend:
uvicorn main:app --reload

### Frontend Setup
cd frontend
npm install
npm run dev

## Usage
1. Open http://localhost:5173
2. Register a new account
3. Click "+ New Project"
4. Choose Word or PowerPoint, enter a topic
5. Use "AI Suggest" or manually add section titles
6. Click "Create Project"
7. On the editor page, click "Generate All Content"
8. Refine individual sections using the AI prompt box
9. Like/dislike sections, add comments
10. Click "Export" to download your .docx or .pptx file
```

---

## 11. Useful Links <a name="useful-links"></a>

| Topic | Link |
|-------|------|
| FastAPI docs | https://fastapi.tiangolo.com |
| FastAPI tutorial | https://fastapi.tiangolo.com/tutorial/ |
| SQLAlchemy docs | https://docs.sqlalchemy.org |
| React docs | https://react.dev |
| React Router | https://reactrouter.com/en/main |
| Tailwind CSS | https://tailwindcss.com/docs |
| Anthropic API docs | https://docs.anthropic.com |
| python-docx docs | https://python-docx.readthedocs.io |
| python-pptx docs | https://python-pptx.readthedocs.io |
| JWT explained | https://jwt.io/introduction |
| Axios docs | https://axios-http.com/docs/intro |

---

## 🎯 Build Order Summary (Do in this exact order)

```
1. ✅ Install Python, Node, Git
2. ✅ Create GitHub repo + clone
3. ✅ Create backend/ folder + venv + install packages
4. ✅ Create: database.py → models.py → schemas.py → auth.py
5. ✅ Create routes/: auth_routes.py → project_routes.py → ai_routes.py → export_routes.py
6. ✅ Create services/: ai_service.py → docx_service.py → pptx_service.py
7. ✅ Create main.py → test at localhost:8000/docs
8. ✅ Create frontend with Vite + install packages
9. ✅ Create: api.js → AuthContext.jsx
10. ✅ Create pages: LoginPage → RegisterPage → DashboardPage → ConfigurePage → EditorPage
11. ✅ Create components: SectionCard.jsx
12. ✅ Update App.jsx + main.jsx
13. ✅ Create .env files
14. ✅ Run both servers + test end to end
15. ✅ Push to GitHub + record demo video
```

---

## 🐛 Common Issues & Fixes

**"CORS error" in browser console**
→ Your frontend URL must be in `allow_origins` in `main.py`. Add `http://localhost:5173`.

**"401 Unauthorized" on API calls**
→ Token not being sent. Check `api.js` interceptor is reading from localStorage.

**"ModuleNotFoundError" in Python**
→ Make sure venv is activated (`source venv/bin/activate`).

**"Cannot find module" in React**
→ Run `npm install` in the frontend/ folder.

**AI returns garbled JSON for suggest-outline**
→ The `suggest_outline` function in `ai_service.py` strips markdown code fences. If it still fails, add a `print(raw)` before `json.loads()` to debug.

**Export download doesn't start**
→ Make sure `responseType: "blob"` is in the axios call in EditorPage.jsx.
```
