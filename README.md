# AI-Powered Resume Screening & Job Matching System

An AI-powered application that analyzes job descriptions, extracts candidate information from resumes, evaluates candidate-job compatibility, and generates ranked screening reports through an interactive Streamlit dashboard.

## Overview

Recruiters often receive large numbers of resumes for a single job opening. Manually reviewing every resume and comparing candidate qualifications against job requirements can be time-consuming.

The **AI-Powered Resume Screening & Job Matching System** aims to simplify this process by combining Large Language Models (LLMs), Python-based document processing, and rule-based scoring.

Users can provide a job description and upload multiple resumes. The system extracts relevant information, identifies matching and missing skills, evaluates experience and education, calculates compatibility scores, and presents the results in an interactive dashboard.

## Key Features

### 1. Job Description Analysis
- Analyzes unstructured job descriptions using the Groq API.
- Extracts the job role and required technical skills.
- Identifies preferred skills and educational requirements.
- Extracts responsibilities and minimum experience requirements.
- Structures the extracted information into a consistent format.

### 2. Resume Information Extraction
- Supports PDF and DOCX resume formats.
- Extracts text from uploaded documents.
- Uses an LLM to identify candidate information.
- Extracts skills, professional experience, education, projects, and certifications.
- Structures the extracted information using Pydantic models.

### 3. Candidate-Job Matching
- Compares candidate skills against job requirements.
- Identifies matched and missing required skills.
- Evaluates preferred skills.
- Calculates experience and education scores where sufficient information is available.
- Generates an overall compatibility score using weighted scoring.

### 4. Batch Resume Screening
- Processes multiple resumes against a single job description.
- Generates individual candidate screening results.
- Ranks candidates based on their calculated compatibility scores.
- Handles individual resume-processing errors without necessarily stopping the entire batch.

### 5. Screening Analytics
- Calculates the total number of processed candidates.
- Tracks successful and failed resume processing.
- Calculates average compatibility scores.
- Identifies the highest-scoring candidate.
- Summarizes recommendation categories.
- Identifies frequently matched and missing skills.

### 6. Interactive Streamlit Dashboard
- Provides a user-friendly interface for job description input and resume uploads.
- Displays candidate rankings and compatibility scores.
- Visualizes screening statistics and skill comparisons.
- Provides downloadable screening reports in JSON and CSV formats.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| User Interface | Streamlit |
| LLM Integration | Groq API |
| Data Validation | Pydantic |
| Document Processing | PyPDF, python-docx |
| Data Analysis | Pandas |
| Data Visualization | Plotly |
| Environment Management | python-dotenv |
| Data Formats | JSON, CSV |

## Project Architecture

The application follows a modular structure, separating document processing, AI-based extraction, matching logic, batch screening, and report generation.

```text
AI-Resume-Screener/
│
├── app.py
├── main.py
├── config.py
├── schemas.py
├── job_description.txt
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── services/
│   ├── __init__.py
│   ├── job_analyzer.py
│   ├── resume_parser.py
│   ├── matcher.py
│   ├── batch_screener.py
│   └── report_generator.py
│
├── utils/
│   ├── __init__.py
│   └── document_reader.py
│
├── resumes/
│
└── output/
```

### Module Responsibilities

| File | Responsibility |
|---|---|
| `app.py` | Streamlit dashboard and application workflow |
| `main.py` | Main application entry point / standalone workflow |
| `config.py` | API configuration and model initialization |
| `schemas.py` | Pydantic data models for jobs, resumes, and experience |
| `job_analyzer.py` | Extracts structured information from job descriptions |
| `resume_parser.py` | Extracts structured candidate information from resumes |
| `matcher.py` | Performs candidate-job matching and score calculation |
| `batch_screener.py` | Processes and ranks multiple resumes |
| `report_generator.py` | Generates screening analytics and reports |
| `document_reader.py` | Reads PDF and DOCX documents |

## How the Matching System Works

The matching engine evaluates candidates using a weighted scoring approach.

| Evaluation Component | Weight |
|---|---:|
| Required Skills | 60% |
| Preferred Skills | 15% |
| Professional Experience | 15% |
| Education | 10% |

The final score is calculated using the available evaluation components. If a component cannot be evaluated because information is missing, its weight is excluded and the remaining weights are adjusted proportionally.

### Skill Matching

The system normalizes common skill variations before comparison.

For example:
- `JS` → `JavaScript`
- `ReactJS` → `React`
- `NodeJS` → `Node.js`

It then identifies:
- **Matched Skills:** Skills required by the job that are also present in the candidate's resume.
- **Missing Skills:** Skills required by the job that are not identified in the candidate's resume.

### Candidate Recommendations

Based on the overall compatibility score:

| Score | Recommendation |
|---|---|
| 75–100 | Strong Alignment |
| 50–74.99 | Partial Alignment |
| Below 50 | Low Alignment |

These recommendations are screening indicators, not final hiring decisions.

## Installation and Setup

### Prerequisites

Make sure you have the following installed:

- Python 3.10 or later
- pip
- Git
- A Groq API key

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Resume-Screener.git
```

Navigate into the project directory:

```bash
cd AI-Resume-Screener
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API Key

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace the placeholder with your actual API key.

The API key should never be committed to GitHub or shared publicly.

### 5. Run the Application

Start the Streamlit dashboard:

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## Usage

1. Launch the Streamlit application.
2. Enter or paste a job description.
3. Upload one or more resumes in PDF or DOCX format.
4. Start the screening process.
5. Allow the system to analyze the job description and extract candidate information.
6. Review the ranked candidate list and compatibility scores.
7. Explore screening analytics and skill comparisons.
8. Download the generated screening reports.

## Output and Reports

The application generates structured screening results that can be used for further analysis.

| Output File | Description |
|---|---|
| `batch_screening_results.json` | Detailed screening results for all processed resumes |
| `batch_screening_results.csv` | Tabular candidate screening results |
| `analytics.json` | Aggregated screening statistics |
| `screening_report.txt` | Human-readable screening summary |
| `parsed_resume.json` | Structured candidate information |
| `job_analysis.json` | Structured job description information |
| `match_report.json` | Individual candidate matching report |

Generated files are stored in the `output/` directory during local execution.

## Limitations

- Resume information extraction depends on the quality of the uploaded document and LLM responses.
- Scanned PDFs may require OCR support, which is not currently included.
- Skill matching primarily uses normalized skill names and rule-based comparison rather than advanced semantic similarity.
- Education matching uses a basic text-overlap heuristic and may require manual verification.
- Compatibility scores are indicative and should not be treated as definitive measures of candidate suitability.
- The application currently uses an external LLM API, so internet connectivity and API availability are required.
- The current implementation is a prototype and does not include user authentication, persistent candidate storage, or a production-grade recruitment workflow.

## Future Improvements

- Implement traditional NLP-based resume parsing using spaCy and regular expressions.
- Introduce TF-IDF and cosine similarity for semantic job-resume matching.
- Improve skill extraction using domain-specific NLP techniques.
- Add OCR support for scanned resumes.
- Introduce candidate profile storage and screening history.
- Add automated unit and integration tests.
- Improve scoring explainability and evaluation using manually labelled test datasets.
- Add authentication and role-based access control.
- Compare LLM-based screening against traditional NLP-based screening.

## Privacy and Security

- API credentials must be stored in environment variables or deployment secrets.
- Do not commit `.env` files, private resumes, or personally identifiable candidate information.
- Obtain appropriate permission before processing candidate resumes.
- Review extracted information and screening recommendations before making recruitment decisions.

## Deployment

The application can be deployed using [Streamlit Community Cloud](https://share.streamlit.io/).

Deployment requires:
1. Pushing the project to a GitHub repository.
2. Configuring the main application file as `app.py`.
3. Installing dependencies through `requirements.txt`.
4. Adding `GROQ_API_KEY` through the Streamlit Cloud secrets configuration.

## Author

**Swati Singh**

B.Tech – Information Technology  
Netaji Subhash Engineering College, Kolkata

---

*This project was developed as a learning-oriented application to explore Python, LLM integration, document processing, structured information extraction, rule-based matching, and interactive data visualization.*
