import streamlit as st

from src.llm import LLMManager
from src.services.config_service import ConfigService
from src.services.embedding_service import EmbeddingService


def render_settings_page():
    st.header("AI Settings")

    st.subheader("Runtime Provider Switching")

    current_llm = st.session_state.get(
        "runtime_llm_provider",
        ConfigService.LLM_PROVIDER
    )

    current_embedding = st.session_state.get(
        "runtime_embedding_provider",
        ConfigService.EMBEDDING_PROVIDER
    )

    llm_provider = st.selectbox(
        "Select LLM Provider",
        ["openai", "ollama"],
        index=["openai", "ollama"].index(current_llm)
    )

    embedding_provider = st.selectbox(
        "Select Embedding Provider",
        ["openai", "ollama"],
        index=["openai", "ollama"].index(current_embedding)
    )

    if st.button("Apply Runtime Settings"):
        st.session_state["runtime_llm_provider"] = llm_provider
        st.session_state["runtime_embedding_provider"] = embedding_provider
        st.success("Runtime AI settings updated successfully.")
        st.info("The change applies during the current Streamlit session.")

    st.divider()

    st.subheader("Current Active Configuration")

    llm_manager = LLMManager()
    embedding_service = EmbeddingService()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Active LLM Provider", llm_manager.get_status()["active_provider"])
        st.json(llm_manager.get_status())

    with col2:
        st.metric(
            "Active Embedding Provider",
            embedding_service.get_status()["active_provider"]
        )
        st.json(embedding_service.get_status())

    st.divider()

    st.subheader("Model Configuration")

    st.write("OpenAI Model:", ConfigService.OPENAI_MODEL)
    st.write("OpenAI Embedding Model:", ConfigService.OPENAI_EMBEDDING_MODEL)
    st.write("Ollama Model:", ConfigService.OLLAMA_MODEL)
    st.write("Ollama Embedding Model:", ConfigService.OLLAMA_EMBED_MODEL)

    st.warning(
        "For Ollama mode, make sure Ollama is running locally and the required models are pulled."
    )

    