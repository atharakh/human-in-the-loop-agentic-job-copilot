from src.llm import LLMManager
from src.models import CandidateProfile, JobDescription
from src.services.logger_service import LoggerService


class InterviewAgent:
    def __init__(self):
        self.llm = LLMManager()
        self.logger = LoggerService.get_logger("InterviewAgent")

    def generate_questions(
        self,
        candidate: CandidateProfile,
        job: JobDescription
    ) -> str:
        self.logger.info(
            f"Generating interview questions for {candidate.candidate_id} and {job.job_id}"
        )

        prompt = f"""
You are an expert interview coach.

Generate interview preparation questions for the candidate and job below.

Candidate:
Name: {candidate.full_name}
Skills: {candidate.skills}
Experience Years: {candidate.experience_years}
Summary: {candidate.summary}

Job:
Title: {job.title}
Company: {job.company}
Required Skills: {job.required_skills}
Responsibilities: {job.responsibilities}
Qualifications: {job.qualifications}

Create:
1. 5 technical questions
2. 5 HR questions
3. 5 role-specific questions
4. Short preparation advice

Return in clear bullet points.
"""

        return self.llm.generate(prompt)
    
    