
import csv
import json
from pathlib import Path

from schemas import JobDescription
from utils.document_reader import read_resume
from services.resume_parser import parse_resume
from services.matcher import match_candidate


def screen_multiple_resumes(
    job: JobDescription,
    resume_folder: Path
) -> list[dict]:

    results = []

    # Find all PDF and DOCX files in the folder.
    resume_files = [
        *resume_folder.glob("*.pdf"),
        *resume_folder.glob("*.docx")
    ]

    if not resume_files:
        raise ValueError("No PDF or DOCX resumes found in the resumes folder.")

    print(f"\nFound {len(resume_files)} resumes.")

    for index, resume_file in enumerate(resume_files, start=1):

        print(
            f"\nProcessing resume {index}/{len(resume_files)}: "
            f"{resume_file.name}"
        )

        try:
            # Step 1: Extract text from the document.
            resume_text = read_resume(resume_file)

            # Step 2: Extract candidate information using Groq.
            candidate = parse_resume(resume_text)

            # Step 3: Compare candidate with the job description.
            result = match_candidate(job, candidate)

            # Add the original filename to the report.
            result["source_file"] = resume_file.name

            results.append(result)

            print(
                f"Completed: {resume_file.name} | "
                f"Score: {result['overall_score']}"
            )

        except Exception as error:
            # One bad resume should not stop the entire batch.
            print(f"Failed: {resume_file.name} | Error: {error}")

            results.append({
                "source_file": resume_file.name,
                "candidate_name": None,
                "job_role": job.role,
                "overall_score": None,
                "recommendation": "Processing failed",
                "error": str(error)
            })

    # Sort by score, highest first.
    # Resumes with no score or processing errors go to the bottom.
    results.sort(
        key=lambda item: (
            item.get("overall_score") is None,
            -(item.get("overall_score") or 0)
        )
    )

    return results


def save_batch_reports(results: list[dict], output_folder: Path):

    output_folder.mkdir(parents=True, exist_ok=True)

    # Save the complete results as JSON.
    json_path = output_folder / "batch_screening_results.json"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    # Save a shorter summary as CSV.
    csv_path = output_folder / "batch_screening_results.csv"

    csv_columns = [
        "source_file",
        "candidate_name",
        "job_role",
        "overall_score",
        "recommendation",
        "matched_required_skills",
        "missing_required_skills",
        "error"
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()

        for result in results:
            row = result.copy()

            # Convert lists into readable text for CSV.
            for column in [
                "matched_required_skills",
                "missing_required_skills"
            ]:
                if isinstance(row.get(column), list):
                    row[column] = ", ".join(row[column])

            writer.writerow({
                column: row.get(column, "")
                for column in csv_columns
            })

    print("\nBatch reports saved:")
    print(json_path)
    print(csv_path)
