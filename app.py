import streamlit as st

from src.services.config_service import ConfigService
from src.services.logger_service import LoggerService
from src.ui.mcp_page import render_mcp_page
from src.ui.dashboard_page import render_dashboard
from src.ui.candidate_page import render_candidate_page
from src.ui.job_page import render_job_page
from src.ui.matching_page import render_matching_page
from src.ui.rag_page import render_rag_page
from src.ui.applications_page import render_applications_page
from src.ui.settings_page import render_settings_page
from src.ui.human_interaction_page import render_human_interaction_page
from src.ui.langgraph_page import render_langgraph_page



st.set_page_config(
    page_title="Agentic AI Job Search Copilot",
    page_icon="🤖",
    layout="wide"
)

ConfigService.create_required_dirs()
ConfigService.validate()

logger = LoggerService.get_logger("app")
logger.info("Final Streamlit app started.")

st.sidebar.title("🤖 Job Copilot")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👤 Candidate Management",
        "💼 Job Management",
        "🎯 AI Matching",
        "🧠 RAG Search",
        "📄 Applications",
        "💬 Human Interaction",
        "🧩 MCP Layer",
        "🕸 LangGraph Workflow",
        "⚙ Settings",
    ]
)

st.title("Human-in-the-Loop Agentic AI Job Search Copilot")

if page == "🏠 Dashboard":
    render_dashboard()

elif page == "👤 Candidate Management":
    render_candidate_page()

elif page == "💼 Job Management":
    render_job_page()

elif page == "🎯 AI Matching":
    render_matching_page()

elif page == "🧠 RAG Search":
    render_rag_page()

elif page == "📄 Applications":
    render_applications_page()

elif page == "⚙ Settings":
    render_settings_page()

elif page == "💬 Human Interaction":
    render_human_interaction_page()

elif page == "🕸 LangGraph Workflow":
    render_langgraph_page()

elif page == "🧩 MCP Layer":
    render_mcp_page()



    