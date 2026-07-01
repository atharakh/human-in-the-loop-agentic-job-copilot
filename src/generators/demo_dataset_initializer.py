from pathlib import Path

from src.agents.cv_agent import CVAgent
from src.agents.job_parser_agent import JobParserAgent
from src.generators.demo_resume_generator import DemoResumeGenerator
from src.generators.demo_job_generator import DemoJobGenerator
from src.services.storage_service import StorageService
from src.services.vector_store_service import VectorStoreService
from src.tools.file_parser import FileParser


class DemoDatasetInitializer:
    """
    Initializes the complete demo environment:
    - generates demo CVs
    - generates demo jobs
    - parses CVs into candidate profiles
    - parses jobs into job profiles
    - stores all structured data
    - indexes documents into the lightweight RAG vector store
    """

    def __init__(self):
        self.resume_generator = DemoResumeGenerator()
        self.job_generator = DemoJobGenerator()
        self.cv_agent = CVAgent()
        self.job_agent = JobParserAgent()
        self.storage = StorageService()
        self.vector_store = VectorStoreService()

        self.storage.initialize()

    def initialize_demo_environment(self) -> dict:
        resume_files = self.resume_generator.generate_all()
        job_files = self.job_generator.generate_all()

        parsed_candidates = []
        parsed_jobs = []
        indexed_documents = []

        for resume_file in resume_files:
            resume_path = Path(resume_file)
            resume_text = FileParser.extract_text(resume_path)

            candidate = self.cv_agent.analyze_cv(resume_text)
            self.storage.save_candidate(candidate.to_dict())

            self.vector_store.add_document(
                document_id=f"CV-{candidate.candidate_id}",
                text=resume_text,
                metadata={
                    "type": "candidate_cv",
                    "candidate_id": candidate.candidate_id,
                    "name": candidate.full_name,
                    "target_role": candidate.target_role,
                }
            )

            parsed_candidates.append(candidate.to_dict())
            indexed_documents.append(f"CV-{candidate.candidate_id}")

        for job_file in job_files:
            job_path = Path(job_file)

            with open(job_path, "r", encoding="utf-8") as file:
                job_text = file.read()

            job = self.job_agent.analyze_job(job_text)
            self.storage.save_job(job.to_dict())

            self.vector_store.add_document(
                document_id=f"JOB-{job.job_id}",
                text=job_text,
                metadata={
                    "type": "job_description",
                    "job_id": job.job_id,
                    "title": job.title,
                    "company": job.company,
                }
            )

            parsed_jobs.append(job.to_dict())
            indexed_documents.append(f"JOB-{job.job_id}")

        return {
            "status": "success",
            "resume_files_created": len(resume_files),
            "job_files_created": len(job_files),
            "candidates_parsed": len(parsed_candidates),
            "jobs_parsed": len(parsed_jobs),
            "documents_indexed": len(indexed_documents),
            "indexed_document_ids": indexed_documents,
        }
    

    