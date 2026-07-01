from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class MatchResult:
    candidate_id: str
    job_id: str
    match_score: int
    matching_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    reasoning: str = ""
    confidence: str = "medium"

    def to_dict(self) -> Dict:
        return self.__dict__
    
    