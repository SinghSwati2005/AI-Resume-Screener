
from collections import Counter
from pathlib import Path
import json


def generate_analytics(results: list[dict]) -> dict:

    # Separate successfully scored candidates.
    successful_results = [
        result for result in results
        if isinstance(result.get("overall_score"), (int, float))
    ]

    failed_results = [
        result for result in results
        if result.get("overall_score") is None
    ]

    total_candidates = len(results)
    successful_count = len(successful_results)

    # Calculate average score.
    if successful_count:
        average_score = round(
            sum(result["overall_score"] for result in successful_results)
            / successful_count,
            2
        )

        # Find the candidate with the highest score.
        top_candidate = max(
            successful_results,
            key=lambda result: result["overall_score"]
        )
    else:
        average_score = None
        top_candidate = None

    # Count candidate alignment categories.
    recommendation_counts = Counter(
        result.get("recommendation", "Unknown")
        for result in successful_results
    )

    # Count matched and missing skills across candidates.
    matched_skill_counts = Counter()
    missing_skill_counts = Counter()

    for result in successful_results:
        matched_skill_counts.update(
            result.get("matched_required_skills", [])
        )

        missing_skill_counts.update(
            result.get("missing_required_skills", [])
        )

    analytics = {
        "total_candidates": total_candidates,
        "successfully_processed": successful_count,
        "failed_candidates": len(failed_results),
        "average_score": average_score,

        "top_candidate": {
            "name": top_candidate.get("candidate_name"),
            "source_file": top_candidate.get("source_file"),
            "score": top_candidate.get("overall_score")
        } if top_candidate else None,

        "recommendation_distribution": dict(recommendation_counts),

        "most_matched_skills": matched_skill_counts.most_common(5),

        "most_missing_skills": missing_skill_counts.most_common(5)
    }

    return analytics


def save_analytics(analytics: dict, output_folder: Path):

    output_folder.mkdir(parents=True, exist_ok=True)

    output_path = output_folder / "analytics.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(analytics, file, indent=4)

    print(f"\nAnalytics saved to: {output_path}")


def generate_text_report(analytics: dict, output_folder: Path):

    output_folder.mkdir(parents=True, exist_ok=True)

    report_path = output_folder / "screening_report.txt"

    with open(report_path, "w", encoding="utf-8") as file:

        file.write("RESUME SCREENING ANALYTICS REPORT\n")
        file.write("=" * 40 + "\n\n")

        file.write(
            f"Total candidates: {analytics['total_candidates']}\n"
        )

        file.write(
            f"Successfully processed: "
            f"{analytics['successfully_processed']}\n"
        )

        file.write(
            f"Failed candidates: {analytics['failed_candidates']}\n"
        )

        file.write(
            f"Average alignment score: {analytics['average_score']}\n\n"
        )

        file.write("TOP CANDIDATE\n")
        file.write("-" * 40 + "\n")

        top = analytics["top_candidate"]

        if top:
            file.write(f"Name: {top['name']}\n")
            file.write(f"File: {top['source_file']}\n")
            file.write(f"Score: {top['score']}\n")
        else:
            file.write("No successfully scored candidates.\n")

        file.write("\nRECOMMENDATION DISTRIBUTION\n")
        file.write("-" * 40 + "\n")

        for label, count in analytics[
            "recommendation_distribution"
        ].items():
            file.write(f"{label}: {count}\n")

        file.write("\nMOST MATCHED REQUIRED SKILLS\n")
        file.write("-" * 40 + "\n")

        for skill, count in analytics["most_matched_skills"]:
            file.write(f"{skill}: {count}\n")

        file.write("\nMOST MISSING REQUIRED SKILLS\n")
        file.write("-" * 40 + "\n")

        for skill, count in analytics["most_missing_skills"]:
            file.write(f"{skill}: {count}\n")

    print(f"Text report saved to: {report_path}")
