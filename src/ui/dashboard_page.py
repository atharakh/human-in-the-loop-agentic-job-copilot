import streamlit as st

from src.services.config_service import ConfigService
from src.services.storage_service import StorageService
from src.services.vector_store_service import VectorStoreService


def render_dashboard():
    storage = StorageService()
    storage.initialize()

    vector_store = VectorStoreService()

    candidates = storage.load_candidates()
    jobs = storage.load_jobs()
    applications = storage.load_applications()
    vector_status = vector_store.get_status()

    st.header("Executive Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Candidates", len(candidates))
    col2.metric("Jobs", len(jobs))
    col3.metric("Applications", len(applications))
    col4.metric("RAG Documents", vector_status.get("documents_count", 0))

    st.divider()

    st.subheader("AI Runtime Configuration")

    col5, col6 = st.columns(2)

    active_llm = st.session_state.get(
        "runtime_llm_provider",
        ConfigService.LLM_PROVIDER
    )

    active_embedding = st.session_state.get(
        "runtime_embedding_provider",
        ConfigService.EMBEDDING_PROVIDER
    )

    col5.success(f"Active LLM Provider: {active_llm}")
    col6.success(f"Active Embedding Provider: {active_embedding}")

    st.divider()

    st.subheader("Application Summary")

    if applications:
        latest_application = applications[-1]

        st.write("Latest Application ID:", latest_application.get("application_id"))
        st.write("Candidate ID:", latest_application.get("candidate_id"))
        st.write("Job ID:", latest_application.get("job_id"))
        st.write("Status:", latest_application.get("status"))
        st.write("Match Score:", latest_application.get("match_score"))
    else:
        st.info("No applications saved yet.")

    st.divider()

    st.subheader("System Capabilities")

    st.markdown("""
    ✅ CV Upload and AI Profile Extraction  
    ✅ Job Description Parsing  
    ✅ Human Review Checkpoints  
    ✅ Candidate-Job Matching  
    ✅ RAG Search with Lightweight Vector Store  
    ✅ Runtime OpenAI / Ollama Switching  
    ✅ Planner, Verification, and Human Interaction Agents  
    ✅ LangGraph Workflow Orchestration  
    ✅ Cover Letter Generation  
    ✅ Interview Question Generation  
    ✅ Application Tracker  
    """)

    st.divider()

    st.subheader("Recommended Demo Flow")

    st.markdown("""
    1. Open **Settings** and show OpenAI/Ollama runtime switching.  
    2. Open **Dashboard** and show system statistics.  
    3. Open **Candidate Management** and upload or review a CV.  
    4. Open **Job Management** and add or review a job.  
    5. Open **RAG Search** and ask a skill-based query.  
    6. Open **AI Matching** and run the Human-in-the-Loop workflow.  
    7. Open **LangGraph Workflow** and show orchestration.  
    8. Open **Applications** and show saved applications.  
    """)

    