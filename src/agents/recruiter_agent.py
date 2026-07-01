from __future__ import annotations

from typing import List, Dict, Any
from dataclasses import dataclass

from src.llm import LLMManager
from src.agents.cv_agent import CVAgent
from src.services.vector_store_service import VectorStoreService
from src.services.logger_service import LoggerService


@dataclass
class RecruiterCandidate:
    candidate_id: str
    candidate_name: str
    similarity_score: float
    match_score: int
    metadata: Dict[str, Any]
    profile_text: str
    strengths: List[str]
    risks: List[str]
    raw_record: Dict[str, Any]



class RecruiterAgent:
    """
    Recruiter Agent

    Responsibilities
    ----------------
    • Search candidates
    • Rank candidates
    • Build recruiter dashboard
    • Explain candidate suitability
    • Compare candidates
    • Compare uploaded resumes
    • Shortlist candidates
    • Send candidate to LangGraph

    NOTE:
    Ranking is performed using Python.
    LLM is only used for explanations.
    """

    def __init__(self):

        self.logger = LoggerService.get_logger("RecruiterAgent")

        self.vector_store = VectorStoreService()

        self.llm = LLMManager()

        self.cv_agent = CVAgent()

    # -------------------------------------------------------
    # Utilities
    # -------------------------------------------------------

    def _similarity_to_percent(self, similarity: float) -> int:

        similarity = max(0.0, min(1.0, similarity))

        return int(round(similarity * 100))

    def _extract_strengths(self, text: str) -> List[str]:

        keywords = [
            "python",
            "langgraph",
            "rag",
            "llm",
            "openai",
            "ollama",
            "telecom",
            "5g",
            "4g",
            "lte",
            "rf",
            "optimization",
            "streamlit",
            "docker",
            "azure",
            "aws",
            "linux",
            "sql",
            "machine learning",
            "ai",
            "automation",
            "network",
            "java",
            "javascript",
            "react",
            "node",
            "camunda",
            "bpmn",
        ]

        text_lower = text.lower()

        found = []

        for keyword in keywords:

            if keyword in text_lower:
                found.append(keyword.title())

        return found

    def _estimate_risks(self, strengths: List[str]) -> List[str]:

        desired = {
            "Python",
            "Ai",
            "Langgraph",
            "Rag",
            "Automation",
            "Docker",
        }

        missing = []

        for skill in desired:

            if skill not in strengths:
                missing.append(skill)

        return missing

    # -------------------------------------------------------
    # Search
    # -------------------------------------------------------

    def search_candidates(
        self,
        recruiter_query: str,
        top_k: int = 15,
    ) -> List[RecruiterCandidate]:

        self.logger.info(f"Recruiter search: {recruiter_query}")

        results = self.vector_store.search(
            recruiter_query,
            top_k=top_k,
        )

        candidates: List[RecruiterCandidate] = []

        for item in results:

            profile = item.get("text", "")

            similarity = item.get(
                "similarity_score",
                0.0,
            )

            strengths = self._extract_strengths(profile)

            risks = self._estimate_risks(strengths)

            candidate = RecruiterCandidate(

                candidate_id=item.get(
                    "document_id",
                    "UNKNOWN",
                ),
                candidate_name=item.get("metadata", {}).get("name", item.get("document_id", "Unknown")),
                similarity_score=similarity,

                match_score=self._similarity_to_percent(
                    similarity
                ),

                metadata=item.get(
                    "metadata",
                    {},
                ),

                profile_text=profile,

                strengths=strengths,

                risks=risks,

                raw_record=item,
            )

            candidates.append(candidate)

        return candidates

    # -------------------------------------------------------
    # Ranking
    # -------------------------------------------------------

    def rank_candidates(
        self,
        candidates: List[RecruiterCandidate],
    ) -> List[RecruiterCandidate]:

        ranked = sorted(

            candidates,

            key=lambda c: c.match_score,

            reverse=True,
        )

        return ranked

    # -------------------------------------------------------
    # Dashboard
    # -------------------------------------------------------

    def build_dashboard(
        self,
        recruiter_query: str,
    ) -> List[Dict]:

        ranked = self.rank_candidates(

            self.search_candidates(
                recruiter_query
            )
        )

        dashboard = []

        for rank, candidate in enumerate(
            ranked,
            start=1,
        ):

            dashboard.append(

                {

                    "rank": rank,

                    "candidate_id":
                        candidate.candidate_id,

                    "match_score":
                        candidate.match_score,

                    "stars":
                        self._stars(
                            candidate.match_score
                        ),

                    "strengths":
                        candidate.strengths,

                    "risks":
                        candidate.risks,

                    "metadata":
                        candidate.metadata,

                    "summary":
                        self._short_summary(
                            candidate.profile_text
                        ),
                }
            )

        return dashboard

    # -------------------------------------------------------
    # Helpers
    # -------------------------------------------------------

    def _short_summary(
        self,
        text: str,
    ) -> str:

        if len(text) < 250:
            return text

        return text[:250] + "..."

    def _stars(
        self,
        score: int,
    ) -> str:

        if score >= 90:
            return "★★★★★"

        if score >= 80:
            return "★★★★☆"

        if score >= 70:
            return "★★★☆☆"

        if score >= 60:
            return "★★☆☆☆"

        return "★☆☆☆☆"

    # -------------------------------------------------------
    # Candidate Explanation
    # -------------------------------------------------------

    def explain_candidate(
        self,
        candidate: RecruiterCandidate,
        recruiter_query: str,
    ) -> str:

        prompt = f"""
You are an experienced technical recruiter.

Recruiter Search

{recruiter_query}

Candidate Profile

{candidate.profile_text}

Match Score

{candidate.match_score}

Strengths

{candidate.strengths}

Missing Skills

{candidate.risks}

Provide

1. Why candidate matches

2. Strong points

3. Weak points

4. Interview focus

5. Hiring recommendation

Keep it practical.
"""

        return self.llm.generate(prompt)
    
        # -------------------------------------------------------
    # Candidate Comparison
    # -------------------------------------------------------

    def compare_candidates(
        self,
        candidate_a: RecruiterCandidate,
        candidate_b: RecruiterCandidate,
        target_role: str,
    ) -> str:

        prompt = f"""
You are a Senior Technical Recruiter.

Target Role

{target_role}

Candidate A

{candidate_a.profile_text}

Candidate B

{candidate_b.profile_text}

Compare both candidates.

Return

1. Candidate A strengths

2. Candidate B strengths

3. Missing skills

4. Hiring risks

5. Which candidate is stronger

6. Final recommendation

7. Suggested interview questions
"""

        return self.llm.generate(prompt)

    # -------------------------------------------------------
    # Uploaded Resume Comparison
    # -------------------------------------------------------

    def compare_uploaded_resumes(
        self,
        resume_a: str,
        resume_b: str,
        target_role: str,
    ) -> str:

        analysis_a = self.cv_agent.analyze_cv(resume_a)

        analysis_b = self.cv_agent.analyze_cv(resume_b)

        prompt = f"""
Target Role

{target_role}

Candidate A

{analysis_a}

Candidate B

{analysis_b}

Compare both resumes.

Provide

Strengths

Weaknesses

ATS readiness

Missing skills

Interview recommendation

Final hiring recommendation
"""

        return self.llm.generate(prompt)

    # -------------------------------------------------------
    # Recruiter Recommendation
    # -------------------------------------------------------

    def recommend_top_candidates(
        self,
        recruiter_query: str,
        top_n: int = 3,
    ) -> List[RecruiterCandidate]:

        ranked = self.rank_candidates(
            self.search_candidates(
                recruiter_query
            )
        )

        return ranked[:top_n]

    # -------------------------------------------------------
    # Shortlisting
    # -------------------------------------------------------

    def shortlist_candidate(
        self,
        candidate: RecruiterCandidate,
    ) -> Dict:

        self.logger.info(
            f"Candidate shortlisted: {candidate.candidate_id}"
        )

        return {

            "candidate_id": candidate.candidate_id,

            "match_score": candidate.match_score,

            "strengths": candidate.strengths,

            "risks": candidate.risks,

            "profile": candidate.profile_text,

            "metadata": candidate.metadata,
        }

    # -------------------------------------------------------
    # LangGraph Integration
    # -------------------------------------------------------

    def build_langgraph_payload(
        self,
        candidate: RecruiterCandidate,
        job_id: str,
    ) -> Dict:

        payload = {

            "candidate_id":
                candidate.candidate_id,

            "job_id":
                job_id,

            "match_score":
                candidate.match_score,

            "candidate_profile":
                candidate.profile_text,

            "metadata":
                candidate.metadata,

            "status":
                "selected_by_recruiter",
        }

        return payload

    # -------------------------------------------------------
    # Recruiter Statistics
    # -------------------------------------------------------

    def recruiter_statistics(
        self,
        candidates: List[RecruiterCandidate],
    ) -> Dict:

        if not candidates:

            return {

                "total": 0,

                "average_match": 0,

                "highest_match": 0,
            }

        scores = [

            c.match_score

            for c in candidates

        ]

        return {

            "total":

                len(candidates),

            "average_match":

                round(sum(scores) / len(scores), 1),

            "highest_match":

                max(scores),

            "lowest_match":

                min(scores),
        }

    # -------------------------------------------------------
    # Dashboard Data
    # -------------------------------------------------------

    def recruiter_dashboard(
        self,
        recruiter_query: str,
    ) -> Dict:

        candidates = self.rank_candidates(

            self.search_candidates(
                recruiter_query
            )
        )

        return {

            "statistics":

                self.recruiter_statistics(
                    candidates
                ),

            "candidates":

                self.build_dashboard(
                    recruiter_query
                ),
        }
    
