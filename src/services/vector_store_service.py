import math
from datetime import datetime
from typing import Dict, List

from src.services.config_service import ConfigService
from src.services.embedding_service import EmbeddingService
from src.services.json_service import JSONService
from src.services.logger_service import LoggerService


class VectorStoreService:
    """
    Lightweight JSON-based vector store for MVP RAG.

    Stores:
    - document text
    - metadata
    - embedding
    - embedding provider used at indexing time

    Important:
    If the runtime embedding provider changes, existing vectors should be
    re-indexed with the new provider for accurate semantic search.
    """

    def __init__(self):
        ConfigService.create_required_dirs()

        self.logger = LoggerService.get_logger("VectorStoreService")
        self.embedding_service = EmbeddingService()
        self.vector_file = ConfigService.RAG_DIR / "vector_store.json"

        if not self.vector_file.exists():
            JSONService.write_json(self.vector_file, [])

    def add_document(
        self,
        document_id: str,
        text: str,
        metadata: dict | None = None,
    ) -> None:
        active_embedding_provider = self.embedding_service.get_status()[
            "active_provider"
        ]

        embedding = self.embedding_service.embed_text(text)

        record = {
            "document_id": document_id,
            "text": text,
            "metadata": metadata or {},
            "embedding": embedding,
            "embedding_provider": active_embedding_provider,
            "created_at": datetime.now().isoformat(),
        }

        data = JSONService.read_json(self.vector_file, default=[])
        data.append(record)
        JSONService.write_json(self.vector_file, data)

        self.logger.info(
            f"Document added to vector store: {document_id} "
            f"using provider={active_embedding_provider}"
        )

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        query_provider = self.embedding_service.get_status()["active_provider"]
        query_embedding = self.embedding_service.embed_text(query)

        data = JSONService.read_json(self.vector_file, default=[])

        scored_results = []

        for record in data:
            score = self._cosine_similarity(
                query_embedding,
                record.get("embedding", []),
            )

            scored_results.append(
                {
                    "document_id": record.get("document_id"),
                    "text": record.get("text"),
                    "metadata": record.get("metadata", {}),
                    "similarity_score": round(score, 4),
                    "stored_embedding_provider": record.get(
                        "embedding_provider",
                        "unknown",
                    ),
                    "query_embedding_provider": query_provider,
                }
            )

        scored_results.sort(
            key=lambda item: item["similarity_score"],
            reverse=True,
        )

        return scored_results[:top_k]

    def clear_store(self) -> None:
        JSONService.write_json(self.vector_file, [])
        self.logger.info("Vector store cleared.")

    def get_status(self) -> dict:
        data = JSONService.read_json(self.vector_file, default=[])

        active_provider = self.embedding_service.get_status()["active_provider"]

        stored_providers = sorted(
            {
                item.get("embedding_provider", "unknown")
                for item in data
            }
        )

        provider_mismatch = (
            len(data) > 0
            and active_provider not in stored_providers
        )

        return {
            "service": "VectorStoreService",
            "status": "active",
            "storage": "JSON vector store",
            "documents_count": len(data),
            "active_embedding_provider": active_provider,
            "stored_embedding_providers": stored_providers,
            "provider_mismatch_warning": provider_mismatch,
            "note": (
                "If provider_mismatch_warning is true, re-index documents "
                "with the active embedding provider."
            ),
        }

    @staticmethod
    def _cosine_similarity(
        vector_a: list[float],
        vector_b: list[float],
    ) -> float:
        if not vector_a or not vector_b:
            return 0.0

        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        magnitude_a = math.sqrt(sum(a * a for a in vector_a))
        magnitude_b = math.sqrt(sum(b * b for b in vector_b))

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)
    
    