import tempfile
from pathlib import Path

import streamlit as st

from src.agents.cv_agent import CVAgent
from src.agents.human_interaction_agent import HumanInteractionAgent
from src.tools.file_parser import FileParser


def render_human_interaction_page():
    st.header("AI Career Coach")

    st.info(
        "Career guidance, Resume Studio, Recruiter Workspace, Learning Hub, "
        "and Human-in-the-Loop decision support."
    )

    agent = HumanInteractionAgent()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "💬 Ask AI",
            "🚀 Career Roadmap",
            "📄 Resume Studio",
            "👔 Recruiter Workspace",
            "🎓 Learning Hub",
        ]
    )

    with tab1:
        st.subheader("Ask AI with RAG Context")

        if "human_interaction_history" not in st.session_state:
            st.session_state.human_interaction_history = []

        question = st.text_input(
            "Ask a question",
            placeholder="Example: Which candidates have Python and 5G experience?",
            key="ask_ai_question_input",
        )

        if st.button("Ask AI Assistant", key="ask_ai_button"):
            if not question.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Retrieving RAG context and generating answer..."):
                    result = agent.answer_question(question)
                    result["next_action"] = agent.suggest_next_action(
                        result["question"],
                        result["answer"],
                    )

                st.session_state.human_interaction_history.append(result)

        if st.session_state.human_interaction_history:
            st.subheader("Conversation History")

            for item in reversed(st.session_state.human_interaction_history):
                st.markdown(f"**Question:** {item['question']}")
                st.markdown(f"**Answer:** {item['answer']}")
                st.success(f"Suggested Next Action: {item['next_action']}")

                with st.expander("Retrieved RAG Evidence"):
                    st.json(item["rag_results"])

                st.divider()

    with tab2:
        st.subheader("Career Roadmap")

        career_goal = st.text_area(
            "Describe your career goal",
            value=(
                "I want to move from RF Planning and Optimization into AI automation, "
                "Network Automation, or technical project management roles in Germany."
            ),
            height=140,
            key="career_roadmap_goal",
        )

        if st.button("Generate Career Roadmap", key="career_roadmap_button"):
            if not career_goal.strip():
                st.warning("Please describe your career goal.")
            else:
                with st.spinner("Generating career roadmap..."):
                    result = agent.provide_career_coaching(career_goal)

                st.subheader("Career Coaching Advice")
                st.write(result["career_advice"])

                with st.expander("Supporting RAG Evidence"):
                    st.json(result["rag_results"])

    with tab3:
        st.subheader("Resume Studio")

        resume_mode = st.radio(
            "Choose Resume Studio mode",
            [
                "Upload Resume for Full Review",
                "Ask Resume Improvement Question",
            ],
            horizontal=True,
            key="resume_studio_mode",
        )

        if resume_mode == "Upload Resume for Full Review":
            uploaded_resume = st.file_uploader(
                "Upload Resume",
                type=["pdf", "docx", "txt"],
                key="resume_studio_upload",
            )

            target_goal = st.text_area(
                "Target role or improvement goal",
                value=(
                    "Improve this CV for AI Engineer, Network Automation Engineer, "
                    "RF Planning Engineer, or technical project management roles in Germany."
                ),
                height=120,
                key="resume_studio_target_goal",
            )

            if st.button("Analyze Resume in Resume Studio", key="resume_studio_analyze_button"):
                if uploaded_resume is None:
                    st.warning("Please upload a resume first.")
                else:
                    suffix = Path(uploaded_resume.name).suffix

                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                        temp_file.write(uploaded_resume.getvalue())
                        temp_path = temp_file.name

                    with st.spinner("Extracting and analyzing resume..."):
                        resume_text = FileParser.extract_text(temp_path)
                        candidate_profile = CVAgent().analyze_cv(resume_text)
                        result = agent.review_uploaded_resume(
                            resume_text=resume_text,
                            target_goal=target_goal,
                        )

                    st.subheader("Extracted Candidate Profile")
                    st.json(candidate_profile.to_dict())

                    st.subheader("Resume Studio Feedback")
                    st.write(result["resume_feedback"])

        if resume_mode == "Ask Resume Improvement Question":
            resume_goal = st.text_area(
                "What should Resume Studio focus on?",
                value=(
                    "How can I improve my CV for Network Automation Engineer, "
                    "AI Engineer, or RF Planning roles in Germany?"
                ),
                height=120,
                key="resume_studio_strategy_goal",
            )

            if st.button("Generate Resume Strategy", key="resume_studio_strategy_button"):
                if not resume_goal.strip():
                    st.warning("Please describe the resume improvement goal.")
                else:
                    with st.spinner("Generating resume improvement strategy..."):
                        result = agent.improve_resume_advice(resume_goal)

                    st.subheader("Resume Improvement Strategy")
                    st.write(result["resume_advice"])

                    with st.expander("Supporting RAG Evidence"):
                        st.json(result["rag_results"])

    with tab4:
        st.subheader("Recruiter Workspace")

        recruiter_mode = st.radio(
            "Choose Recruiter Workspace mode",
            [
                "Search Candidates",
                "Compare Existing Candidates",
                "Compare Uploaded Resumes",
                "Structured Human Evaluation",
            ],
            horizontal=True,
            key="recruiter_workspace_mode",
        )

        if recruiter_mode == "Search Candidates":
            recruiter_query = st.text_area(
                "Recruiter search request",
                value=(
                    "Find candidates suitable for AI Engineer, Network Automation Engineer, "
                    "or RF Planning Engineer roles. Highlight strengths, risks, and interview focus areas."
                ),
                height=120,
                key="recruiter_search_query",
            )

            if st.button("Search and Evaluate Candidates", key="recruiter_search_button"):
                if not recruiter_query.strip():
                    st.warning("Please enter a recruiter search request.")
                else:
                    with st.spinner("Searching candidates..."):
                        result = agent.recruiter_search_advice(recruiter_query)

                    st.subheader("Recruiter Search Advice")
                    st.write(result["recruiter_advice"])

                    with st.expander("Retrieved RAG Evidence"):
                        st.json(result["rag_results"])

        if recruiter_mode == "Compare Existing Candidates":
            candidate_a = st.text_input(
                "Candidate A",
                value="CAND-001",
                key="compare_existing_candidate_a",
            )

            candidate_b = st.text_input(
                "Candidate B",
                value="CAND-005",
                key="compare_existing_candidate_b",
            )

            target_role = st.text_input(
                "Target role",
                value="AI Engineer or Network Automation Engineer",
                key="compare_existing_target_role",
            )

            human_feedback = st.text_area(
                "Human feedback / observations",
                value=(
                    "Human reviewer thinks Candidate B may be stronger because of AI tools experience, "
                    "but Candidate A has stronger telecom domain knowledge."
                ),
                height=120,
                key="compare_existing_human_feedback",
            )

            if st.button("Compare Existing Candidates", key="compare_existing_button"):
                with st.spinner("Comparing candidates..."):
                    result = agent.compare_candidates_for_role(
                        candidate_a=candidate_a,
                        candidate_b=candidate_b,
                        target_role=target_role,
                        human_feedback=human_feedback,
                    )

                st.subheader("Candidate Comparison")
                st.write(result["comparison"])

                with st.expander("Retrieved RAG Evidence"):
                    st.json(result["rag_results"])

        if recruiter_mode == "Compare Uploaded Resumes":
            uploaded_resume_a = st.file_uploader(
                "Upload Candidate A Resume",
                type=["pdf", "docx", "txt"],
                key="compare_uploaded_resume_a",
            )

            uploaded_resume_b = st.file_uploader(
                "Upload Candidate B Resume",
                type=["pdf", "docx", "txt"],
                key="compare_uploaded_resume_b",
            )

            target_role = st.text_input(
                "Target role for comparison",
                value="AI Engineer or Network Automation Engineer",
                key="compare_uploaded_target_role",
            )

            human_feedback = st.text_area(
                "Human feedback / observations",
                value=(
                    "Human reviewer believes Candidate B may have stronger AI experience, "
                    "but Candidate A may have stronger telecom/domain experience."
                ),
                height=120,
                key="compare_uploaded_human_feedback",
            )

            if st.button("Compare Uploaded Resumes", key="compare_uploaded_button"):
                if uploaded_resume_a is None or uploaded_resume_b is None:
                    st.warning("Please upload both resumes.")
                else:
                    suffix_a = Path(uploaded_resume_a.name).suffix
                    suffix_b = Path(uploaded_resume_b.name).suffix

                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix_a) as temp_a:
                        temp_a.write(uploaded_resume_a.getvalue())
                        temp_a_path = temp_a.name

                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix_b) as temp_b:
                        temp_b.write(uploaded_resume_b.getvalue())
                        temp_b_path = temp_b.name

                    with st.spinner("Extracting and comparing uploaded resumes..."):
                        resume_a_text = FileParser.extract_text(temp_a_path)
                        resume_b_text = FileParser.extract_text(temp_b_path)

                        result = agent.compare_uploaded_resumes_for_role(
                            resume_a_text=resume_a_text,
                            resume_b_text=resume_b_text,
                            target_role=target_role,
                            human_feedback=human_feedback,
                        )

                    st.subheader("Uploaded Resume Comparison")
                    st.write(result["comparison"])

        if recruiter_mode == "Structured Human Evaluation":
            st.info(
                "Use this after AI comparison when a human reviewer wants to challenge or refine the AI recommendation."
            )

            ai_recommendation = st.text_area(
                "Paste AI recommendation or comparison result",
                height=160,
                key="structured_ai_recommendation",
            )

            preferred_candidate = st.radio(
                "Human preferred candidate",
                ["Candidate A", "Candidate B", "No preference"],
                horizontal=True,
                key="structured_preferred_candidate",
            )

            confidence = st.slider(
                "Human confidence",
                1,
                5,
                3,
                key="structured_human_confidence",
            )

            human_reasons = st.multiselect(
                "Human reasons",
                [
                    "Better technical skills",
                    "Better communication",
                    "Better leadership",
                    "Better domain knowledge",
                    "Better AI experience",
                    "Better cultural fit",
                    "Lower hiring risk",
                    "Better long-term potential",
                ],
                key="structured_human_reasons",
            )

            human_notes = st.text_area(
                "Additional human notes",
                height=120,
                key="structured_human_notes",
            )

            if st.button("Generate Consensus Recommendation", key="structured_consensus_button"):
                if not ai_recommendation.strip():
                    st.warning("Please paste the AI recommendation first.")
                else:
                    with st.spinner("Reconciling AI and human judgment..."):
                        result = agent.structured_recruiter_evaluation(
                            ai_recommendation=ai_recommendation,
                            preferred_candidate=preferred_candidate,
                            confidence=confidence,
                            human_reasons=human_reasons,
                            human_notes=human_notes,
                        )

                    st.subheader("Consensus Recommendation")
                    st.write(result["evaluation"])

    with tab5:
        st.subheader("Learning Hub")

        target_role = st.text_input(
            "Target role",
            value="AI Engineer or Network Automation Engineer",
            key="learning_hub_target_role",
        )

        current_background = st.text_area(
            "Current background",
            value=(
                "RF Planning and Optimization engineer with telecom, 4G/5G, KPI analysis, "
                "drive testing, Python basics, LangGraph, RAG, and Streamlit project experience."
            ),
            height=120,
            key="learning_hub_background",
        )

        weekly_hours = st.slider(
            "Available learning hours per week",
            2,
            30,
            8,
            key="learning_hub_weekly_hours",
        )

        if st.button("Generate Learning Plan", key="learning_hub_generate_button"):
            with st.spinner("Generating Learning Hub plan..."):
                result = agent.generate_learning_hub_plan(
                    target_role=target_role,
                    current_background=current_background,
                    weekly_hours=weekly_hours,
                )

            st.subheader("Learning Plan")
            st.write(result["learning_plan"])

            
            