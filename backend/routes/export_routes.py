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
