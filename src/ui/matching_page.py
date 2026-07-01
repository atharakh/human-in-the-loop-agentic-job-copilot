import streamlit as st

from src.agents.human_interaction_agent import HumanInteractionAgent
from src.ui.workflow_progress import render_workflow_progress
from src.graph.workflow import AgenticWorkflow
from src.services.storage_service import StorageService


def render_matching_page():
    st.header("AI Matching Workflow")

    storage = StorageService()
    storage.initialize()

    candidates = storage.load_candidates()
    jobs = storage.load_jobs()

    if not candidates or not jobs:
        st.warning("Please add at least one candidate and one job first.")
        return

    candidate_options = {
        f"{c.get('candidate_id')} - {c.get('full_name', c.get('name', 'Unknown'))}": c
        for c in candidates
    }

    job_options = {
        f"{j.get('job_id')} - {j.get('title', 'Unknown')} at {j.get('company', 'Unknown')}": j
        for j in jobs
    }

    selected_candidate_label = st.selectbox(
        "Select Candidate",
        list(candidate_options.keys())
    )

    selected_job_label = st.selectbox(
        "Select Job",
        list(job_options.keys())
    )

    candidate_id = candidate_options[selected_candidate_label].get("candidate_id")
    job_id = job_options[selected_job_label].get("job_id")

    workflow_engine = AgenticWorkflow()

    st.divider()

    if "workflow_state" not in st.session_state:
        st.session_state.workflow_state = None

    if st.button("Start Agentic Matching Workflow"):
        workflow = workflow_engine.start_matching_workflow(candidate_id, job_id)

        workflow = workflow_engine.retrieve_rag_context(workflow)
        workflow = workflow_engine.calculate_match(workflow)
        workflow = workflow_engine.verify_match(workflow)

        st.session_state.workflow_state = workflow

    if st.session_state.workflow_state:
        workflow = st.session_state.workflow_state

        st.subheader("Workflow Status")
        st.json(workflow.to_dict())
        render_workflow_progress(workflow)

        if workflow.match_result:
            st.subheader("Match Result")
            st.metric("Match Score", f"{workflow.match_result.get('match_score')}%")
            st.write("Confidence:", workflow.match_result.get("confidence"))
            st.write("Reasoning:", workflow.match_result.get("reasoning"))
            st.write("Matching Skills:", workflow.match_result.get("matching_skills"))
            st.write("Missing Skills:", workflow.match_result.get("missing_skills"))
            st.write("Recommendations:", workflow.match_result.get("recommendations"))
        if st.button("Explain This Match"):
            with st.spinner("Generating AI explanation..."):
                explanation = HumanInteractionAgent().explain_match_result(
                    workflow.match_result
                )

            st.subheader("AI Match Explanation")
            st.write(explanation)
        st.divider()

        st.subheader("Human Approval Checkpoint")

        decision = st.radio(
            "Do you approve this match?",
            ["pending", "approve", "reject"],
            horizontal=True
        )

        notes = st.text_area("Human notes", height=100)

        if st.button("Submit Human Decision"):
            workflow = workflow_engine.record_human_decision(
                workflow,
                decision,
                notes
            )
            st.session_state.workflow_state = workflow

        workflow = st.session_state.workflow_state

        if workflow.human_decision == "reject":
            st.error("Workflow rejected by human reviewer.")
            return

        if workflow.human_decision == "approve":
            st.success("Workflow approved. Continue generating application materials.")

            if st.button("Generate Cover Letter"):
                workflow = workflow_engine.generate_cover_letter(workflow)
                st.session_state.workflow_state = workflow

            if workflow.cover_letter:
                st.subheader("Generated Cover Letter")
                st.text_area("Cover Letter", workflow.cover_letter, height=280)

            if st.button("Generate Interview Questions"):
                workflow = workflow_engine.generate_interview_questions(workflow)
                st.session_state.workflow_state = workflow

            if workflow.interview_questions:
                st.subheader("Generated Interview Questions")
                st.text_area("Interview Questions", workflow.interview_questions, height=280)

            if workflow.cover_letter and workflow.interview_questions:
                if st.button("Save Application"):
                    workflow = workflow_engine.save_application(workflow)
                    st.session_state.workflow_state = workflow
                    st.success("Application saved successfully.")


