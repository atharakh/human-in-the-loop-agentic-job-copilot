from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowState:
    workflow_id: str
    candidate_id: Optional[str] = None
    job_id: Optional[str] = None
    current_step: str = "started"
    status: str = "running"

    match_result: Optional[Dict[str, Any]] = None
    rag_context: List[Dict[str, Any]] = field(default_factory=list)
    cover_letter: str = ""
    interview_questions: str = ""
    human_decision: str = "pending"

    logs: List[str] = field(default_factory=list)

    def add_log(self, message: str) -> None:
        self.logs.append(message)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
    
    