Stage 1 — Project foundation

Folder structure, imports, configuration, Pydantic models.



Stage 2 — Job description analyser

Send the JD to Groq and extract structured job requirements.



Stage 3 — Resume reader

Read PDF and DOCX files and extract their text.



Stage 4 — AI resume parser

Extract skills, education, internships, projects and experience.



Stage 5 — Matching engine

Compare candidates against job requirements and calculate scores.



Stage 6 — Batch screening

Process multiple resumes, handle failures and rank candidates.



Stage 7 — Reports and CSV

Generate detailed results and downloadable reports.



Stage 8 — Streamlit dashboard

Turn the Python application into a polished recruiter-facing application.

Step 1B. Create config.py
This file handles our application configuration

Step 1C. Create schemas.py
This is one of the most important concepts in this project.

What is a schema?

Imagine you ask an AI:

"Read this job description and tell me its required skills."

The AI could respond with a paragraph, a list, or some inconsistent JSON.

We want a predictable structure.

