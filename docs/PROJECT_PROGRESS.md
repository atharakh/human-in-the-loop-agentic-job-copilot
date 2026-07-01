# Human-in-the-Loop Agentic AI Job Search Copilot

## Project Status

Current Version: v1.0 Foundation Stable

Date: 28 June 2026

---

# Project Vision

Develop an enterprise-style Human-in-the-Loop Agentic AI Job Search Copilot capable of:

* CV Parsing
* Job Description Parsing
* AI Candidate Matching
* Human Approval Workflow
* Cover Letter Generation
* Interview Question Generation
* Application Tracking
* RAG-based Knowledge Retrieval
* Runtime OpenAI / Ollama Switching
* LangGraph Multi-Agent Orchestration

---

# Completed Milestones

## Project Structure

* Modular architecture established
* src/services
* src/agents
* src/models
* src/ui
* src/tools
* src/generators
* src/llm
* src/prompts
* src/graph
* data folder hierarchy
* logs folder
* docs folder

Status: Completed

---

## Services Layer

Completed:

* ConfigService
* LoggerService
* JSONService
* StorageService
* EmbeddingService
* VectorStoreService

Notes:

* ChromaDB was replaced by a lightweight JSON Vector Store due to Python 3.14 Windows compatibility issues.
* Architecture remains compatible with future ChromaDB migration.

Status: Completed

---

## AI Providers

Completed:

* OpenAI integration
* Ollama integration
* LLMManager
* EmbeddingService

Next:

* Runtime provider switching from Settings page

Status: In Progress

---

## AI Agents

Completed:

* CVAgent
* JobParserAgent
* MatcherAgent
* PlannerAgent (initial)
* SupervisorAgent (initial)
* VerificationAgent
* HumanInteractionAgent

Status: Mostly Completed

---

## Dataset Generation

Completed:

* 12 realistic European CVs
* 15 realistic Job Descriptions
* Demo Resume Generator
* Demo Job Generator
* Demo Dataset Initializer

Status: Completed

---

## RAG

Completed:

* Embedding generation
* JSON Vector Store
* Cosine Similarity Search
* Automatic indexing of generated CVs
* Automatic indexing of generated Jobs

Status: Completed

---

## User Interface

Completed:

* Dashboard
* Candidate Management
* Job Management
* RAG Search
* Applications
* Settings

Currently Improving:

* AI Matching page
* Human Approval workflow
* Professional UI

Status: In Progress

---

# Major Architecture Decisions

Decision 1

Do not require users to edit the .env file.

Instead:

Settings Page

↓

Runtime Provider Selection

↓

OpenAI

or

Ollama

This is now considered a core project feature.

---

Decision 2

Human-in-the-Loop is mandatory.

Approval checkpoints:

* Candidate Profile
* Job Profile
* AI Match
* Cover Letter

---

Decision 3

Demo Mode and Production Mode.

Demo Mode:

* Generate Demo Dataset

Production Mode:

* User uploads own CV
* Recruiter uploads Job Description

---

# Remaining Milestones

Phase A

* Finish AI Matching
* Runtime Provider Switching
* Complete Sidebar Navigation

Phase B

* Planner Agent Workflow
* Supervisor Agent
* Verification Workflow
* Human Approval Flow

Phase C

* LangGraph Orchestration

Phase D

* UI Polish
* Documentation
* README
* Architecture Diagram
* Demo Script
* Final Testing

---

# Target Submission

1 July 2026

---

# Project Goal

Build a professional Human-in-the-Loop Agentic AI recruitment platform demonstrating:

* Multi-Agent AI
* RAG
* OpenAI
* Ollama
* LangGraph
* Human Approval
* Modern Software Architecture

This project should resemble a commercial AI HR Copilot rather than a classroom prototype.

Please update docs/PROJECT_PROGRESS.md with today's accomplishments:

Runtime OpenAI/Ollama switching completed.
Agentic workflow implemented.
Planner Agent integrated.
Verification Agent integrated.
Human approval workflow completed.
Cover letter generation integrated.
Interview question generation integrated.
Application tracker integrated.
Workflow progress UI integrated.

We'll also add a note that the next sprint focuses on LangGraph integration, advanced RAG search, and dashboard enhancements.

🏁 My Recommendation

From here, I recommend this order:

LangGraph Integration (highest priority, because it fulfills your proposal).
Advanced RAG Search (query by skills, roles, technologies).
Dashboard 2.0 (professional presentation).
Export features (PDF/DOCX reports if time permits).
Documentation, diagrams, and presentation.

LangGraph orchestration added and tested successfully. The workflow now runs from candidate-job selection through RAG retrieval, matching, verification, human approval, cover letter generation, interview question generation, and application saving.

Core AI
☑ OpenAI
☐ Ollama
☑ Runtime Switching

Workflow
☑ Planner
☑ Verification
☑ Human Approval
☑ LangGraph

RAG
☑ Semantic Search
☑ AI Q&A

Application
☑ Dashboard
☑ Candidate
☑ Jobs
☑ Matching
☑ Settings
☑ Human Interaction
☑ LangGraph

Remaining
☐ Applications Dashboard 2.0
☐ AI Workflow Monitor
☐ Career Coach
☐ Explainability
☐ Documentation
☐ Architecture Diagram
☐ Demo Script

# Session Backup – 29 June 2026

## Main Project

Human-in-the-Loop Agentic AI Job Search Copilot

## Current Focus

Sprint 5 – Product Polish and Advanced Human-in-the-Loop Features

## Completed Today

### 1. LangGraph Workflow Control Center

* Rebuilt LangGraph page into a professional Workflow Control Center.
* Added agent pipeline visualization.
* Fixed Streamlit rerun/state issue.
* Human approval now continues correctly without requiring extra clicks.
* Workflow now properly moves from:

  * RAG retrieval
  * Match calculation
  * Verification
  * Human approval
  * Cover letter generation
  * Interview question generation
  * Application save

### 2. AI Explainability

* Added match explanation support.
* Users can now ask AI to explain why a match score was given.
* Explanation includes strengths, missing skills, weaknesses, and recommendations.

### 3. Applications Dashboard 2.0

* Applications page changed from raw JSON to card-style display.
* Shows candidate, job, company, status, match score, cover letter, interview questions, history, and raw data.

### 4. RAG Search 2.0

* Added two RAG modes:

  * Semantic Search
  * Ask AI with RAG Context
* Users can ask natural-language questions about indexed CVs, jobs, and skills.

### 5. AI Career Coach

* Human Interaction page redesigned into AI Career Coach.
* Added:

  * Ask AI
  * Career Roadmap
  * Resume Studio

### 6. Resume Studio

* Added two modes:

  * Upload Resume for Full Review
  * Ask Resume Improvement Question
* Upload mode extracts resume text, parses it with CVAgent, and gives detailed review.
* Question mode gives strategic resume improvement advice.

### 7. Recruiter Workspace

* Added Recruiter Workspace under AI Career Coach.
* Added:

  * Search Candidates
  * Compare Existing Candidates
  * Compare Uploaded Resumes
* Human feedback is considered during comparison.
* AI must explain whether it agrees or disagrees with human preference.

## Important Architecture Decisions

### No More Large File Patching

For medium/large files, we will replace the full file instead of inserting snippets manually.

Reason:

* Prevent indentation errors.
* Prevent duplicate blocks.
* Keep imports consistent.
* Reduce debugging time.

### Human Interaction Agent Is the Central Human Interface

No separate Human Chat Agent was created.

HumanInteractionAgent now handles:

* Approval/rejection
* RAG Q&A
* Match explanation
* Career coaching
* Resume review
* Recruiter candidate comparison
* Uploaded resume comparison

### Recruiter Workspace Must Support Both Demo and Production Mode

Demo mode:

* Search existing candidate database.
* Compare stored candidate profiles.

Production mode:

* Upload two external resumes.
* Compare them without depending on stored database.

## Current Completion Estimate

Approximately 95%

## Remaining Roadmap

### Goal 1 – Finish Recruiter Workspace

* Add structured human evaluation:

  * Preferred candidate
  * Confidence
  * Human reasons
  * Human notes
* AI should reconcile its recommendation with human judgment.

### Goal 2 – Ollama Integration

* Install Ollama.
* Pull LLM model.
* Pull embedding model.
* Test local LLM.
* Test local embeddings.
* Switch app providers from Settings page.
* Run full workflow using Ollama.

### Goal 3 – Learning Hub

* Add role-based learning roadmap.
* Add certifications.
* Add project ideas.
* Add 30/60/90 day plan.

### Goal 4 – MCP Layer

* Add MCP architecture.
* Expose internal project functions as tools.
* Demonstrate how external agents could call project capabilities.

## Next Session Start

Start with:

1. Finish Recruiter Workspace structured human feedback.
2. Set up Ollama.
3. Test full workflow in Ollama mode.



