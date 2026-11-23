
import json
import tempfile
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from services.job_analyzer import analyze_job_description
from services.batch_screener import (
    screen_multiple_resumes,
    save_batch_reports
)
from services.report_generator import (
    generate_analytics,
    save_analytics,
    generate_text_report
)


# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)


# -----------------------------------------
# CUSTOM CSS
# -----------------------------------------

st.markdown("""
<style>
    .main-title {
        font-size: 34px;
        font-weight: 700;
    }

    .subtitle {
        color: #888888;
        font-size: 16px;
    }

    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.08);
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------
# SESSION STATE
# -----------------------------------------

if "results" not in st.session_state:
    st.session_state.results = None

if "analytics" not in st.session_state:
    st.session_state.analytics = None

if "job" not in st.session_state:
    st.session_state.job = None


# -----------------------------------------
# HEADER
# -----------------------------------------

st.markdown(
    '<div class="main-title">📄 AI-Powered Resume Screening</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze job descriptions, screen resumes and rank candidates.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# -----------------------------------------
# SIDEBAR
# -----------------------------------------

st.sidebar.title("About the Project")

st.sidebar.write(
    "An AI-assisted resume screening application "
    "using Groq, Python and Streamlit."
)

st.sidebar.divider()

st.sidebar.subheader("Screening Workflow")

st.sidebar.write("1. Enter a job description")
st.sidebar.write("2. Upload candidate resumes")
st.sidebar.write("3. Run AI screening")
st.sidebar.write("4. Review candidate rankings")
st.sidebar.write("5. Download reports")


# -----------------------------------------
# INPUT SECTION
# -----------------------------------------

st.header("1. Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=220,
    placeholder="Enter the complete job description..."
)

st.header("2. Upload Candidate Resumes")

uploaded_resumes = st.file_uploader(
    "Upload PDF or DOCX resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

st.caption(
    "You can upload multiple resumes. "
    "Each resume will be processed separately."
)

st.divider()


# -----------------------------------------
# SCREENING BUTTON
# -----------------------------------------

if st.button(
    "🚀 Start Resume Screening",
    type="primary",
    use_container_width=True
):

    if not job_description.strip():
        st.error("Please enter a job description.")

    elif not uploaded_resumes:
        st.error("Please upload at least one resume.")

    else:

        try:
            with st.spinner("Analyzing job description..."):

                job = analyze_job_description(job_description)

                if not job.role:
                    raise ValueError(
                        "Could not extract the job role from the description."
                    )

                if not job.required_skills and not job.preferred_skills:
                    raise ValueError(
                        "No skills were extracted. Please check the job description."
                    )

            st.success(f"Job analyzed: {job.role}")

            with st.spinner("Processing candidate resumes..."):

                # Temporary folder for uploaded files.
                # Files are removed automatically after screening.
                with tempfile.TemporaryDirectory() as temp_dir:

                    resume_folder = Path(temp_dir)

                    for index, uploaded_file in enumerate(
                        uploaded_resumes,
                        start=1
                    ):

                        # Prefix the filename to avoid duplicate-name collisions.
                        safe_name = (
                            f"{index}_{Path(uploaded_file.name).name}"
                        )

                        file_path = resume_folder / safe_name

                        file_path.write_bytes(uploaded_file.getvalue())

                    # Screen all uploaded resumes.
                    results = screen_multiple_resumes(
                        job,
                        resume_folder
                    )

                # Generate analytics.
                analytics = generate_analytics(results)

                # Save reports to output folder.
                output_folder = Path("output")

                save_batch_reports(results, output_folder)
                save_analytics(analytics, output_folder)
                generate_text_report(analytics, output_folder)

                # Store results across Streamlit reruns.
                st.session_state.results = results
                st.session_state.analytics = analytics
                st.session_state.job = job.model_dump()

            st.success("Resume screening completed!")

        except Exception as error:
            st.error(f"Screening failed: {error}")


# -----------------------------------------
# RESULTS DASHBOARD
# -----------------------------------------

if st.session_state.results is not None:

    results = st.session_state.results
    analytics = st.session_state.analytics

    st.divider()

    st.header("3. Screening Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Resumes",
        analytics["total_candidates"]
    )

    col2.metric(
        "Successfully Processed",
        analytics["successfully_processed"]
    )

    col3.metric(
        "Failed",
        analytics["failed_candidates"]
    )

    average_score = analytics["average_score"]

    col4.metric(
        "Average Match Score",
        f"{average_score}%" if average_score is not None else "N/A"
    )

    # Top candidate.
    top_candidate = analytics["top_candidate"]

    if top_candidate:

        st.subheader("Top Scoring Candidate")

        st.success(
            f"{top_candidate['name']} — "
            f"{top_candidate['score']}% JD alignment"
        )

    st.divider()


    # -----------------------------------------
    # CANDIDATE RANKING
    # -----------------------------------------

    st.header("4. Candidate Rankings")

    successful_results = [
        result for result in results
        if isinstance(result.get("overall_score"), (int, float))
    ]

    if successful_results:

        ranking_data = []

        for rank, result in enumerate(successful_results, start=1):

            ranking_data.append({
                "Rank": rank,
                "Candidate": result.get("candidate_name"),
                "Resume": result.get("source_file"),
                "Match Score": result.get("overall_score"),
                "Recommendation": result.get("recommendation")
            })

        ranking_df = pd.DataFrame(ranking_data)

        st.dataframe(
            ranking_df,
            use_container_width=True,
            hide_index=True
        )

        # Score distribution chart.
        fig = px.bar(
            ranking_df,
            x="Candidate",
            y="Match Score",
            color="Recommendation",
            title="Candidate JD Alignment Scores",
            hover_data=["Resume"]
        )

        fig.update_layout(
            yaxis_range=[0, 100]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.warning("No candidates were successfully scored.")


    st.divider()


    # -----------------------------------------
    # SKILL ANALYTICS
    # -----------------------------------------

    st.header("5. Skill Analysis")

    skill_col1, skill_col2 = st.columns(2)

    matched_skills = analytics["most_matched_skills"]
    missing_skills = analytics["most_missing_skills"]

    with skill_col1:

        st.subheader("Most Matched Required Skills")

        if matched_skills:

            matched_df = pd.DataFrame(
                matched_skills,
                columns=["Skill", "Candidate Count"]
            )

            fig = px.bar(
                matched_df,
                x="Candidate Count",
                y="Skill",
                orientation="h",
                title="Frequently Matched Skills"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("No matched required skills available.")

    with skill_col2:

        st.subheader("Most Missing Required Skills")

        if missing_skills:

            missing_df = pd.DataFrame(
                missing_skills,
                columns=["Skill", "Candidate Count"]
            )

            fig = px.bar(
                missing_df,
                x="Candidate Count",
                y="Skill",
                orientation="h",
                title="Frequently Missing Skills"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("No missing required skills available.")


    st.divider()


    # -----------------------------------------
    # CANDIDATE DETAILS
    # -----------------------------------------

    st.header("6. Individual Candidate Analysis")

    for result in results:

        candidate_name = (
            result.get("candidate_name")
            or result.get("source_file")
            or "Unknown candidate"
        )

        with st.expander(candidate_name):

            if result.get("overall_score") is None:

                st.error(
                    result.get("error", "Candidate could not be scored.")
                )

                continue

            st.write(
                "**JD Alignment Score:**",
                f"{result['overall_score']}%"
            )

            st.write(
                "**Recommendation:**",
                result["recommendation"]
            )

            st.write("**Matched Required Skills**")

            st.write(
                ", ".join(result.get("matched_required_skills", []))
                or "None"
            )

            st.write("**Missing Required Skills**")

            st.write(
                ", ".join(result.get("missing_required_skills", []))
                or "None"
            )

            st.write("**Experience Analysis**")

            st.write(result.get("experience_note", "Not available."))

            st.write("**Education Analysis**")

            st.write(result.get("education_note", "Not available."))


    st.divider()


    # -----------------------------------------
    # DOWNLOAD REPORTS
    # -----------------------------------------

    st.header("7. Download Reports")

    download_col1, download_col2, download_col3 = st.columns(3)

    # Detailed JSON.
    json_data = json.dumps(results, indent=4)

    download_col1.download_button(
        "Download JSON",
        data=json_data,
        file_name="resume_screening_results.json",
        mime="application/json",
        use_container_width=True
    )

    # CSV.
    csv_data = pd.DataFrame(results)

    for column in [
        "matched_required_skills",
        "missing_required_skills",
        "matched_preferred_skills",
        "missing_preferred_skills"
    ]:

        if column in csv_data.columns:

            csv_data[column] = csv_data[column].apply(
                lambda value: ", ".join(value)
                if isinstance(value, list)
                else value
            )

    download_col2.download_button(
        "Download CSV",
        data=csv_data.to_csv(index=False),
        file_name="resume_screening_results.csv",
        mime="text/csv",
        use_container_width=True
    )

    # Analytics.
    download_col3.download_button(
        "Download Analytics",
        data=json.dumps(analytics, indent=4),
        file_name="resume_analytics.json",
        mime="application/json",
        use_container_width=True
    )


else:

    st.info(
        "Enter a job description and upload resumes to start screening."
    )
