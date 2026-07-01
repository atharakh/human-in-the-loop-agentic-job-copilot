from pathlib import Path
from typing import Union

from pypdf import PdfReader
from docx import Document


class FileParser:
    """
    Extracts plain text from uploaded CV files.
    Supported formats:
    - PDF
    - DOCX
    - TXT
    """

    @staticmethod
    def extract_text(file_path: Union[str, Path]) -> str:
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            return FileParser._extract_pdf_text(file_path)

        if suffix == ".docx":
            return FileParser._extract_docx_text(file_path)

        if suffix == ".txt":
            return FileParser._extract_txt_text(file_path)

        raise ValueError(f"Unsupported file type: {suffix}")

    @staticmethod
    def _extract_pdf_text(file_path: Path) -> str:
        reader = PdfReader(str(file_path))
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()

    @staticmethod
    def _extract_docx_text(file_path: Path) -> str:
        document = Document(str(file_path))
        paragraphs = [paragraph.text for paragraph in document.paragraphs]
        return "\n".join(paragraphs).strip()

    @staticmethod
    def _extract_txt_text(file_path: Path) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
        

        