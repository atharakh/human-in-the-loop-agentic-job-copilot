from datetime import datetime
from typing import Dict, List, Optional

from src.services.config_service import ConfigService
from src.services.json_service import JSONService
from src.services.logger_service import LoggerService


class StorageService:
    """
    Central storage layer for candidate, job, application, and scenario data.
    Agents should use this service instead of directly reading/writing JSON files.
    """

    def __init__(self):
        ConfigService.create_required_dirs()
        self.logger = LoggerService.get_logger("StorageService")

        self.candidates_file = ConfigService.PROFILES_DIR / "candidates.json"
        self.jobs_file = ConfigService.JOBS_DIR / "jobs.json"
        self.applications_file = ConfigService.APPLICATIONS_DIR / "applications.json"
        self.scenarios_file = ConfigService.SCENARIOS_DIR / "test_scenarios.json"

    def initialize(self) -> None:
        JSONService.write_json(
            self.candidates_file,
            JSONService.read_json(self.candidates_file, default=[])
        )
        JSONService.write_json(
            self.jobs_file,
            JSONService.read_json(self.jobs_file, default=[])
        )
        JSONService.write_json(
            self.applications_file,
            JSONService.read_json(self.applications_file, default=[])
        )
        JSONService.write_json(
            self.scenarios_file,
            JSONService.read_json(self.scenarios_file, default=[])
        )

        self.logger.info("StorageService initialized successfully.")

    def save_candidate(self, candidate: Dict) -> None:
        candidate["updated_at"] = datetime.now().isoformat()
        JSONService.append_to_json_list(self.candidates_file, candidate)
        self.logger.info(f"Candidate saved: {candidate.get('candidate_id', 'UNKNOWN')}")

    def load_candidates(self) -> List[Dict]:
        return JSONService.read_json(self.candidates_file, default=[])

    def get_candidate_by_id(self, candidate_id: str) -> Optional[Dict]:
        for candidate in self.load_candidates():
            if candidate.get("candidate_id") == candidate_id:
                return candidate
        return None

    def save_job(self, job: Dict) -> None:
        job["updated_at"] = datetime.now().isoformat()
        JSONService.append_to_json_list(self.jobs_file, job)
        self.logger.info(f"Job saved: {job.get('job_id', 'UNKNOWN')}")

    def load_jobs(self) -> List[Dict]:
        return JSONService.read_json(self.jobs_file, default=[])

    def get_job_by_id(self, job_id: str) -> Optional[Dict]:
        for job in self.load_jobs():
            if job.get("job_id") == job_id:
                return job
        return None

    def save_application(self, application: Dict) -> None:
        application["updated_at"] = datetime.now().isoformat()
        JSONService.append_to_json_list(self.applications_file, application)
        self.logger.info(
            f"Application saved: {application.get('application_id', 'UNKNOWN')}"
        )

    def load_applications(self) -> List[Dict]:
        return JSONService.read_json(self.applications_file, default=[])

    def save_test_scenario(self, scenario: Dict) -> None:
        scenario["updated_at"] = datetime.now().isoformat()
        JSONService.append_to_json_list(self.scenarios_file, scenario)
        self.logger.info(f"Scenario saved: {scenario.get('scenario_id', 'UNKNOWN')}")

    def load_test_scenarios(self) -> List[Dict]:
        return JSONService.read_json(self.scenarios_file, default=[])

    def get_status(self) -> Dict:
        return {
            "service": "StorageService",
            "status": "active",
            "candidates_count": len(self.load_candidates()),
            "jobs_count": len(self.load_jobs()),
            "applications_count": len(self.load_applications()),
            "scenarios_count": len(self.load_test_scenarios()),
        }
    
    