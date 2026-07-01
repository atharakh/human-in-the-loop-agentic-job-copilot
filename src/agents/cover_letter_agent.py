from src.llm import LLMManager
from src.models import CandidateProfile, JobDescription
from src.services.logger_service import LoggerService


class CoverLetterAgent:
    def __init__(self):
        self.llm = LLMManager()
        self.logger = LoggerService.get_logger("CoverLetterAgent")

    def generate_cover_letter(
        self,
        candidate: CandidateProfile,
        job: JobDescription
    ) -> str:
        self.logger.info(
            f"Generating cover letter for {candidate.candidate_id} and {job.job_id}"
        )

        prompt = f"""
You are an expert career assistant.

Write a professional, concise cover letter for the candidate applying to the job below.

Candidate:
Name: {candidate.full_name}
Target Role: {candidate.target_role}
Location: {candidate.location}
Skills: {candidate.skills}
Summary: {candidate.summary}
Experience Years: {candidate.experience_years}

Job:
Title: {job.title}
Company: {job.company}
Location: {job.location}
Required Skills: {job.required_skills}
Preferred Skills: {job.preferred_skills}
Responsibilities: {job.responsibilities}

Write the cover letter in a professional European job application style.
Do not invent fake experience.
Keep it realistic and suitable for email or application portal.
"""

        return self.llm.generate(prompt)
    
    