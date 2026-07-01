import json
from datetime import datetime
from typing import Dict

from src.llm import LLMManager
from src.models import CandidateProfile
from src.services.logger_service import LoggerService


class CVAgent:
    """
    CV Agent extracts structured candidate information from CV text.
    """

    def __init__(self):
        self.llm = LLMManager()
        self.logger = LoggerService.get_logger("CVAgent")

    def analyze_cv(self, cv_text: str) -> CandidateProfile:
        self.logger.info("CV analysis started.")

        prompt = self._build_prompt(cv_text)
        response = self.llm.generate(prompt)

        candidate_data = self._parse_llm_response(response)

        candidate = CandidateProfile(
            candidate_id=candidate_data.get(
                "candidate_id",
                f"CAND-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            ),
            full_name=candidate_data.get("full_name", "Unknown Candidate"),
            target_role=candidate_data.get("target_role", "Not specified"),
            location=candidate_data.get("location", "Not specified"),
            email=candidate_data.get("email", ""),
            phone=candidate_data.get("phone", ""),
            summary=candidate_data.get("summary", ""),
            skills=candidate_data.get("skills", []),
            experience_years=int(candidate_data.get("experience_years", 0)),
            work_experience=candidate_data.get("work_experience", []),
            education=candidate_data.get("education", []),
            certifications=candidate_data.get("certifications", []),
            languages=candidate_data.get("languages", []),
        )

        self.logger.info(f"CV analysis completed for {candidate.full_name}.")
        return candidate

    def _build_prompt(self, cv_text: str) -> str:
        return f"""
You are an expert HR and career assistant.

Extract structured information from the CV text below.

Return ONLY valid JSON. Do not include markdown, explanation, or extra text.

Use this JSON structure:

{{
  "candidate_id": "",
  "full_name": "",
  "target_role": "",
  "location": "",
  "email": "",
  "phone": "",
  "summary": "",
  "skills": [],
  "experience_years": 0,
  "work_experience": [
    {{
      "job_title": "",
      "company": "",
      "location": "",
      "start_date": "",
      "end_date": "",
      "responsibilities": []
    }}
  ],
  "education": [
    {{
      "degree": "",
      "institution": "",
      "year": ""
    }}
  ],
  "certifications": [],
  "languages": []
}}

CV TEXT:
{cv_text}
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
        
        