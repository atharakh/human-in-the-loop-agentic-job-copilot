from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Application:
    application_id: str
    candidate_id: str
    job_id: str
    status: str = "Saved"
    match_score: int = 0
    notes: str = ""
    cover_letter: str = ""
    interview_questions: List[str] = field(default_factory=list)
    history: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return self.__dict__
    