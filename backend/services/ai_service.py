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
