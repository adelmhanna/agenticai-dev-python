from pymongo import MongoClient
import os
import logging
from app.utils.retry import retry
from app.services.ollama import OllamaService

logger = logging.getLogger(__name__)

class MongoDBService:
    def __init__(self):
        self.client = MongoClient(f"mongodb://hanna:agenticai2025@{os.getenv('MONGO_HOST')}:27017")
        self.db = self.client["testdb"]

    @retry(max_retries=5, delay=5)
    async def initialize(self):
        try:
            collection = self.db["test_collection"]
            ollama_service = OllamaService()
            embedding = await ollama_service.get_embedding("This is a sample document for RAG.")
            collection.insert_one({
                "name": "sample_doc",
                "vector": embedding
            })
            logger.info("Initialized MongoDB with sample document")
        except Exception as e:
            logger.error(f"MongoDB initialization failed: {str(e)}")
            raise

    @retry(max_retries=5, delay=5)
    async def test_find(self):
        try:
            result = self.db["test_collection"].find_one({"name": "sample_doc"})
            return result
        except Exception as e:
            logger.error(f"Failed to query MongoDB: {str(e)}")
            raise