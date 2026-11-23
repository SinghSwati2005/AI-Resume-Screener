
from pydantic import BaseModel, Field


# 1. Job Description Schema
class JobDescription(BaseModel):

    role: str = ""

    required_skills: list[str] = Field(default_factory=list)

    preferred_skills: list[str] = Field(default_factory=list)

    minimum_experience: float | None = None

    education_requirements: list[str] = Field(default_factory=list)

    responsibilities: list[str] = Field(default_factory=list)


# 2. Candidate Experience Schema
class Experience(BaseModel):

    company: str | None = None

    role: str | None = None

    duration: str | None = None

    description: str | None = None

    skills_used: list[str] = Field(default_factory=list)


# 3. Resume Schema
class Resume(BaseModel):

    name: str | None = None

    email: str | None = None

    phone: str | None = None

    total_experience_years: float | None = None

    skills: list[str] = Field(default_factory=list)

    experiences: list[Experience] = Field(default_factory=list)

    education: list[str] = Field(default_factory=list)

    projects: list[str] = Field(default_factory=list)

    certifications: list[str] = Field(default_factory=list)
