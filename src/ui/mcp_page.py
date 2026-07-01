import json
import streamlit as st

from src.mcp.mcp_server import SimpleMCPServer


def render_mcp_page():
    st.header("MCP Layer")

    st.info(
        "This page demonstrates the MCP-style tool layer. "
        "Internal project capabilities are exposed as callable tools."
    )

    server = SimpleMCPServer()

    st.subheader("MCP Server Status")
    st.json(server.get_status())

    st.divider()

    st.subheader("Available MCP Tools")
    tools = server.list_tools()

    for tool in tools:
        with st.container(border=True):
            st.markdown(f"### {tool.get('name')}")
            st.write(tool.get("description"))
            st.caption(f"Required payload: {tool.get('required_payload')}")

    st.divider()

    st.subheader("Test MCP Tool")

    tool_names = [tool["name"] for tool in tools]

    selected_tool = st.selectbox(
        "Select MCP Tool",
        tool_names,
        key="mcp_selected_tool",
    )

    default_payloads = {
        "ask_ai": {
            "question": "Which candidates have Python experience?"
        },
        "career_roadmap": {
            "career_goal": "Move from RF optimization to AI automation roles."
        },
        "resume_advice": {
            "resume_goal": "Improve my CV for AI Engineer and Network Automation roles."
        },
        "recruiter_search": {
            "query": "Find candidates with Python, AI, RAG, LangGraph, or telecom automation experience."
        },
        "compare_candidates": {
            "candidate_a": "CAND-001",
            "candidate_b": "CAND-005",
            "target_role": "AI Engineer",
            "human_feedback": "Candidate B may have stronger AI tools experience."
        },
        "compare_uploaded_resumes": {
            "resume_a_text": "Candidate A has Python, telecom, RF optimization experience.",
            "resume_b_text": "Candidate B has AI, LangGraph, RAG, and automation experience.",
            "target_role": "AI Engineer",
            "human_feedback": "Human reviewer prefers Candidate B for AI work."
        },
        "learning_plan": {
            "target_role": "AI Engineer",
            "current_background": "RF Planning and Optimization engineer with Python basics.",
            "weekly_hours": 8
        },
    }

    payload_text = st.text_area(
        "Tool Payload JSON",
        value=json.dumps(default_payloads.get(selected_tool, {}), indent=2),
        height=220,
        key="mcp_payload_text",
    )

    if st.button("Run MCP Tool", key="run_mcp_tool_button"):
        try:
            payload = json.loads(payload_text)

            with st.spinner("Calling MCP tool..."):
                response = server.call_tool(selected_tool, payload)

            st.subheader("MCP Tool Response")
            st.json(response)

        except json.JSONDecodeError:
            st.error("Invalid JSON payload.")
        except Exception as error:
            st.error(f"MCP tool failed: {error}")

            