import json
import streamlit as st

from src.agents.human_interaction_agent import HumanInteractionAgent
from src.services.storage_service import StorageService
from src.services.vector_store_service import VectorStoreService


def rebuild_vector_store():
    storage = StorageService()
    storage.initialize()

    vector_store = VectorStoreService()
    vector_store.clear_store()

    candidates = storage.load_candidates()
    jobs = storage.load_jobs()

    indexed_count = 0

    for candidate in candidates:
        candidate_id = candidate.get("candidate_id", f"CAND-{indexed_count}")
        text = json.dumps(candidate, indent=2)

        vector_store.add_document(
            document_id=f"CV-{candidate_id}",
            text=text,
            metadata={
                "type": "candidate_profile",
                "candidate_id": candidate_id,
                "name": candidate.get("full_name", candidate.get("name", "")),
            },
        )
        indexed_count += 1

    for job in jobs:
        job_id = job.get("job_id", f"JOB-{indexed_count}")
        text = json.dumps(job, indent=2)

        vector_store.add_document(
            document_id=f"JOB-{job_id}",
            text=text,
            metadata={
                "type": "job_description",
                "job_id": job_id,
                "title": job.get("title", ""),
                "company": job.get("company", ""),
            },
        )
        indexed_count += 1

    return indexed_count


def render_rag_page():
    st.header("RAG Search 2.0")

    vector_store = VectorStoreService()

    st.info(
        "Search indexed CVs and job descriptions using semantic similarity. "
        "You can also ask natural-language questions about candidates, jobs, and skills."
    )

    st.subheader("Vector Store Status")
    st.json(vector_store.get_status())

    st.divider()

    st.subheader("Rebuild Vector Store")

    st.warning(
        "If you switch between OpenAI and Ollama embeddings, rebuild the vector store "
        "so stored document embeddings match the active embedding provider."
    )

    if st.button("Rebuild Vector Store with Active Embedding Provider"):
        with st.spinner("Rebuilding vector store... This may take some time with Ollama."):
            indexed_count = rebuild_vector_store()

        st.success(f"Vector store rebuilt successfully. Indexed documents: {indexed_count}")
        st.rerun()

    st.divider()

    search_mode = st.radio(
        "Choose RAG Mode",
        [
            "Semantic Search",
            "Ask AI with RAG Context",
        ],
        horizontal=True,
    )

    if search_mode == "Semantic Search":
        query = st.text_input(
            "Semantic search query",
            value="Python LangChain RAG engineer",
        )

        top_k = st.slider("Number of results", min_value=1, max_value=10, value=5)

        if st.button("Search Vector Store"):
            with st.spinner("Searching vector store..."):
                results = vector_store.search(query, top_k=top_k)

            st.subheader("Search Results")

            for result in results:
                with st.expander(
                    f"{result.get('document_id')} | Score: {result.get('similarity_score')}"
                ):
                    st.write("Metadata:")
                    st.json(result.get("metadata", {}))

                    st.write("Provider Info:")
                    st.json(
                        {
                            "stored_embedding_provider": result.get("stored_embedding_provider"),
                            "query_embedding_provider": result.get("query_embedding_provider"),
                        }
                    )

                    st.write("Text Preview:")
                    st.write(result.get("text", "")[:1500])

    if search_mode == "Ask AI with RAG Context":
        question = st.text_input(
            "Ask a question",
            value="Which candidates have Python and 5G experience?",
        )

        if st.button("Ask with RAG"):
            with st.spinner("Retrieving context and generating answer..."):
                agent = HumanInteractionAgent()
                result = agent.answer_question(question)

            st.subheader("AI Answer")
            st.write(result["answer"])

            with st.expander("Retrieved RAG Evidence"):
                st.json(result["rag_results"])

            if st.button("Suggest Next Action"):
                next_action = agent.suggest_next_action(
                    result["question"],
                    result["answer"],
                )
                st.success(next_action)

                