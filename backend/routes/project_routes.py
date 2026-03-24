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
