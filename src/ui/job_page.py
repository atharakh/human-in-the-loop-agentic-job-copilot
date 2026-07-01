import streamlit as st

from src.agents.job_parser_agent import JobParserAgent
from src.services.storage_service import StorageService
from src.services.vector_store_service import VectorStoreService


def render_job_page():
    st.header("Job Management")

    storage = StorageService()
    storage.initialize()
    vector_store = VectorStoreService()

    job_text = st.text_area("Paste Job Description", height=300)

    if st.button("Analyze Job Description"):
        if not job_text.strip():
            st.warning("Please paste a job description first.")
            return

        with st.spinner("Analyzing job description..."):
            job = JobParserAgent().analyze_job(job_text)

        st.session_state["latest_job"] = job.to_dict()
        st.session_state["latest_job_text"] = job_text

        st.success("Job analyzed successfully.")

    if "latest_job" in st.session_state:
        st.subheader("Extracted Job Profile")
        st.json(st.session_state["latest_job"])

        st.info("Human checkpoint: review the extracted job before saving.")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Approve and Save Job"):
                job_data = st.session_state["latest_job"]
                job_text = st.session_state["latest_job_text"]

                storage.save_job(job_data)

                vector_store.add_document(
                    document_id=f"JOB-{job_data.get('job_id')}",
                    text=job_text,
                    metadata={
                        "type": "job_description",
                        "job_id": job_data.get("job_id"),
                        "title": job_data.get("title"),
                        "company": job_data.get("company"),
                    }
                )

                st.success("Job saved and indexed into RAG successfully.")

        with col2:
            if st.button("Reject Job Extraction"):
                st.warning("Job extraction rejected. Please paste or modify the job description.")

    st.divider()

    st.subheader("Stored Jobs")
    st.json(storage.load_jobs())

    