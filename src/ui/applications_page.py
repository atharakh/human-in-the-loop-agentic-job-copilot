import streamlit as st

from src.services.storage_service import StorageService


def render_applications_page():
    st.header("Applications Dashboard")

    storage = StorageService()
    storage.initialize()

    applications = storage.load_applications()
    candidates = storage.load_candidates()
    jobs = storage.load_jobs()

    candidate_lookup = {
        candidate.get("candidate_id"): candidate
        for candidate in candidates
    }

    job_lookup = {
        job.get("job_id"): job
        for job in jobs
    }

    if not applications:
        st.info("No applications saved yet.")
        return

    st.metric("Total Applications", len(applications))

    st.divider()

    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Saved", "Submitted", "Interview", "Rejected", "Offer"]
    )

    filtered_applications = applications

    if status_filter != "All":
        filtered_applications = [
            app for app in applications
            if app.get("status") == status_filter
        ]

    st.subheader("Saved Applications")

    for application in reversed(filtered_applications):
        candidate = candidate_lookup.get(application.get("candidate_id"), {})
        job = job_lookup.get(application.get("job_id"), {})

        candidate_name = candidate.get("full_name", application.get("candidate_id"))
        job_title = job.get("title", application.get("job_id"))
        company = job.get("company", "Unknown Company")

        with st.container(border=True):
            col1, col2, col3 = st.columns(3)

            col1.write(f"**Candidate:** {candidate_name}")
            col1.write(f"**Candidate ID:** {application.get('candidate_id')}")

            col2.write(f"**Job:** {job_title}")
            col2.write(f"**Company:** {company}")

            col3.metric("Match Score", f"{application.get('match_score', 0)}%")
            col3.write(f"**Status:** {application.get('status', 'Saved')}")

            with st.expander("View Cover Letter"):
                st.write(application.get("cover_letter", "No cover letter saved."))

            with st.expander("View Interview Questions"):
                interview_questions = application.get("interview_questions", [])

                if isinstance(interview_questions, list):
                    for question_block in interview_questions:
                        st.write(question_block)
                else:
                    st.write(interview_questions)

            with st.expander("Application History"):
                st.json(application.get("history", []))

            with st.expander("Raw Application Data"):
                st.json(application)