"""
Response Parser Module
Parses AI response into structured format
"""
import re


def parse_ai_response(response_text):
    """
    Parse the raw AI response into a structured dictionary.
    
    Args:
        response_text (str): Raw response from AI
        
    Returns:
        dict: Structured response with sections
    """
    
    if not response_text or not response_text.strip():
        raise ValueError("Empty or invalid AI response")
    
    def extract_section(text, section_name):
        """Extract content between section headers."""
        pattern = rf"---{section_name}---\n(.*?)(?=---|\Z)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""
    
    bullet_improvements_text = extract_section(response_text, "BULLET IMPROVEMENTS")
    missing_keywords_text = extract_section(response_text, "MISSING KEYWORDS")
    summary_suggestion_text = extract_section(response_text, "SUMMARY SUGGESTION")
    skills_suggestion_text = extract_section(response_text, "SKILLS SUGGESTIONS")
    ats_score_text = extract_section(response_text, "ATS SCORE")
    
    bullet_improvements = parse_bullets(bullet_improvements_text)
    missing_keywords = parse_keywords(missing_keywords_text)
    summary_suggestion = parse_summary(summary_suggestion_text)
    skills_suggestion = parse_skills(skills_suggestion_text)
    ats_score = parse_ats_score(ats_score_text)
    
    return {
        "ats_score": ats_score,
        "bullet_improvements": bullet_improvements,
        "missing_keywords": missing_keywords,
        "summary_suggestion": summary_suggestion,
        "skills_suggestion": skills_suggestion
    }


def parse_bullets(text):
    """Parse bullet improvements section."""
    bullets = []
    
    if not text or not text.strip():
        return bullets
    
    parts = text.split("Original:")
    
    for part in parts[1:]:
        lines = part.strip().split("\n")
        
        original = ""
        improved = ""
        reason = ""
        
        current = "original"
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            lower_line = line.lower()
            
            if lower_line.startswith("improved:"):
                improved = line.split(":", 1)[1].strip() if ":" in line else ""
                current = "improved"
            elif lower_line.startswith("reason:"):
                reason = line.split(":", 1)[1].strip() if ":" in line else ""
                current = "reason"
            elif current == "improved" and not lower_line.startswith("reason:"):
                if improved:
                    improved += " " + line
                else:
                    improved = line
            elif current == "reason":
                if reason:
                    reason += " " + line
                else:
                    reason = line
            elif current == "original" and not lower_line.startswith("original:"):
                if original:
                    original += " " + line
                else:
                    original = line
        
        if original and improved:
            bullets.append({
                "original": original.strip(),
                "improved": improved.strip(),
                "reason": reason.strip() if reason else ""
            })
    
    return bullets


def parse_keywords(text):
    """Parse missing keywords section."""
    keywords = {
        "must_add": [],
        "nice_to_add": []
    }
    
    if not text or not text.strip():
        return keywords
    
    lines = text.split("\n")
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
        
        lower_line = line.lower()
        
        if lower_line.startswith("must add:"):
            keywords_str = line.split(":", 1)[1].strip()
            keywords["must_add"] = [k.strip() for k in keywords_str.split(",") if k.strip()]
        
        elif lower_line.startswith("nice to add:"):
            keywords_str = line.split(":", 1)[1].strip()
            keywords["nice_to_add"] = [k.strip() for k in keywords_str.split(",") if k.strip()]
    
    return keywords


def parse_summary(text):
    """Parse summary suggestion section."""
    summary = {
        "current": "",
        "suggested": ""
    }
    
    if not text or not text.strip():
        return summary
    
    lines = text.split("\n")
    
    current = ""
    suggested = ""
    parsing_current = False
    parsing_suggested = False
    
    for line in lines:
        line_stripped = line.strip()
        
        if not line_stripped:
            continue
        
        lower_line = line_stripped.lower()
        
        if lower_line.startswith("current:"):
            current = line.split(":", 1)[1].strip()
            parsing_current = True
            parsing_suggested = False
        elif lower_line.startswith("suggested:"):
            suggested = line.split(":", 1)[1].strip()
            parsing_suggested = True
            parsing_current = False
        elif parsing_current and not lower_line.startswith(("suggested:", "current:")):
            current += " " + line_stripped
        elif parsing_suggested and not lower_line.startswith(("current:", "suggested:")):
            suggested += " " + line_stripped
    
    summary["current"] = re.sub(r"\s+", " ", current).strip()
    summary["suggested"] = re.sub(r"\s+", " ", suggested).strip()
    
    return summary


def parse_skills(text):
    """Parse skills suggestions section."""
    skills = {
        "add": [],
        "remove": []
    }
    
    if not text or not text.strip():
        return skills
    
    lines = text.split("\n")
    
    for line in lines:
        line_stripped = line.strip()
        
        if not line_stripped:
            continue
        
        lower_line = line_stripped.lower()
        
        if lower_line.startswith("add:"):
            skills_str = line.split(":", 1)[1].strip()
            skills["add"] = [s.strip() for s in skills_str.split(",") if s.strip()]
        
        elif lower_line.startswith("remove:"):
            skills_str = line.split(":", 1)[1].strip()
            skills["remove"] = [s.strip() for s in skills_str.split(",") if s.strip()]
    
    return skills


def parse_ats_score(text):
    """Parse ATS score section."""
    score = {
        "percentage": "0",
        "reason": ""
    }
    
    lines = text.split("\n")
    
    for line in lines:
        line_lower = line.strip().lower()
        
        if line_lower.startswith("score:"):
            score_str = line.replace("Score:", "").replace("score:", "").strip()
            # Extract just the percentage number
            match = re.search(r"(\d+)", score_str)
            if match:
                score["percentage"] = match.group(1)
        
        elif line_lower.startswith("reason:"):
            score["reason"] = line.replace("Reason:", "").replace("reason:", "").strip()
    
    return score
