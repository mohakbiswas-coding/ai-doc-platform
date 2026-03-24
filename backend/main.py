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
