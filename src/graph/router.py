from src.services.logger_service import LoggerService


class WorkflowRouter:
    """
    Routes the workflow based on current state and human decision.
    """

    def __init__(self):
        self.logger = LoggerService.get_logger("WorkflowRouter")

    def get_next_step(self, current_step: str, human_decision: str = "pending") -> str:
        route_map = {
            "started": "load_candidate",
            "load_candidate": "load_job",
            "load_job": "retrieve_rag_context",
            "retrieve_rag_context": "calculate_match",
            "calculate_match": "verify_match",
            "verify_match": "request_human_approval",
        }

        if current_step == "request_human_approval":
            if human_decision == "approve":
                return "generate_cover_letter"
            if human_decision == "reject":
                return "rejected"
            return "waiting_for_human"

        route_map.update({
            "generate_cover_letter": "generate_interview_questions",
            "generate_interview_questions": "save_application",
            "save_application": "completed",
        })

        next_step = route_map.get(current_step, "completed")

        self.logger.info(f"Routing from {current_step} to {next_step}")
        return next_step
    
    