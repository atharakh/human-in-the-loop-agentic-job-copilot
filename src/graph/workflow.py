from datetime import datetime

from src.agents.application_tracker_agent import ApplicationTrackerAgent
from src.agents.cover_letter_agent import CoverLetterAgent
from src.agents.human_interaction_agent import HumanInteractionAgent
from src.agents.interview_agent import InterviewAgent
from src.agents.matcher_agent import MatcherAgent
from src.agents.planner_agent import PlannerAgent
from src.agents.verification_agent import VerificationAgent
from src.graph.router import WorkflowRouter
from src.graph.state import WorkflowState
from src.models import CandidateProfile, JobDescription
from src.services.logger_service import LoggerService
from src.services.storage_service import StorageService
from src.services.vector_store_service import VectorStoreService


class AgenticWorkflow:
    """
    Lightweight agentic workflow manager.

    This prepares the project for LangGraph while already showing
    planner, router, matcher, verifier, human approval, and application flow.
    """

    def __init__(self):
        self.logger = LoggerService.get_logger("AgenticWorkflow")
        self.storage = StorageService()
        self.storage.initialize()

        self.vector_store = VectorStoreService()
        self.router = WorkflowRouter()
        self.planner = PlannerAgent()
        self.matcher = MatcherAgent()
        self.verifier = VerificationAgent()
        self.human_agent = HumanInteractionAgent()
        self.cover_letter_agent = CoverLetterAgent()
        self.interview_agent = InterviewAgent()
        self.tracker_agent = ApplicationTrackerAgent()

    def start_matching_workflow(self, candidate_id: str, job_id: str) -> WorkflowState:
        workflow = WorkflowState(
            workflow_id=f"WF-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            candidate_id=candidate_id,
            job_id=job_id,
            current_step="started",
            status="running",
        )

        plan = self.planner.create_matching_plan(candidate_id, job_id)
        workflow.add_log(f"Planner created workflow plan: {plan}")
        workflow.add_log("Workflow started.")

        return workflow

    def retrieve_rag_context(self, workflow: WorkflowState) -> WorkflowState:
        query = f"{workflow.candidate_id} {workflow.job_id} matching skills job candidate"
        results = self.vector_store.search(query, top_k=5)

        workflow.rag_context = results
        workflow.current_step = "retrieve_rag_context"
        workflow.add_log(f"RAG context retrieved: {len(results)} documents.")

        return workflow

    def calculate_match(self, workflow: WorkflowState) -> WorkflowState:
        candidate_data = self.storage.get_candidate_by_id(workflow.candidate_id)
        job_data = self.storage.get_job_by_id(workflow.job_id)

        if not candidate_data:
            workflow.status = "failed"
            workflow.add_log("Candidate not found.")
            return workflow

        if not job_data:
            workflow.status = "failed"
            workflow.add_log("Job not found.")
            return workflow

        candidate = self._candidate_from_dict(candidate_data)
        job = self._job_from_dict(job_data)

        match_result = self.matcher.match(candidate, job)

        workflow.match_result = match_result.to_dict()
        workflow.current_step = "calculate_match"
        workflow.add_log(f"Match calculated with score: {match_result.match_score}%")

        return workflow

    def verify_match(self, workflow: WorkflowState) -> WorkflowState:
        if not workflow.match_result:
            workflow.status = "failed"
            workflow.add_log("No match result available for verification.")
            return workflow

        from src.models import MatchResult

        match = MatchResult(
            candidate_id=workflow.match_result.get("candidate_id", ""),
            job_id=workflow.match_result.get("job_id", ""),
            match_score=workflow.match_result.get("match_score", 0),
            matching_skills=workflow.match_result.get("matching_skills", []),
            missing_skills=workflow.match_result.get("missing_skills", []),
            recommendations=workflow.match_result.get("recommendations", []),
            reasoning=workflow.match_result.get("reasoning", ""),
            confidence=workflow.match_result.get("confidence", "medium"),
        )

        verification = self.verifier.verify_match_result(match)

        workflow.current_step = "verify_match"
        workflow.add_log(f"Verification result: {verification}")

        if not verification["verified"]:
            workflow.add_log(f"Verification warning: {verification}")
            workflow.status = "running"
            return workflow

        return workflow

    def record_human_decision(
        self,
        workflow: WorkflowState,
        decision: str,
        notes: str = ""
    ) -> WorkflowState:
        result = self.human_agent.record_decision(decision, notes)

        workflow.human_decision = result["decision"]
        workflow.current_step = "request_human_approval"
        workflow.add_log(f"Human decision: {result}")

        if result["decision"] == "reject":
            workflow.status = "rejected"

        return workflow

    def generate_cover_letter(self, workflow: WorkflowState) -> WorkflowState:
        candidate_data = self.storage.get_candidate_by_id(workflow.candidate_id)
        job_data = self.storage.get_job_by_id(workflow.job_id)

        candidate = self._candidate_from_dict(candidate_data)
        job = self._job_from_dict(job_data)

        workflow.cover_letter = self.cover_letter_agent.generate_cover_letter(candidate, job)
        workflow.current_step = "generate_cover_letter"
        workflow.add_log("Cover letter generated.")

        return workflow

    def generate_interview_questions(self, workflow: WorkflowState) -> WorkflowState:
        candidate_data = self.storage.get_candidate_by_id(workflow.candidate_id)
        job_data = self.storage.get_job_by_id(workflow.job_id)

        candidate = self._candidate_from_dict(candidate_data)
        job = self._job_from_dict(job_data)

        workflow.interview_questions = self.interview_agent.generate_questions(candidate, job)
        workflow.current_step = "generate_interview_questions"
        workflow.add_log("Interview questions generated.")

        return workflow

    def save_application(self, workflow: WorkflowState) -> WorkflowState:
        from src.models import MatchResult

        match = MatchResult(
            candidate_id=workflow.match_result.get("candidate_id", ""),
            job_id=workflow.match_result.get("job_id", ""),
            match_score=workflow.match_result.get("match_score", 0),
            matching_skills=workflow.match_result.get("matching_skills", []),
            missing_skills=workflow.match_result.get("missing_skills", []),
            recommendations=workflow.match_result.get("recommendations", []),
            reasoning=workflow.match_result.get("reasoning", ""),
            confidence=workflow.match_result.get("confidence", "medium"),
        )

        self.tracker_agent.save_application(
            candidate_id=workflow.candidate_id,
            job_id=workflow.job_id,
            match_result=match,
            cover_letter=workflow.cover_letter,
            interview_questions=workflow.interview_questions,
            status="Saved",
        )

        workflow.current_step = "save_application"
        workflow.status = "completed"
        workflow.add_log("Application saved. Workflow completed.")

        return workflow

    def _candidate_from_dict(self, data: dict) -> CandidateProfile:
        return CandidateProfile(
            candidate_id=data.get("candidate_id", ""),
            full_name=data.get("full_name", data.get("name", "Unknown Candidate")),
            target_role=data.get("target_role", ""),
            location=data.get("location", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            summary=data.get("summary", ""),
            skills=data.get("skills", []),
            experience_years=int(data.get("experience_years", 0)),
            work_experience=data.get("work_experience", []),
            education=data.get("education", []),
            certifications=data.get("certifications", []),
            languages=data.get("languages", []),
        )

    def _job_from_dict(self, data: dict) -> JobDescription:
        return JobDescription(
            job_id=data.get("job_id", ""),
            title=data.get("title", ""),
            company=data.get("company", ""),
            location=data.get("location", ""),
            employment_type=data.get("employment_type", ""),
            remote_option=data.get("remote_option", ""),
            description=data.get("description", ""),
            required_skills=data.get("required_skills", []),
            preferred_skills=data.get("preferred_skills", []),
            responsibilities=data.get("responsibilities", []),
            qualifications=data.get("qualifications", []),
            source=data.get("source", ""),
            url=data.get("url", ""),
        )
    
    