
from pathlib import Path

from utils.document_reader import calculate_file_hash

resume_path = Path("resumes/Latest_Resume.pdf")

file_hash = calculate_file_hash(resume_path)

print("Resume:", resume_path.name)

print("SHA-256:", file_hash)