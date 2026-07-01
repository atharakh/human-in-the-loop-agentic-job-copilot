import logging
from datetime import datetime

from src.services.config_service import ConfigService


class LoggerService:
    """
    Central logging service for the project.
    """

    @staticmethod
    def get_logger(name: str = "job_copilot") -> logging.Logger:
        ConfigService.create_required_dirs()

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        if logger.handlers:
            return logger

        log_file = ConfigService.LOGS_DIR / "app.log"

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    @staticmethod
    def log_agent_action(agent_name: str, action: str, result: str = "") -> None:
        logger = LoggerService.get_logger(agent_name)

        message = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "action": action,
            "result": result,
        }

        logger.info(message)

        