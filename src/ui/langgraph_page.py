import streamlit as st

from src.agents.human_interaction_agent import HumanInteractionAgent
from src.graph.langgraph_workflow import LangGraphWorkflow
from src.services.storage_service import StorageService
from src.ui.workflow_progress import render_workflow_progress


def _render_agent_pipeline():
    st.subheader("Agent Collaboration Pipeline")

    agents = [
        ("🧠 Planner Agent", "Creates workflow plan"),
        ("📚 RAG Retrieval", "Retrieves context"),
        ("🎯 Matcher Agent", "Calculates match"),
        ("✅ Verification Agent", "Validates output"),
        ("👤 Human Agent", "Handles approval"),
        ("✉️ Cover Letter Agent", "Generates cover letter"),
        ("🎤 Interview Agent", "Generates questions"),
        ("📌 Tracker Agent", "Saves application"),
    ]

    cols = st.columns(4)

    for index, (name, desc) in enumerate(agents):
        with cols[index % 4]:
            with st.container(border=True):
                st.write(f"**{name}**")
                st.caption(desc)
                st.success("Ready")


def _render_workflow_summary(workflow):
    st.subheader("Workflow Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Workflow ID", workflow.workflow_id)
    col2.metric("Status", workflow.status)
    col3.metric("Current Step", workflow.current_step)
    col4.metric("Human Decision", workflow.human_decision)

    if workflow.match_result:
        st.metric("Match Score", f"{workflow.match_result.get('match_score')}%")


def _render_match_result(workflow):
    if not workflow.match_result:
        return

    st.subheader("Match Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Match Score", f"{workflow.match_result.get('match_score')}%")
        st.write("**Confidence:**", workflow.match_result.get("confidence"))
        st.write("**Reasoning:**")
        st.write(workflow.match_result.get("reasoning"))

    with col2:
        st.write("**Matching Skills:**")
        st.write(workflow.match_result.get("matching_skills"))

        st.write("**Missing Skills:**")
        st.write(workflow.match_result.get("missing_skills"))

        st.write("**Recommendations:**")
        st.write(workflow.match_result.get("recommendations"))

    if st.button("Explain Match Result", key="explain_langgraph_match"):
        with st.spinner("Generating explanation..."):
            explanation = HumanInteractionAgent().explain_match_result(
                workflow.match_result
            )

        st.subheader("AI Explanation")
        st.write(explanation)


def _render_generated_outputs(workflow):
    if workflow.cover_letter:
        st.subheader("Generated Cover Letter")
        st.text_area("Cover Letter", workflow.cover_letter, height=250)

    if workflow.interview_questions:
        st.subheader("Generated Interview Questions")
        st.text_area("Interview Questions", workflow.interview_questions, height=250)


def render_langgraph_page():
    st.header("LangGraph Workflow Control Center")

    st.info(
        "This page demonstrates LangGraph orchestration with RAG, matching, "
        "verification, human approval, cover letter generation, interview questions, "
        "and application tracking."
    )

    storage = StorageService()
    storage.initialize()

    candidates = storage.load_candidates()
    jobs = storage.load_jobs()

    if not candidates or not jobs:
        st.warning("Please add candidates and jobs first.")
        return

    _render_agent_pipeline()

    st.divider()

    candidate_options = {
        f"{c.get('candidate_id')} - {c.get('full_name', c.get('name', 'Unknown'))}": c
        for c in candidates
    }

    job_options = {
        f"{j.get('job_id')} - {j.get('title', 'Unknown')} at {j.get('company', 'Unknown')}": j
        for j in jobs
    }

    col1, col2 = st.columns(2)

    with col1:
        selected_candidate = candidate_options[
            st.selectbox("Select Candidate", list(candidate_options.keys()))
        ]

    with col2:
        selected_job = job_options[
            st.selectbox("Select Job", list(job_options.keys()))
        ]

    candidate_id = selected_candidate.get("candidate_id")
    job_id = selected_job.get("job_id")

    graph = LangGraphWorkflow()

    if "langgraph_workflow" not in st.session_state:
        st.session_state.langgraph_workflow = None

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        if st.button("Run Workflow Until Human Approval", key="run_langgraph"):
            with st.spinner("Running LangGraph workflow..."):
                workflow = graph.run_until_human_approval(candidate_id, job_id)
                st.session_state.langgraph_workflow = workflow

            st.success("Workflow reached human approval checkpoint.")
            st.rerun()

    with col4:
        if st.button("Reset Workflow", key="reset_langgraph"):
            st.session_state.langgraph_workflow = None
            st.success("Workflow reset successfully.")
            st.rerun()

    workflow = st.session_state.langgraph_workflow

    if not workflow:
        st.info("No active workflow yet. Select a candidate and job, then run the workflow.")
        return

    st.divider()

    _render_workflow_summary(workflow)

    st.divider()

    render_workflow_progress(workflow)

    st.divider()

    _render_match_result(workflow)

    st.divider()

    if workflow.status == "waiting_for_human":
        st.subheader("Human Approval Checkpoint")

        decision = st.radio(
            "Approve or reject this LangGraph workflow?",
            ["pending", "approve", "reject"],
            horizontal=True,
            key="langgraph_human_decision",
        )

        notes = st.text_area(
            "Human notes",
            height=100,
            key="langgraph_human_notes",
        )

        if st.button("Continue Workflow After Human Decision", key="continue_langgraph"):
            if decision == "pending":
                st.warning("Please approve or reject before continuing.")
                return

            with st.spinner("Continuing workflow after human decision..."):
                workflow = graph.continue_after_human_approval(
                    workflow,
                    decision,
                    notes,
                )
                st.session_state.langgraph_workflow = workflow

            if workflow.status == "rejected":
                st.error("Workflow rejected by human reviewer.")
            else:
                st.success("LangGraph workflow completed successfully.")

            st.rerun()

    elif workflow.status == "completed":
        st.success("Workflow completed successfully.")

    elif workflow.status == "rejected":
        st.error("Workflow was rejected by the human reviewer.")

    st.divider()

    workflow = st.session_state.langgraph_workflow

    if workflow:
        _render_generated_outputs(workflow)

        with st.expander("Raw Workflow Data"):
            st.json(workflow.to_dict())

            