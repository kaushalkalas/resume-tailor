"""
AI Engine Module
Handles Groq API calls for resume analysis
"""
import os
import time
from groq import Groq, RateLimitError, APIError, APIConnectionError
from dotenv import load_dotenv

load_dotenv()

MAX_RETRIES = 3
RETRY_DELAY = 2


def get_ai_suggestions(resume_text, job_description):
    """
    Send resume and job description to Groq API for analysis.
    
    Args:
        resume_text (str): Content of the resume
        job_description (str): Job description to match against
        
    Returns:
        str: Raw AI response with suggestions
        
    Raises:
        Exception: If API call fails or API key is missing
    """
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. Please set it in your .env file.\n"
            "Get your free API key at: https://console.groq.com/"
        )
    
    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is empty")
    
    if not job_description or not job_description.strip():
        raise ValueError("Job description is empty")
    
    resume_truncated = truncate_text(resume_text, max_chars=8000)
    jd_truncated = truncate_text(job_description, max_chars=4000)
    
    try:
        client = Groq(api_key=api_key, timeout=60.0)
        
        prompt = f"""You are an expert ATS resume consultant with 10+ years of experience helping job seekers.

Your task is to analyze the resume and job description below, then provide specific, actionable suggestions.

IMPORTANT: Return your response in this EXACT format with these exact section headers:

---BULLET IMPROVEMENTS---
Original: <original bullet point>
Improved: <improved bullet point>
Reason: <brief explanation of improvement>
[Repeat for each bullet point - analyze at least 3 major bullets]

---MISSING KEYWORDS---
Must Add: <comma-separated technical keywords that are in JD but missing in resume>
Nice to Add: <comma-separated additional keywords that could strengthen the profile>

---SUMMARY SUGGESTION---
Current: <current professional summary/objective from resume>
Suggested: <improved professional summary tailored to the job>

---SKILLS SUGGESTIONS---
Add: <comma-separated skills missing from resume that are in JD>
Remove: <skills less relevant to this job role>

---ATS SCORE---
Score: <percentage>%
Reason: <one sentence explanation>

RULES:
- Do NOT fabricate or add fake experience
- Keep original job titles, companies, and dates
- Focus on rewording to match job description keywords
- Be specific, not generic
- Use action verbs and quantifiable metrics
- Only suggest additions if genuinely in the resume

RESUME:
{resume_truncated}

JOB DESCRIPTION:
{jd_truncated}"""
        
        last_error = None
        for attempt in range(MAX_RETRIES):
            try:
                message = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    max_tokens=2048,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                
                response = message.choices[0].message.content
                if not response or not response.strip():
                    raise ValueError("AI returned an empty response")
                
                return response
                
            except RateLimitError as e:
                last_error = e
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                    continue
                raise ValueError(f"API rate limit exceeded. Please wait a moment and try again.")
            
            except (APIConnectionError, APIError) as e:
                last_error = e
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                raise Exception(f"Error calling Groq API: {str(e)}")
            
            except ValueError:
                raise
            
            except Exception as e:
                raise Exception(f"Unexpected error: {str(e)}")
        
        if last_error:
            raise Exception(f"Failed after {MAX_RETRIES} attempts: {str(last_error)}")
    
    except ValueError:
        raise
    except Exception as e:
        raise Exception(f"Error calling Groq API: {str(e)}")


def truncate_text(text, max_chars):
    """Truncate text to max_chars while trying to preserve complete sentences."""
    if len(text) <= max_chars:
        return text
    
    truncated = text[:max_chars]
    last_period = truncated.rfind(".")
    
    if last_period > max_chars * 0.8:
        return truncated[:last_period + 1]
    
    last_newline = truncated.rfind("\n")
    if last_newline > max_chars * 0.8:
        return truncated[:last_newline]
    
    return truncated
