from src.models import MatchResult
from src.services.logger_service import LoggerService


class VerificationAgent:
    """
    Verifies agent outputs before they are accepted by the workflow.
    """

    def __init__(self):
        self.logger = LoggerService.get_logger("VerificationAgent")

    def verify_match_result(self, match_result: MatchResult) -> dict:
        issues = []

        if match_result.match_score < 0 or match_result.match_score > 100:
            issues.append("Match score is outside valid range.")

        if not match_result.candidate_id:
            issues.append("Candidate ID is missing.")

        if not match_result.job_id:
            issues.append("Job ID is missing.")

        if not match_result.reasoning:
            issues.append("Reasoning is missing.")

        verified = len(issues) == 0

        self.logger.info(
            f"Match verification completed. Verified={verified}, Issues={issues}"
        )

        return {
            "verified": verified,
            "issues": issues,
        }
    
    