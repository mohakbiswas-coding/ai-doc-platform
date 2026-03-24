# backend/services/ai_service.py

import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

# Groq API configuration (much higher free tier rate limits!)
API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

print(f"[AI Service] Using Groq with model: {MODEL}")
print(f"[AI Service] Groq API Key present: {bool(API_KEY)}")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not set in .env file!")


def _call_groq(messages: list, retry_count: int = 0, max_retries: int = 2) -> str:
    """
    Call Groq API with automatic retry on rate limit.
    Groq has much higher free tier limits (500+ req/min).
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7,
    }
    
    try:
        print(f"[AI Service] Making request to Groq with model: {MODEL}")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        # Check for rate limit (429) - retry with backoff
        if response.status_code == 429:
            if retry_count < max_retries:
                wait_time = (2 ** retry_count) + 1
                print(f"[AI Service] Rate limited. Retrying in {wait_time} seconds... (attempt {retry_count + 1}/{max_retries})")
                time.sleep(wait_time)
                return _call_groq(messages, retry_count + 1, max_retries)
            else:
                raise Exception("Rate limited by Groq. Please wait a moment and try again.")
        
        # Check for other errors
        if response.status_code != 200:
            print(f"[AI Service] HTTP Error {response.status_code}")
            print(f"[AI Service] Response: {response.text[:500]}")
            
            if response.status_code == 401:
                raise Exception("Invalid Groq API key. Check your GROQ_API_KEY in .env file.")
            else:
                raise Exception(f"Groq API error: {response.status_code} - {response.text[:200]}")
        
        # Parse response
        data = response.json()
        
        if "error" in data:
            error_msg = data["error"].get("message", str(data["error"]))
            print(f"[AI Service] API returned error: {error_msg}")
            raise Exception(f"Groq error: {error_msg}")
        
        if "choices" not in data or len(data["choices"]) == 0:
            print(f"[AI Service] No choices in response: {data}")
            raise Exception("Groq returned no content")
        
        content = data["choices"][0]["message"]["content"]
        print(f"[AI Service] Got response: {len(content)} characters")
        return content
        
    except requests.exceptions.Timeout:
        raise Exception("Request to Groq timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        raise Exception("Failed to connect to Groq. Check your internet connection.")
    except json.JSONDecodeError as e:
        print(f"[AI Service] Failed to parse JSON response: {e}")
        raise Exception("Groq returned invalid JSON response")


def generate_section_content(topic: str, section_title: str, doc_type: str) -> str:
    """
    Generate AI content for one section of a document using Groq.

    topic: The main document topic
    section_title: The specific section
    doc_type: "docx" or "pptx"
    """
    if doc_type == "pptx":
        prompt = f"""You are creating content for a PowerPoint slide.

Document topic: {topic}
Slide title: {section_title}

Write concise bullet points for this slide (4-6 bullet points).
Each bullet point should be 1-2 sentences max.
Do NOT include the slide title in your response.
Start directly with the bullet points using "•" as the bullet character.

IMPORTANT: Do NOT include any thinking, reasoning, or explanatory text. Return ONLY the slide content, nothing else."""
    else:
        prompt = f"""You are writing a section of a business document.

Document topic: {topic}
Section title: {section_title}

Write 2-3 paragraphs of professional content for this section.
Do NOT include the section title in your response.
Write in a clear, professional business writing style.

IMPORTANT: Do NOT include any thinking, reasoning, or explanatory text before or after the content. Return ONLY the section content, nothing else."""

    try:
        print(f"[AI Service] Generating content for section: {section_title}")
        content = _call_groq([
            {"role": "user", "content": prompt}
        ])
        # Remove <think> tags and common thinking patterns
        content = content.replace("<think>", "").replace("</think>", "").strip()
        
        # Remove common thinking text patterns if they appear at the start
        thinking_patterns = [
            "Okay, ", "Let me ", "First, ", "Next, ", "I need to ", 
            "The user wants ", "I should ", "I'll ", "Alright, ",
            "So, the user "
        ]
        lines = content.split('\n')
        start_idx = 0
        
        # Skip lines that look like thinking text
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            if any(line_stripped.startswith(pattern) for pattern in thinking_patterns):
                if not any(char in line for char in ['•', '**', '-'] if char != '-'):
                    start_idx = i + 1
                else:
                    break
            elif line_stripped and not any(pattern in line for pattern in thinking_patterns):
                break
        
        content = '\n'.join(lines[start_idx:]).strip()
        
        print(f"[AI Service] Successfully generated content for: {section_title}")
        return content
    except Exception as e:
        print(f"[AI Service] Error generating content: {e}")
        raise


def refine_section_content(
    current_content: str,
    section_title: str,
    refinement_prompt: str,
    doc_type: str
) -> str:
    """
    Refine existing content based on user's instruction using Groq.
    """
    prompt = f"""You are editing a section of a {'PowerPoint slide' if doc_type == 'pptx' else 'business document'}.

Section title: {section_title}

Current content:
{current_content}

User's refinement request: {refinement_prompt}

Please rewrite the content according to the user's request.
Maintain the same format (bullet points for slides, paragraphs for documents).
Return ONLY the rewritten content, nothing else.

IMPORTANT: Do NOT include any thinking, reasoning, or explanatory text. Return ONLY the refined content."""

    try:
        print(f"[AI Service] Refining section: {section_title}")
        content = _call_groq([
            {"role": "user", "content": prompt}
        ])
        # Remove <think> tags and thinking text
        content = content.replace("<think>", "").replace("</think>", "").strip()
        
        # Remove thinking text patterns
        thinking_patterns = [
            "Okay, ", "Let me ", "First, ", "Next, ", "I need to ", 
            "The user wants ", "I should ", "I'll ", "Alright, ",
            "So, the user "
        ]
        lines = content.split('\n')
        start_idx = 0
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            if any(line_stripped.startswith(pattern) for pattern in thinking_patterns):
                if not any(char in line for char in ['•', '**', '-'] if char != '-'):
                    start_idx = i + 1
                else:
                    break
            elif line_stripped and not any(pattern in line for pattern in thinking_patterns):
                break
        
        content = '\n'.join(lines[start_idx:]).strip()
        
        print(f"[AI Service] Successfully refined: {section_title}")
        return content
    except Exception as e:
        print(f"[AI Service] Error refining content: {e}")
        raise


def suggest_outline(topic: str, doc_type: str) -> list:
    """
    Bonus feature: AI suggests section/slide titles for a topic using Groq.
    Returns a list of strings.
    """
    if doc_type == "pptx":
        prompt = f"""Suggest 8-10 slide titles for a PowerPoint presentation about: {topic}

Return ONLY the slide titles, one per line, without numbering.
Do NOT include any thinking, reasoning, or explanatory text."""
    else:
        prompt = f"""Suggest 8-10 section titles for a business document about: {topic}

Return ONLY the section titles, one per line, without numbering.
Do NOT include any thinking, reasoning, or explanatory text."""

    try:
        content = _call_groq([
            {"role": "user", "content": prompt}
        ])
        # Remove <think> tags and thinking text
        content = content.replace("<think>", "").replace("</think>", "").strip()
        
        # Remove thinking text patterns
        thinking_patterns = [
            "Okay, ", "Let me ", "First, ", "Next, ", "I need to ", 
            "The user wants ", "I should ", "I'll ", "Alright, ",
            "So, the user"
        ]
        lines = content.split('\n')
        filtered_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            # Skip lines that are clearly thinking text
            if any(line_stripped.startswith(pattern) for pattern in thinking_patterns):
                if not any(char in line for char in ['•', '**'] if char != '-'):
                    continue
            filtered_lines.append(line_stripped)
        
        return filtered_lines[:10]  # Return max 10
    except Exception as e:
        print(f"[AI Service] Error suggesting outline: {e}")
        raise
