
from pathlib import Path

from pypdf import PdfReader
from docx import Document


# Path: handles file paths.
# PdfReader: opens PDF files.
# Document: opens DOCX files.


def read_pdf(file_path: Path) -> str:

    # Open the PDF document
    reader = PdfReader(str(file_path))

    # Store extracted text
    extracted_text = ""

    # Iterate through every page
    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if page_text:
            extracted_text += page_text + "\n"

    return extracted_text



def read_docx(file_path : Path)->str:

    #open the word doc
    document = Document(str(file_path))
    extracted_text=""

    #Extracted para

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            extracted_text+=paragraph.text+"\n"

            #extract tables
    for table in document.tables:
        for row in table.rows:
            for ceil in row.ceils:
                if ceil.text.strip():
                    extracted_text+=ceil.text+"\n"

    return extracted_text


def read_resume(file_path: Path) -> str:

    # Check whether the file exists
    if not file_path.exists():
        raise FileNotFoundError(
            f"Resume not found: {file_path}"
        )

    # Check whether it is actually a file
    if not file_path.is_file():
        raise ValueError("Provided path is not a file")

    # Check file extension
    extension = file_path.suffix.lower()

    # Read PDF
    if extension == ".pdf":
        extracted_text = read_pdf(file_path)

    # Read DOCX
    elif extension == ".docx":
        extracted_text = read_docx(file_path)

    else:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    # Check whether text was extracted
    if not extracted_text.strip():
        raise ValueError(
            "No readable text found in resume. "
            "It may be a scanned PDF or empty document."
        )

    return extracted_text



import hashlib

def calculate_file_hash(file_path: Path) -> str:

    sha256 = hashlib.sha256()

    # Read file in small chunks
    with open(file_path, "rb") as file:

        while True:

            chunk = file.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()
