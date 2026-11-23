
from pathlib import Path

from utils.document_reader import read_resume
from services.resume_parser import parse_resume


# STEP 1: Select a resume

resume_path = Path("resumes/Latest_Resume.pdf")


try:

    # STEP 2: Extract text from document

    print("Reading resume...")

    resume_text = read_resume(resume_path)


    # STEP 3: Send text to AI parser

    print("Analysing resume using Groq...")

    candidate = parse_resume(resume_text)


    # STEP 4: Display candidate information

    print("\n========== CANDIDATE PROFILE ==========")

    print("\nName:")
    print(candidate.name)

    print("\nEmail:")
    print(candidate.email)

    print("\nPhone:")
    print(candidate.phone)

    print("\nTotal Experience:")
    print(candidate.total_experience_years)


    print("\nTechnical Skills:")

    for skill in candidate.skills:
        print("-", skill)


    print("\nEducation:")

    for education in candidate.education:
        print("-", education)


    print("\nExperience:")

    for experience in candidate.experiences:

        print("\nCompany:", experience.company)

        print("Role:", experience.role)

        print("Duration:", experience.duration)

        print("Skills:", experience.skills_used)

        print("Description:", experience.description)


    print("\nProjects:")

    for project in candidate.projects:
        print("-", project)


    print("\nCertifications:")

    for certificate in candidate.certifications:
        print("-", certificate)


    # STEP 5: Save parsed resume as JSON

    output_path = Path("output/parsed_resume.json")

    output_path.parent.mkdir(exist_ok=True)

    output_path.write_text(
        candidate.model_dump_json(indent=4),
        encoding="utf-8"
    )

    print("\nResume parsing completed successfully!")


except Exception as error:

    print("\nResume parsing failed:", error)
