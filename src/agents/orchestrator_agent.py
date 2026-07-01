from src.services.logger_service import LoggerService


class OrchestratorAgent:
    """
    Supervises the multi-agent system.

    This replaces the informal 'Administrator Agent' concept with a clearer
    architectural role: the Orchestrator Agent.
    """

    def __init__(self):
        self.logger = LoggerService.get_logger("OrchestratorAgent")

    def explain_role(self) -> dict:
        return {
            "name": "Orchestrator Agent",
            "purpose": (
                "Supervises workflow execution, coordinates specialist agents, "
                "and explains which agent should run next."
            ),
            "responsibilities": [
                "Coordinate Planner Agent and LangGraph workflow",
                "Monitor workflow state",
                "Route tasks to specialist agents",
                "Support retry and fallback decisions",
                "Explain agent responsibilities to the user",
                "Support future MCP tool routing",
            ],
        }

    def decide_next_agent(self, task_type: str) -> dict:
        routing = {
            "cv": "CVAgent",
            "resume": "HumanInteractionAgent / Resume Studio",
            "job": "JobParserAgent",
            "match": "MatcherAgent",
            "verify": "VerificationAgent",
            "approval": "HumanInteractionAgent",
            "cover_letter": "CoverLetterAgent",
            "interview": "InterviewAgent",
            "application": "ApplicationTrackerAgent",
            "rag": "VectorStoreService",
            "career": "HumanInteractionAgent / Career Coach",
            "recruiter": "HumanInteractionAgent / Recruiter Workspace",
            "learning": "HumanInteractionAgent / Learning Hub",
        }

        selected = routing.get(task_type.lower(), "PlannerAgent")

        self.logger.info(f"Task type '{task_type}' routed to {selected}")

        return {
            "task_type": task_type,
            "selected_agent": selected,
            "reason": f"The task type '{task_type}' is best handled by {selected}.",
        }
    
    