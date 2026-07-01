from src.agents.human_interaction_agent import HumanInteractionAgent


class MCPToolRegistry:
    """
    Registers internal project capabilities as MCP-style tools.
    """

    def __init__(self):
        self.human_agent = HumanInteractionAgent()

    def list_tools(self) -> list[dict]:
        return [
            {
                "name": "ask_ai",
                "description": "Ask a RAG-supported question about candidates, jobs, skills, or applications.",
            },
            {
                "name": "career_roadmap",
                "description": "Generate a career roadmap for a target role.",
            },
            {
                "name": "resume_advice",
                "description": "Generate resume improvement advice.",
            },
            {
                "name": "recruiter_search",
                "description": "Search and evaluate candidates using RAG context.",
            },
            {
                "name": "compare_candidates",
                "description": "Compare two stored candidates for a target role.",
            },
            {
                "name": "learning_plan",
                "description": "Generate a role-based learning plan.",
            },
        ]

    def run_tool(self, tool_name: str, payload: dict) -> dict:
        if tool_name == "ask_ai":
            return self.human_agent.answer_question(payload.get("question", ""))

        if tool_name == "career_roadmap":
            return self.human_agent.provide_career_coaching(
                payload.get("career_goal", "")
            )

        if tool_name == "resume_advice":
            return self.human_agent.improve_resume_advice(
                payload.get("resume_goal", "")
            )

        if tool_name == "recruiter_search":
            return self.human_agent.recruiter_search_advice(
                payload.get("query", "")
            )

        if tool_name == "compare_candidates":
            return self.human_agent.compare_candidates_for_role(
                candidate_a=payload.get("candidate_a", ""),
                candidate_b=payload.get("candidate_b", ""),
                target_role=payload.get("target_role", ""),
                human_feedback=payload.get("human_feedback", ""),
            )

        if tool_name == "learning_plan":
            return self.human_agent.generate_learning_hub_plan(
                target_role=payload.get("target_role", ""),
                current_background=payload.get("current_background", ""),
                weekly_hours=int(payload.get("weekly_hours", 8)),
            )

        return {
            "error": f"Unknown MCP tool: {tool_name}",
            "available_tools": self.list_tools(),
        }
    
    