
import re
from schemas import JobDescription, Resume


# Different names that can refer to the same skill.
SKILL_ALIASES = {
    "js": "javascript",
    "javascript": "javascript",
    "node": "node.js",
    "nodejs": "node.js",
    "node.js": "node.js",
    "reactjs": "react",
    "react.js": "react",
    "amazon web services": "aws",
    "c plus plus": "c++",
    "cpp": "c++",
    "c++": "c++",
    "structured query language": "sql",
    "dsa": "data structures and algorithms",
}


def normalize_skill(skill: str) -> str:
    """Convert skill names into a consistent format."""
    cleaned = re.sub(r"\s+", " ", skill.strip().lower())
    return SKILL_ALIASES.get(cleaned, cleaned)


def match_skills(required_skills: list[str], candidate_skills: list[str]):
    """Find skills that are present and missing."""
    required = {normalize_skill(skill) for skill in required_skills}
    candidate = {normalize_skill(skill) for skill in candidate_skills}

    matched = sorted(required & candidate)
    missing = sorted(required - candidate)

    return matched, missing


def calculate_skill_score(required_skills: list[str],
                          candidate_skills: list[str]):
    """Calculate the percentage of required skills matched."""
    matched, missing = match_skills(required_skills, candidate_skills)

    if not required_skills:
        return None, matched, missing

    score = (len(matched) / len({
        normalize_skill(skill) for skill in required_skills
    })) * 100

    return round(score, 2), matched, missing


def calculate_experience_score(required_years, candidate_years):
    """Compare candidate experience with the stated minimum."""
    if required_years is None or required_years <= 0:
        return None, "No minimum experience requirement to assess."

    if candidate_years is None:
        return None, "Candidate experience is not available."

    score = min(candidate_years / required_years, 1) * 100

    if candidate_years >= required_years:
        note = "Candidate meets or exceeds the stated minimum."
    else:
        note = "Candidate has less experience than the stated minimum."

    return round(score, 2), note


def calculate_education_score(requirements, candidate_education):
    """
    Use simple text matching as an initial indicator.
    This is not a substitute for manual qualification review.
    """
    if not requirements:
        return None, "No education requirement to assess."

    if not candidate_education:
        return None, "Candidate education information is unavailable."

    requirement_text = " ".join(requirements).lower()
    education_text = " ".join(candidate_education).lower()

    # Remove punctuation to make basic phrase comparisons easier.
    requirement_text = re.sub(r"[^a-z0-9 ]", " ", requirement_text)
    education_text = re.sub(r"[^a-z0-9 ]", " ", education_text)

    requirement_words = set(requirement_text.split())
    education_words = set(education_text.split())

    # Ignore common words that do not indicate a qualification.
    common_words = {
        "in", "of", "and", "or", "a", "an", "the", "degree",
        "required", "preferred", "field", "related", "equivalent"
    }

    meaningful_words = requirement_words - common_words

    if not meaningful_words:
        return None, "Education requirement needs manual review."

    overlap = meaningful_words & education_words
    similarity = len(overlap) / len(meaningful_words)

    if similarity >= 0.7:
        return 100.0, "Education text appears to match; verify manually."

    return 0.0, "Education text does not clearly match; verify manually."


def match_candidate(job: JobDescription, resume: Resume) -> dict:
    """Compare one candidate's resume with one job description."""

    required_score, matched_required, missing_required = (
        calculate_skill_score(job.required_skills, resume.skills)
    )

    preferred_score, matched_preferred, missing_preferred = (
        calculate_skill_score(job.preferred_skills, resume.skills)
    )

    experience_score, experience_note = calculate_experience_score(
        job.minimum_experience,
        resume.total_experience_years
    )

    education_score, education_note = calculate_education_score(
        job.education_requirements,
        resume.education
    )

    # Only assess dimensions for which we have usable information.
    # The active weights are automatically rescaled to total 100%.
    weights = {
        "required_skills": (required_score, 60),
        "preferred_skills": (preferred_score, 15),
        "experience": (experience_score, 15),
        "education": (education_score, 10),
    }

    active_dimensions = {
        name: (score, weight)
        for name, (score, weight) in weights.items()
        if score is not None
    }

    if not active_dimensions:
        overall_score = None
    else:
        total_weight = sum(weight for score, weight in active_dimensions.values())
        weighted_score = sum(
            score * weight
            for score, weight in active_dimensions.values()
        )
        overall_score = round(weighted_score / total_weight, 2)

    if overall_score is None:
        recommendation = "Insufficient information"
    elif overall_score >= 75:
        recommendation = "Strong alignment"
    elif overall_score >= 50:
        recommendation = "Partial alignment"
    else:
        recommendation = "Low alignment"

    return {
        "candidate_name": resume.name,
        "job_role": job.role,
        "overall_score": overall_score,
        "required_skill_score": required_score,
        "preferred_skill_score": preferred_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "matched_required_skills": matched_required,
        "missing_required_skills": missing_required,
        "matched_preferred_skills": matched_preferred,
        "missing_preferred_skills": missing_preferred,
        "experience_note": experience_note,
        "education_note": education_note,
        "recommendation": recommendation,
    }
