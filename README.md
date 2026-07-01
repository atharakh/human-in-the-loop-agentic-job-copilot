# 🤖 Human-in-the-Loop Agentic AI Job Search Copilot

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![LangGraph](https://img.shields.io/badge/Framework-LangGraph-success)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT-green)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-orange)
![Docker](https://img.shields.io/badge/Deployment-Docker-blueviolet)
![RAG](https://img.shields.io/badge/RAG-ChromaDB-important)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

# Human-in-the-Loop Agentic AI Job Search Copilot

An enterprise-grade AI-powered recruitment platform that combines **Human-in-the-Loop decision making**, **Retrieval-Augmented Generation (RAG)**, **LangGraph agent orchestration**, **Model Context Protocol (MCP)**, and **Large Language Models** to support modern recruitment and career guidance.

The application demonstrates how AI agents and human reviewers collaborate during candidate screening, resume evaluation, job matching, career coaching, recruiter analysis, and learning recommendations.

Unlike conventional recruitment assistants, the system allows human experts to remain in control of every critical hiring decision while AI performs reasoning, document retrieval, scoring, recommendations, and explanation generation.

---

# Table of Contents

- Project Overview
- Features
- System Architecture
- Technology Stack
- Project Structure
- Installation
- Configuration
- Running the Application
- Docker Deployment
- LangGraph Workflow
- MCP Layer
- Human-in-the-Loop Workflow
- Modules
- Logging & Observability
- Future Improvements
- Authors
- License

---

# Project Overview

The Human-in-the-Loop Agentic AI Job Search Copilot is designed to demonstrate an intelligent recruitment platform capable of assisting recruiters, hiring managers, and job seekers.

Instead of replacing recruiters, the AI collaborates with humans by providing explainable recommendations while allowing humans to approve or override every important decision.

The project combines:

- Human-in-the-Loop AI
- Retrieval Augmented Generation (RAG)
- LangGraph Agent Workflow
- Model Context Protocol (MCP)
- OpenAI GPT
- Ollama Local LLM
- ChromaDB Vector Search
- Streamlit User Interface
- Docker Deployment
- FastAPI-ready Backend Architecture

---

# Key Features

## Candidate Management

- Store candidate profiles
- Resume ingestion
- Candidate search
- Resume upload
- Resume analysis
- Candidate comparison
- ATS-style recommendations

---

## Job Management

- Job description storage
- Job editing
- Job search
- Role categorization
- Skill extraction

---

## AI Matching Engine

- Resume-to-job matching
- Candidate ranking
- Matching score generation
- Skill gap identification
- Missing keyword detection

---

## Human-in-the-Loop

The recruiter remains in control throughout the hiring process.

The AI generates:

- Candidate recommendations
- Resume feedback
- Career coaching
- Recruiter insights
- Human review support

Humans can:

- Approve
- Reject
- Request review
- Provide feedback
- Override AI recommendations

---

## AI Career Coach

The system provides:

- Career roadmap
- Resume improvement
- Learning recommendations
- Skill gap analysis
- Certification suggestions
- Portfolio ideas
- Interview preparation

---

## Learning Hub

- Personalized learning plans
- Weekly study schedule
- Technology recommendations
- Career transition guidance

---

## Recruiter Workspace

Provides intelligent recruiter assistance including:

- Candidate comparison
- Resume comparison
- Hiring recommendations
- Human evaluation workflow
- AI explanation generation

---

## RAG Search

Retrieval-Augmented Generation enables the application to search stored resumes and job descriptions before generating AI responses.

The LLM answers questions using retrieved context instead of relying solely on model memory.

---

## LangGraph Workflow

The application demonstrates an agent workflow using LangGraph where specialized agents collaborate to solve recruitment tasks.

Agents include:

- Human Interaction Agent
- Candidate Agent
- Job Agent
- Matching Agent
- RAG Agent
- MCP Layer

---

## Model Context Protocol (MCP)

The MCP Layer acts as an orchestration layer between AI agents and external services.

It manages:

- Context exchange
- Tool routing
- External API integration
- LLM communication
- Agent coordination

---

## External Integrations

The project demonstrates integration with multiple external services including:

- OpenAI API
- Ollama Local Models
- ChromaDB
- Docker
- Streamlit

The architecture is extensible for additional enterprise APIs.

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Programming Language | Python 3.11 |
| Frontend | Streamlit |
| Backend | Python Service Layer (FastAPI-ready architecture) |
| Agent Framework | LangGraph + LangChain |
| Local LLM | Ollama |
| Cloud LLM | OpenAI GPT |
| Embeddings | Ollama Embeddings / OpenAI Embeddings |
| Vector Database | ChromaDB |
| Retrieval | Retrieval-Augmented Generation (RAG) |
| Agent Communication | Model Context Protocol (MCP) |
| Deployment | Docker & Docker Compose |
| Version Control | Git & GitHub |
| Logging | Python Logging Service |
| Configuration | Environment Variables (.env) |

---

# High-Level System Architecture

The project follows a modular Agentic AI architecture where the Streamlit interface communicates with specialized AI agents. These agents retrieve relevant context through a Retrieval-Augmented Generation (RAG) pipeline, invoke Large Language Models (OpenAI or Ollama), and return explainable results to the user.

The architecture is organized into independent components to improve scalability, maintainability, and future extensibility.

## Main Components

- Streamlit User Interface
- Human Interaction Agent
- Candidate Management
- Job Management
- AI Matching Engine
- LangGraph Workflow
- MCP Layer
- RAG Pipeline
- ChromaDB Vector Store
- OpenAI / Ollama Providers
- Configuration & Logging Services

---

# Agent Workflow

The application is built around multiple cooperating AI components.

## Human Interaction Agent

Responsibilities:

- Answer recruiter questions
- Generate career coaching
- Resume analysis
- Recruiter recommendations
- Candidate comparison
- Learning plans
- Human review workflow

---

## Candidate Management

Responsible for:

- Resume storage
- Candidate retrieval
- Candidate metadata
- Candidate search
- Candidate updates

---

## Job Management

Responsible for:

- Job descriptions
- Job creation
- Job search
- Skill extraction
- Job metadata

---

## AI Matching Engine

Provides:

- Resume-to-job matching
- Matching score calculation
- Skill comparison
- Missing keyword detection
- Candidate ranking

---

## Retrieval-Augmented Generation (RAG)

Instead of asking the LLM directly, the application first retrieves relevant information from the vector database.

Workflow:

1. User submits a query.
2. Relevant documents are retrieved from ChromaDB.
3. Retrieved context is combined into a prompt.
4. The LLM generates an informed response.
5. The response is returned to the user.

Benefits:

- Reduced hallucinations
- Context-aware responses
- Better explainability
- Faster retrieval of relevant information

---

# LangGraph Workflow

The LangGraph implementation orchestrates multiple intelligent components.

Typical execution flow:

1. User submits request.
2. LangGraph selects the appropriate workflow.
3. Context is retrieved using RAG.
4. MCP Layer selects the required tool.
5. LLM reasoning is performed.
6. Human review (if applicable).
7. Final response returned to the interface.

This workflow demonstrates multi-agent collaboration while preserving human oversight.

---

# Model Context Protocol (MCP)

The project includes an MCP-style abstraction layer that exposes internal capabilities as callable tools.

Current MCP tools include:

- Ask AI
- Career Roadmap
- Resume Advice
- Recruiter Search
- Candidate Comparison
- Resume Comparison
- Learning Plan

The MCP Layer acts as an orchestration interface between the user interface, LangGraph workflow, and AI services.

Advantages:

- Modular tool registration
- Standardized interfaces
- Easier integration of external tools
- Scalable architecture
- Future interoperability with additional MCP-compatible services

---

# Large Language Model Support

The application supports two independent LLM providers.

## OpenAI

Used for:

- Advanced reasoning
- Complex resume analysis
- Detailed recruiter recommendations
- Career coaching

Advantages:

- High-quality reasoning
- Strong instruction following
- Better long-context handling

---

## Ollama

Used for:

- Fully local inference
- Offline execution
- Privacy-sensitive workflows
- CPU-based deployment

Advantages:

- No cloud dependency
- Local data processing
- Cost-efficient development
- Enterprise-friendly deployment

The application can dynamically switch between OpenAI and Ollama using configuration settings.

---

# Project Folder Structure

```text
Human-In-The-Loop-Agentic-Job-Copilot/

├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── .env
│
├── data/
│   ├── candidates/
│   ├── jobs/
│   └── uploads/
│
├── logs/
│
├── src/
│
│   ├── agents/
│   │      candidate_agent.py
│   │      human_interaction_agent.py
│   │      recruiter_agent.py
│   │
│   ├── llm/
│   │      openai_provider.py
│   │      ollama_provider.py
│   │      llm_manager.py
│   │
│   ├── mcp/
│   │      tool_registry.py
│   │      mcp_server.py
│   │
│   ├── rag/
│   │
│   ├── services/
│   │      config_service.py
│   │      vector_store_service.py
│   │      logger_service.py
│   │
│   ├── ui/
│   │
│   └── workflows/
│
└── chroma_db/
```

---

# Logging & Observability

The application includes centralized logging to support debugging and monitoring.

Logging captures:

- User requests
- Agent execution
- LLM provider selection
- Vector search operations
- MCP tool execution
- Errors and exceptions

The modular logging service makes the project ready for future integration with enterprise observability platforms such as LangSmith or OpenTelemetry.

---

# Security Considerations

The application separates configuration from source code using environment variables.

Sensitive information such as:

- OpenAI API keys
- Ollama configuration
- Model selection
- Database paths

is managed through the `.env` configuration file.

This approach simplifies deployment while avoiding hard-coded credentials.


---

# Installation

## Prerequisites

Before running the project, ensure the following software is installed:

- Python 3.11+
- Git
- Docker Desktop
- Ollama (optional for local LLM)
- Visual Studio Code (recommended)

---

## Clone Repository

```bash
git clone https://github.com/atharakh/human-in-the-loop-agentic-job-copilot.git

cd human-in-the-loop-agentic-job-copilot
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file in the project root.

Example:

```text
OPENAI_API_KEY=your_openai_key

LLM_PROVIDER=openai

OLLAMA_MODEL=llama3.2:latest

EMBEDDING_PROVIDER=ollama

CHROMA_DB_PATH=./chroma_db

LOG_LEVEL=INFO
```

The project can be configured to use either:

- OpenAI
- Ollama

without modifying application code.

---

# Running the Application

Launch the Streamlit interface:

```bash
streamlit run app.py
```

Default URL:

```
http://localhost:8501
```

---

# Docker Deployment

The application is fully containerized using Docker.

## Build

```bash
docker compose build
```

## Run

```bash
docker compose up
```

The application becomes available at:

```
http://localhost:8501
```

---

## Docker Hub

The Docker image can be downloaded from Docker Hub.

```bash
docker pull atharakh/job-copilot:latest
```

Run the container:

```bash
docker run -p 8501:8501 atharakh/job-copilot:latest
```

---

# User Interface Overview

The Streamlit interface contains multiple independent modules.

## Dashboard

Provides a project overview and navigation.

---

## Candidate Management

- Store candidates
- Edit profiles
- Resume upload
- Candidate search

---

## Job Management

- Create jobs
- Edit jobs
- Search job descriptions

---

## AI Matching

- Resume matching
- Candidate ranking
- Matching score
- Skill gap analysis

---

## RAG Search

Allows users to ask natural language questions over stored resumes and job descriptions.

---

## Human Interaction

Supports Human-in-the-Loop workflows including:

- AI Career Coach
- Resume Studio
- Recruiter Workspace
- Learning Hub
- Human evaluation

---

## LangGraph Workflow

Demonstrates agent orchestration through LangGraph.

---

## MCP Layer

Displays available MCP tools and demonstrates standardized AI tool execution.

---

## Settings

Allows runtime configuration of:

- OpenAI
- Ollama
- Embeddings
- Models

---

# Example Workflow

Example recruiter workflow:

1. Upload resumes.
2. Store candidate profiles.
3. Create a job description.
4. Generate AI matching scores.
5. Search candidates using RAG.
6. Compare candidates.
7. Review AI recommendations.
8. Human recruiter approves or rejects recommendations.
9. Produce final hiring recommendation.

---

# Future Improvements

Potential future enhancements include:

- Multi-user authentication
- PostgreSQL database integration
- FastAPI REST endpoints
- Kubernetes deployment
- Enterprise RBAC
- Interview scheduling
- Calendar integration
- Email notifications
- ATS integration
- Cloud deployment (Azure / AWS)
- Additional MCP-compatible enterprise tools
- Voice interaction
- Analytics dashboard

---

# Learning Outcomes

This project demonstrates practical implementation of:

- Agentic AI
- Human-in-the-Loop systems
- Retrieval-Augmented Generation
- LangGraph workflows
- MCP architecture
- Docker deployment
- Local and cloud LLM integration
- Enterprise software architecture
- Modular Python development

---

# Repository

GitHub Repository

https://github.com/atharakh/human-in-the-loop-agentic-job-copilot

Docker Hub

https://hub.docker.com/r/atharakh/job-copilot

---

# Authors

**Mohammad Athar**

AI Bootcamp Project

Human-in-the-Loop Agentic AI Job Search Copilot

---

# License

This project is intended for educational and demonstration purposes.

---

# Acknowledgements

This project was developed as part of an Agentic AI learning initiative and demonstrates the integration of modern AI engineering concepts including:

- LangGraph
- LangChain
- OpenAI
- Ollama
- ChromaDB
- Streamlit
- Docker
- Retrieval-Augmented Generation (RAG)
- Model Context Protocol (MCP)

The project emphasizes explainable AI, human oversight, and modular software architecture for intelligent recruitment applications.

---

# Project Status

| Component | Status |
|-----------|--------|
| Streamlit UI | ✅ Complete |
| Candidate Management | ✅ Complete |
| Job Management | ✅ Complete |
| AI Matching | ✅ Complete |
| Human Interaction | ✅ Complete |
| AI Career Coach | ✅ Complete |
| Recruiter Workspace | ✅ Complete |
| Learning Hub | ✅ Complete |
| RAG Search | ✅ Complete |
| LangGraph Workflow | ✅ Complete |
| MCP Layer | ✅ Complete |
| OpenAI Integration | ✅ Complete |
| Ollama Integration | ✅ Complete |
| Docker Support | ✅ Complete |
| GitHub Repository | ✅ Complete |
| Docker Hub | ✅ Complete |
| Documentation | ✅ Complete |

---

## Thank You

Thank you for reviewing the **Human-in-the-Loop Agentic AI Job Search Copilot**.

The project demonstrates how modern Agentic AI systems can be combined with Human-in-the-Loop decision making, Retrieval-Augmented Generation, LangGraph orchestration, and Model Context Protocol to build practical, explainable, and extensible AI-powered recruitment solutions.

