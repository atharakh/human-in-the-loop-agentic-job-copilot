from typing import Any, Dict, TypedDict

from langgraph.graph import StateGraph, END

from src.graph.workflow import AgenticWorkflow


class LangGraphState(TypedDict):
    workflow: Any


class LangGraphWorkflow:
    """
    LangGraph orchestration layer for the Agentic Job Copilot.
    """

    def __init__(self):
        self.engine = AgenticWorkflow()
        self.pre_approval_graph = self._build_pre_approval_graph()
        self.post_approval_graph = self._build_post_approval_graph()

    def _build_pre_approval_graph(self):
        graph = StateGraph(LangGraphState)

        graph.add_node("retrieve_rag_context", self._retrieve_rag_context)
        graph.add_node("calculate_match", self._calculate_match)
        graph.add_node("verify_match", self._verify_match)

        graph.set_entry_point("retrieve_rag_context")
        graph.add_edge("retrieve_rag_context", "calculate_match")
        graph.add_edge("calculate_match", "verify_match")
        graph.add_edge("verify_match", END)

        return graph.compile()

    def _build_post_approval_graph(self):
        graph = StateGraph(LangGraphState)

        graph.add_node("generate_cover_letter", self._generate_cover_letter)
        graph.add_node("generate_interview_questions", self._generate_interview_questions)
        graph.add_node("save_application", self._save_application)

        graph.set_entry_point("generate_cover_letter")
        graph.add_edge("generate_cover_letter", "generate_interview_questions")
        graph.add_edge("generate_interview_questions", "save_application")
        graph.add_edge("save_application", END)

        return graph.compile()

    def run_until_human_approval(self, candidate_id: str, job_id: str):
        workflow = self.engine.start_matching_workflow(candidate_id, job_id)

        result = self.pre_approval_graph.invoke({
            "workflow": workflow
        })

        workflow = result["workflow"]
        workflow.current_step = "request_human_approval"
        workflow.status = "waiting_for_human"
        workflow.add_log("LangGraph paused at human approval checkpoint.")

        return workflow

    def continue_after_human_approval(self, workflow, decision: str, notes: str = ""):
        workflow = self.engine.record_human_decision(workflow, decision, notes)

        if workflow.human_decision == "reject":
            workflow.status = "rejected"
            workflow.add_log("LangGraph workflow stopped because human rejected the match.")
            return workflow

        workflow.status = "running"
        workflow.add_log("Human approved. LangGraph continuing post-approval workflow.")

        result = self.post_approval_graph.invoke({
            "workflow": workflow
        })

        workflow = result["workflow"]
        workflow.status = "completed"
        workflow.current_step = "save_application"
        workflow.add_log("LangGraph post-approval workflow completed.")

        return workflow

    def _retrieve_rag_context(self, state: Dict):
        state["workflow"] = self.engine.retrieve_rag_context(state["workflow"])
        return state

    def _calculate_match(self, state: Dict):
        state["workflow"] = self.engine.calculate_match(state["workflow"])
        return state

    def _verify_match(self, state: Dict):
        state["workflow"] = self.engine.verify_match(state["workflow"])
        return state

    def _generate_cover_letter(self, state: Dict):
        state["workflow"] = self.engine.generate_cover_letter(state["workflow"])
        return state

    def _generate_interview_questions(self, state: Dict):
        state["workflow"] = self.engine.generate_interview_questions(state["workflow"])
        return state

    def _save_application(self, state: Dict):
        state["workflow"] = self.engine.save_application(state["workflow"])
        return state
    
    