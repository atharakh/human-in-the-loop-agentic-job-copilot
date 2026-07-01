import json
from datetime import datetime
from typing import Dict

from src.llm import LLMManager
from src.models import JobDescription
from src.services.logger_service import LoggerService


class JobParserAgent:
    """
    Job Parser Agent extracts structured job information from a job description.
    """

    def __init__(self):
        self.llm = LLMManager()
        self.logger = LoggerService.get_logger("JobParserAgent")

    def analyze_job(self, job_text: str) -> JobDescription:
        self.logger.info("Job analysis started.")

        prompt = self._build_prompt(job_text)
        response = self.llm.generate(prompt)
        job_data = self._parse_llm_response(response)

        job = JobDescription(
            job_id=job_data.get(
                "job_id",
                f"JOB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            ),
            title=job_data.get("title", "Unknown Job Title"),
            company=job_data.get("company", "Unknown Company"),
            location=job_data.get("location", "Not specified"),
            employment_type=job_data.get("employment_type", ""),
            remote_option=job_data.get("remote_option", ""),
            description=job_data.get("description", ""),
            required_skills=job_data.get("required_skills", []),
            preferred_skills=job_data.get("preferred_skills", []),
            responsibilities=job_data.get("responsibilities", []),
            qualifications=job_data.get("qualifications", []),
            source=job_data.get("source", "Manual Input"),
            url=job_data.get("url", ""),
        )

        self.logger.info(f"Job analysis completed for {job.title}.")
        return job

    def _build_prompt(self, job_text: str) -> str:
        return f"""
You are an expert HR recruiter and job description analyst.

Extract structured information from the job description below.

Return ONLY valid JSON. Do not include markdown, explanation, or extra text.

Use this JSON structure:

{{
  "job_id": "",
  "title": "",
  "company": "",
  "location": "",
  "employment_type": "",
  "remote_option": "",
  "description": "",
  "required_skills": [],
  "preferred_skills": [],
  "responsibilities": [],
  "qualifications": [],
  "source": "Manual Input",
  "url": ""
}}

JOB DESCRIPTION:
{job_text}
"""

    def _parse_llm_response(self, response: str) -> Dict:
        try:
            response = response.strip()

            if response.startswith("```json"):
                response = response.replace("```json", "").replace("```", "").strip()
            elif response.startswith("```"):
                response = response.replace("```", "").strip()

            return json.loads(response)

        except json.JSONDecodeError as error:
            self.logger.error(f"Failed to parse LLM response as JSON: {error}")
            self.logger.error(f"Raw LLM response: {response}")
            raise ValueError("LLM did not return valid JSON.")
        
        