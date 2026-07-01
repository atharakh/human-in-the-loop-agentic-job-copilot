import streamlit as st


def render_workflow_progress(workflow):
    """
    Displays visible progress for the agentic workflow.
    """

    st.subheader("Agentic Workflow Progress")

    step_labels = [
        ("started", "Workflow Started"),
        ("retrieve_rag_context", "RAG Context Retrieved"),
        ("calculate_match", "Match Calculated"),
        ("verify_match", "Match Verified"),
        ("request_human_approval", "Human Approval"),
        ("generate_cover_letter", "Cover Letter Generated"),
        ("generate_interview_questions", "Interview Questions Generated"),
        ("save_application", "Application Saved"),
    ]

    completed_steps = _get_completed_steps(workflow)

    for step_key, label in step_labels:
        if step_key in completed_steps:
            st.success(f"✅ {label}")
        elif workflow.current_step == step_key:
            st.info(f"🔄 {label}")
        else:
            st.write(f"⬜ {label}")

    st.divider()

    st.subheader("Workflow Logs")

    if workflow.logs:
        for log in workflow.logs:
            st.write(f"• {log}")
    else:
        st.info("No workflow logs yet.")


def _get_completed_steps(workflow):
    completed = []

    if workflow.rag_context:
        completed.append("retrieve_rag_context")

    if workflow.match_result:
        completed.append("calculate_match")

    if any("Verification result" in log for log in workflow.logs):
        completed.append("verify_match")

    if workflow.human_decision in ["approve", "reject"]:
        completed.append("request_human_approval")

    if workflow.cover_letter:
        completed.append("generate_cover_letter")

    if workflow.interview_questions:
        completed.append("generate_interview_questions")

    if workflow.status == "completed":
        completed.append("save_application")

    completed.append("started")

    return completed

    