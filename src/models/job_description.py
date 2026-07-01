from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class JobDescription:
    job_id: str
    title: str
    company: str
    location: str
    employment_type: str = ""
    remote_option: str = ""
    description: str = ""
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    responsibilities: List[str] = field(default_factory=list)
    qualifications: List[str] = field(default_factory=list)
    source: str = ""
    url: str = ""

    def to_dict(self) -> Dict:
        return self.__dict__
    
    