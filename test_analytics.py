
import json
from pathlib import Path

from services.report_generator import (
    generate_analytics,
    save_analytics,
    generate_text_report
)


# Step 1: Load batch screening results.
input_path = Path("output/batch_screening_results.json")

with open(input_path, "r", encoding="utf-8") as file:
    results = json.load(file)


# Step 2: Generate analytics.
analytics = generate_analytics(results)


# Step 3: Display analytics.
print("\n========== SCREENING ANALYTICS ==========")

print("Total candidates:", analytics["total_candidates"])

print(
    "Successfully processed:",
    analytics["successfully_processed"]
)

print("Failed candidates:", analytics["failed_candidates"])

print("Average score:", analytics["average_score"])

print("\nTop candidate:")
print(analytics["top_candidate"])

print("\nRecommendation distribution:")
print(analytics["recommendation_distribution"])

print("\nMost matched skills:")
print(analytics["most_matched_skills"])

print("\nMost missing skills:")
print(analytics["most_missing_skills"])


# Step 4: Save reports.
output_folder = Path("output")

save_analytics(analytics, output_folder)

generate_text_report(analytics, output_folder)
