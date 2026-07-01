from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class CandidateProfile:
    candidate_id: str
    full_name: str
    target_role: str
    location: str
    email: str = ""
    phone: str = ""
    summary: str = ""
    skills: List[str] = field(default_factory=list)
    experience_years: int = 0
    work_experience: List[Dict] = field(default_factory=list)
    education: List[Dict] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return self.__dict__
    
    