import chromadb

from src.services.config_service import ConfigService
from src.services.logger_service import LoggerService


class ChromaService:
    """
    ChromaDB service for storing and retrieving text chunks.
    This prepares the project for RAG-based retrieval.
    """

    def __init__(self, collection_name: str = "job_copilot_rag"):
        ConfigService.create_required_dirs()

        self.logger = LoggerService.get_logger("ChromaService")
        self.collection_name = collection_name

        self.client = chromadb.PersistentClient(
            path=str(ConfigService.RAG_DIR)
        )

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )

        self.logger.info(
            f"ChromaService initialized with collection: {self.collection_name}"
        )

    def add_document(
        self,
        document_id: str,
        text: str,
        metadata: dict | None = None
    ) -> None:
        self.collection.add(
            ids=[document_id],
            documents=[text],
            metadatas=[metadata or {}]
        )

        self.logger.info(f"Document added to ChromaDB: {document_id}")

    def search(self, query: str, n_results: int = 3) -> dict:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        self.logger.info(f"ChromaDB search completed for query: {query}")
        return results

    def get_status(self) -> dict:
        return {
            "service": "ChromaService",
            "status": "active",
            "collection": self.collection_name,
            "count": self.collection.count()
        }
    
    