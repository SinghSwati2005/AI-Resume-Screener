
from pathlib import Path

from services.job_analyzer import analyze_job_description


# Step 1: Locate the job description file
job_file = Path("job_description.txt")


# Step 2: Read the file
job_text = job_file.read_text(encoding="utf-8")


# Step 3: Analyse the job description
job = analyze_job_description(job_text)


# Step 4: Display the extracted information
print("\n========== JOB ANALYSIS ==========")

print("\nJob Role:")
print(job.role)

print("\nRequired Skills:")
for skill in job.required_skills:
    print("-", skill)

print("\nPreferred Skills:")
for skill in job.preferred_skills:
    print("-", skill)

print("\nMinimum Experience:")
print(job.minimum_experience)

print("\nEducation Requirements:")
for education in job.education_requirements:
    print("-", education)

print("\nResponsibilities:")
for responsibility in job.responsibilities:
    print("-", responsibility)

# Step 5: Save structured output
output_file = Path("output/job_analysis.json")

output_file.parent.mkdir(exist_ok=True)

output_file.write_text(
    job.model_dump_json(indent=4),
    encoding="utf-8"
)

print("\nJob analysis saved successfully!")
