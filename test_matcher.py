
import json
from pathlib import Path

from schemas import JobDescription, Resume
from services.matcher import match_candidate


# Load the job description analysis.
job_path = Path("output/job_analysis.json")
with open(job_path, "r", encoding="utf-8") as file:
    job_data = json.load(file)

# Load the parsed resume.
resume_path = Path("output/parsed_resume.json")
with open(resume_path, "r", encoding="utf-8") as file:
    resume_data = json.load(file)


# Convert dictionaries into validated Pydantic objects.
job = JobDescription.model_validate(job_data)
resume = Resume.model_validate(resume_data)


# Compare the resume with the job.
result = match_candidate(job, resume)

print("\n========== RESUME MATCH REPORT ==========")
print("Candidate:", result["candidate_name"])
print("Job role:", result["job_role"])
print("JD alignment score:", result["overall_score"])
print("Recommendation:", result["recommendation"])

print("\n--- Skill Analysis ---")
print("Required skill score:", result["required_skill_score"])
print("Matched required skills:", result["matched_required_skills"])
print("Missing required skills:", result["missing_required_skills"])

print("\nPreferred skill score:", result["preferred_skill_score"])
print("Matched preferred skills:", result["matched_preferred_skills"])
print("Missing preferred skills:", result["missing_preferred_skills"])

print("\n--- Other Criteria ---")
print("Experience score:", result["experience_score"])
print("Experience note:", result["experience_note"])
print("Education score:", result["education_score"])
print("Education note:", result["education_note"])


# Save the result as JSON.
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

output_path = output_dir / "match_report.json"

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(result, file, indent=4)

print("\nReport saved to:", output_path)
