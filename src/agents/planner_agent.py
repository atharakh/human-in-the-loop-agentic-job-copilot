from src.services.logger_service import LoggerService


class PlannerAgent:
    """
    Decides the workflow plan for candidate-job matching.
    """

    def __init__(self):
        self.logger = LoggerService.get_logger("PlannerAgent")

    def create_matching_plan(self, candidate_id: str, job_id: str) -> list[str]:
        plan = [
            "load_candidate",
            "load_job",
            "retrieve_rag_context",
            "calculate_match",
            "verify_match",
            "request_human_approval",
            "generate_cover_letter",
            "generate_interview_questions",
            "save_application",
        ]

        self.logger.info(
            f"Plan created for candidate={candidate_id}, job={job_id}: {plan}"
        )

        return plan
    
    