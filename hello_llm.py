
from pathlib import Path

from utils.document_reader import read_resume


# Path of the sample resume
resume_path = Path("resumes/Latest_Resume.pdf")


try:

    # Read the resume
    resume_text = read_resume(resume_path)

    # Print extracted text
    print("\n========== EXTRACTED RESUME ==========")

    print(resume_text)

    # Display some basic information
    print("\n========== DOCUMENT INFORMATION ==========")

    print("File name:", resume_path.name)

    print("Total characters:", len(resume_text))

    print("Total words:", len(resume_text.split()))


except Exception as error:

    print("Error reading resume:", error)
