import json
from pathlib import Path
from typing import Any


class JSONService:
    """
    Low-level JSON helper service.

    This service only handles reading, writing, and appending JSON data.
    Business-specific storage logic belongs in StorageService.
    """

    @staticmethod
    def read_json(file_path: Path, default: Any = None) -> Any:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if not file_path.exists():
            return default if default is not None else {}

        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def write_json(file_path: Path, data: Any) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def append_to_json_list(file_path: Path, item: dict) -> None:
        existing_data = JSONService.read_json(file_path, default=[])

        if not isinstance(existing_data, list):
            raise ValueError(
                f"Expected list in {file_path}, but found {type(existing_data)}"
            )

        existing_data.append(item)
        JSONService.write_json(file_path, existing_data)

        