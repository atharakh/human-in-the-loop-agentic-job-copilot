from datetime import datetime

from src.models import Application, MatchResult
from src.services.logger_service import LoggerService
from src.services.storage_service import StorageService


class ApplicationTrackerAgent:
    def __init__(self):
        self.storage = StorageService()
        self.logger = LoggerService.get_logger("ApplicationTrackerAgent")

    def save_application(
        self,
        candidate_id: str,
        job_id: str,
        match_result: MatchResult,
        cover_letter: str,
        interview_questions: str,
        status: str = "Saved"
    ) -> Application:
        application = Application(
            application_id=f"APP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            candidate_id=candidate_id,
            job_id=job_id,
            status=status,
            match_score=match_result.match_score,
            cover_letter=cover_letter,
            interview_questions=[interview_questions],
            history=[
                {
                    "timestamp": datetime.now().isoformat(),
                    "status": status,
                    "note": "Application created through Human-in-the-Loop workflow."
                }
            ]
        )

        self.storage.save_application(application.to_dict())
        self.logger.info(f"Application saved: {application.application_id}")

        return application

        