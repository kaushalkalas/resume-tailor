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
        """Extract a section despite markdown, spacing, or code fences."""
        section_names = [
            "BULLET IMPROVEMENTS",
            "MISSING KEYWORDS",
            "SUMMARY SUGGESTION",
            "SKILLS SUGGESTIONS",
            "ATS SCORE",
        ]
        header_pattern = re.compile(
            r"^\s*(?:#{1,6}\s*)?(?:\*\*|__|`)?(?:---\s*)?("
            + "|".join(re.escape(name) for name in section_names)
            + r")(?:\s*(?:---|#{1,6}))?(?:\*\*|__|`)?\s*$",
            re.IGNORECASE | re.MULTILINE,
        )
        headers = list(header_pattern.finditer(text))
        wanted = section_name.casefold()
        for index, header in enumerate(headers):
            if header.group(1).casefold() == wanted:
                end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
                return text[header.end():end].strip().strip("`").strip()
        return ""
    
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
    
    label_pattern = re.compile(
        r"^\s*(?:[-*]\s*)?(?:\*\*|__|`)?(original|improved|reason)"
        r"(?:\*\*|__|`)?\s*:\s*(.*)$",
        re.IGNORECASE,
    )
    current_bullet = None
    current_field = "improved"

    for line in text.split("\n"):
        line = line.strip().strip("`").strip()
        if not line:
            continue

        match = label_pattern.match(line)
        if match and match.group(1).casefold() == "original":
            if current_bullet and current_bullet["original"] and current_bullet["improved"]:
                bullets.append(current_bullet)
            current_bullet = {"original": match.group(2).strip(" *_`"), "improved": "", "reason": ""}
            current_field = "original"
            continue

        if current_bullet is None:
            continue

        if match:
            current_field = match.group(1).casefold()
            current_bullet[current_field] = match.group(2).strip(" *_`")
        else:
            current_bullet[current_field] = (current_bullet[current_field] + " " + line.strip(" *_`")) .strip()

    if current_bullet and current_bullet["original"] and current_bullet["improved"]:
        bullets.append(current_bullet)

    return bullets


def _parse_comma_values(text, label):
    """Parse a comma-separated field with optional markdown formatting."""
    pattern = re.compile(
        rf"^\s*(?:[-*]\s*)?(?:\*\*|__|`)?{re.escape(label)}"
        rf"(?:\*\*|__|`)?\s*:\s*(.*)$",
        re.IGNORECASE,
    )
    for line in text.split("\n"):
        match = pattern.match(line.strip())
        if match:
            return [item.strip(" -*`") for item in match.group(1).split(",") if item.strip(" -*`")]
    return []


def parse_keywords(text):
    """Parse missing keywords section."""
    return {
        "must_add": _parse_comma_values(text, "must add"),
        "nice_to_add": _parse_comma_values(text, "nice to add"),
    }


def parse_summary(text):
    """Parse summary suggestion section."""
    summary = {"current": "", "suggested": ""}
    label_pattern = re.compile(
        r"^\s*(?:[-*]\s*)?(?:\*\*|__|`)?(current|suggested)"
        r"(?:\*\*|__|`)?\s*:\s*(.*)$",
        re.IGNORECASE,
    )
    current = None
    for line in text.split("\n"):
        line = line.strip().strip("`").strip()
        if not line:
            continue
        match = label_pattern.match(line)
        if match:
            current = match.group(1).casefold()
            summary[current] = match.group(2).strip()
        elif current:
            summary[current] = (summary[current] + " " + line).strip()
    summary["current"] = re.sub(r"\s+", " ", summary["current"])
    summary["suggested"] = re.sub(r"\s+", " ", summary["suggested"])
    return summary


def parse_skills(text):
    """Parse skills suggestions section."""
    return {
        "add": _parse_comma_values(text, "add"),
        "remove": _parse_comma_values(text, "remove"),
    }


def parse_ats_score(text):
    """Parse and normalize the ATS score section."""
    score = {"percentage": "0", "reason": ""}
    score_match = re.search(
        r"(?:score|percentage)[^0-9\n]{0,12}(\d{1,3})\s*%?",
        text,
        re.IGNORECASE,
    )
    if score_match:
        score["percentage"] = str(max(0, min(100, int(score_match.group(1)))))

    reason_match = re.search(r"reason\s*:\s*(.+)", text, re.IGNORECASE)
    if reason_match:
        score["reason"] = reason_match.group(1).strip().strip("`*")
    return score
