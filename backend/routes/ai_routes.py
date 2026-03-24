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
    try:
        project = db.query(models.Project).filter(
            models.Project.id == project_id,
            models.Project.owner_id == current_user.id
        ).first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Generate content for each section (Groq has high rate limits, no delay needed)
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
    except HTTPException:
        raise
    except Exception as e:
        print(f"[AI Routes] Error generating content: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


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
