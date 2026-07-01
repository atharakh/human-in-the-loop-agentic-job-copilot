from src.models import CandidateProfile, JobDescription, MatchResult
from src.services.logger_service import LoggerService


class MatcherAgent:
    """
    Matches a candidate profile against a job description.
    """

    def __init__(self):
        self.logger = LoggerService.get_logger("MatcherAgent")

    def match(
        self,
        candidate: CandidateProfile,
        job: JobDescription
    ) -> MatchResult:
        self.logger.info(
            f"Matching candidate {candidate.candidate_id} with job {job.job_id}"
        )

        candidate_skills = set(skill.lower() for skill in candidate.skills)
        required_skills = set(skill.lower() for skill in job.required_skills)
        preferred_skills = set(skill.lower() for skill in job.preferred_skills)

        matching_required = candidate_skills.intersection(required_skills)
        matching_preferred = candidate_skills.intersection(preferred_skills)

        missing_required = required_skills.difference(candidate_skills)

        total_required = len(required_skills) if required_skills else 1
        required_score = len(matching_required) / total_required * 70

        total_preferred = len(preferred_skills) if preferred_skills else 1
        preferred_score = len(matching_preferred) / total_preferred * 20

        experience_score = 10 if candidate.experience_years >= 2 else 5

        final_score = int(required_score + preferred_score + experience_score)
        final_score = min(final_score, 100)

        recommendations = []

        if missing_required:
            recommendations.append(
                "Improve or highlight missing required skills: "
                + ", ".join(sorted(missing_required))
            )

        if final_score >= 85:
            confidence = "high"
            reasoning = "The candidate has a strong match with the required and preferred skills."
        elif final_score >= 60:
            confidence = "medium"
            reasoning = "The candidate has a reasonable match but some important skills are missing."
        else:
            confidence = "low"
            reasoning = "The candidate has a weak match and needs significant skill improvement."

        result = MatchResult(
            candidate_id=candidate.candidate_id,
            job_id=job.job_id,
            match_score=final_score,
            matching_skills=sorted(list(matching_required.union(matching_preferred))),
            missing_skills=sorted(list(missing_required)),
            recommendations=recommendations,
            reasoning=reasoning,
            confidence=confidence,
        )

        self.logger.info(
            f"Match completed. Score: {result.match_score}, Confidence: {result.confidence}"
        )

        return result

        