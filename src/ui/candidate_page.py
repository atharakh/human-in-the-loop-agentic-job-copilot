import shutil
from pathlib import Path

import streamlit as st

from src.agents.cv_agent import CVAgent
from src.services.config_service import ConfigService
from src.services.storage_service import StorageService
from src.services.vector_store_service import VectorStoreService
from src.tools.file_parser import FileParser


def render_candidate_page():
    st.header("Candidate Management")

    storage = StorageService()
    storage.initialize()

    vector_store = VectorStoreService()

    uploaded_file = st.file_uploader(
        "Upload CV",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file:
        save_path = ConfigService.CVS_DIR / uploaded_file.name

        with open(save_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        st.success(f"CV uploaded and saved to: {save_path}")

        if st.button("Analyze CV"):
            with st.spinner("Extracting and analyzing CV..."):
                cv_text = FileParser.extract_text(save_path)

                candidate = CVAgent().analyze_cv(cv_text)

                st.session_state["latest_candidate"] = candidate.to_dict()
                st.session_state["latest_cv_text"] = cv_text
                st.session_state["latest_cv_path"] = str(save_path)

            st.success("CV analyzed successfully.")

    if "latest_candidate" in st.session_state:
        st.subheader("Extracted Candidate Profile")
        st.json(st.session_state["latest_candidate"])

        st.info("Human checkpoint: review the extracted profile before saving.")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Approve and Save Candidate"):
                candidate_data = st.session_state["latest_candidate"]
                cv_text = st.session_state["latest_cv_text"]

                storage.save_candidate(candidate_data)

                vector_store.add_document(
                    document_id=f"CV-{candidate_data.get('candidate_id')}",
                    text=cv_text,
                    metadata={
                        "type": "candidate_cv",
                        "candidate_id": candidate_data.get("candidate_id"),
                        "name": candidate_data.get("full_name"),
                        "target_role": candidate_data.get("target_role"),
                    }
                )

                st.success("Candidate saved and indexed into RAG successfully.")

        with col2:
            if st.button("Reject Candidate Extraction"):
                st.warning("Candidate extraction rejected. Please upload another CV or modify the source file.")

    st.divider()

    st.subheader("Stored Candidates")
    st.json(storage.load_candidates())

    