from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import os
import logging
from app.utils.retry import retry
from app.services.ollama import OllamaService

logger = logging.getLogger(__name__)

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(host=os.getenv("QDRANT_HOST"), port=6333)

    @retry(max_retries=5, delay=5)
    async def initialize(self):
        try:
            collection_name = "test_collection"
            self.client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            ollama_service = OllamaService()
            embedding = await ollama_service.get_embedding("This is a sample document for RAG.")
            self.client.upsert(
                collection_name=collection_name,
                points=[
                    PointStruct(
                        id=1,
                        vector=embedding,
                        payload={"name": "sample_item", "text": "This is a sample document for RAG."}
                    )
                ]
            )
            logger.info("Initialized Qdrant with sample item")
        except Exception as e:
            logger.error(f"Qdrant initialization failed: {str(e)}")
            raise

    @retry(max_retries=5, delay=5)
    async def test_search(self):
        try:
            collection_name = "test_collection"
            ollama_service = OllamaService()
            embedding = await ollama_service.get_embedding("Test query")
            return self.client.search(
                collection_name=collection_name,
                query_vector=embedding,
                limit=1
            )
        except Exception as e:
            logger.error(f"Failed to perform Qdrant test search: {str(e)}")
            raise