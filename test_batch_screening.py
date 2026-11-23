
import json
from pathlib import Path

from schemas import JobDescription
from services.batch_screener import (
    screen_multiple_resumes,
    save_batch_reports
)


# Step 1: Load the analyzed job description.
job_path = Path("output/job_analysis.json")

with open(job_path, "r", encoding="utf-8") as file:
    job_data = json.load(file)

job = JobDescription.model_validate(job_data)


# Step 2: Screen all resumes.
resume_folder = Path("resumes")

results = screen_multiple_resumes(job, resume_folder)


# Step 3: Display the ranking.
print("\n========== CANDIDATE RANKING ==========")

for rank, result in enumerate(results, start=1):

    print(f"\nRank: {rank}")
    print("Candidate:", result.get("candidate_name"))
    print("File:", result.get("source_file"))
    print("Score:", result.get("overall_score"))
    print("Recommendation:", result.get("recommendation"))


# Step 4: Save JSON and CSV reports.
save_batch_reports(results, Path("output"))
