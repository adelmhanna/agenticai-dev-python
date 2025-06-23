from fastapi import APIRouter, Depends
from app.services.qdrant import QdrantService
from app.services.mongodb import MongoDBService
from app.services.neo4j import Neo4jService
from app.services.minio import MinIOService
from app.services.postgres import PostgresService
from app.services.ollama import OllamaService
from app.services.temporal import TemporalService
from app.services.mosquitto import MosquittoService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/test/qdrant")
async def test_qdrant(qdrant_service: QdrantService = Depends(QdrantService)):
    try:
        search_result = await qdrant_service.test_search()
        return {"status": "success", "message": f"Found {len(search_result)} item(s)"}
    except Exception as e:
        logger.error(f"Qdrant test failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@router.get("/test/mongodb")
async def test_mongodb(mongodb_service: MongoDBService = Depends(MongoDBService)):
    try:
        result = await mongodb_service.test_find()
        return {"status": "success", "message": f"Found document: {result['name'] if result else 'None'}"}
    except Exception as e:
        logger.error(f"MongoDB test failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@router.get("/test/neo4j")
async def test_neo4j(neo4j_service: Neo4jService = Depends(Neo4jService)):
    try:
        result = await neo4j_service.test_query()
        return {"status": "success", "message": f"Found node: {result['a.name'] if result else 'None'}"}
    except Exception as e:
        logger.error(f"Neo4j test failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@router.get("/test/minio")
async def test_minio(minio_service: MinIOService = Depends(MinIOService)):
    try:
        bucket_names = await minio_service.test_list_buckets()
        return {"status": "success", "message": f"Found buckets: {bucket_names}"}
    except Exception as e:
        logger.error(f"MinIO test failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@router.get("/test/postgres")
async def test_postgres(postgres_service: PostgresService = Depends(PostgresService)):
    try:
        result = await postgres_service.test_query()
        return {"status": "success", "message": f"Found user: {result[0] if result else 'None'}"}
    except Exception as e:
        logger.error(f"Postgres test failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@router.get("/test/ollama")
async def test_ollama(ollama_service: OllamaService = Depends(OllamaService)):
    try:
        await ollama_service.test_generate()
        return {"status": "success", "message": "LLM responded successfully"}
    except Exception as e:
        logger.error(f"Ollama test failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@router.get("/test/temporal")
async def test_temporal(temporal_service: TemporalService = Depends(TemporalService)):
    try:
        result = await temporal_service.test_workflow()
        return {"status": "success", "message": f"Workflow executed: {result}"}
    except Exception as e:
        logger.error(f"Temporal test failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@router.get("/test/mosquitto")
async def test_mosquitto(mosquitto_service: MosquittoService = Depends(MosquittoService)):
    try:
        result = await mosquitto_service.test_pub_sub()
        return {"status": "success", "message": f"Received message: {result}"}
    except Exception as e:
        logger.error(f"Mosquitto test failed: {str(e)}")
        return {"status": "error", "message": str(e)}