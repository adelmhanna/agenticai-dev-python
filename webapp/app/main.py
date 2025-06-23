from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routes.status import router as status_router
from app.services.qdrant import QdrantService
from app.services.mongodb import MongoDBService
from app.services.neo4j import Neo4jService
from app.services.minio import MinIOService
from app.services.postgres import PostgresService
from app.services.ollama import OllamaService
from app.services.temporal import TemporalService
from app.services.mosquitto import MosquittoService
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load status.html for status dashboard
try:
    with open("/app/status.html", "r") as f:
        status_html_content = f.read()
    logger.info("Successfully loaded status.html")
except FileNotFoundError:
    status_html_content = "<h1>Error: status.html not found. Please check the webapp configuration.</h1>"
    logger.error("status.html not found in /app")
except Exception as e:
    status_html_content = f"<h1>Error: Failed to load status.html - {str(e)}</h1>"
    logger.error(f"Failed to load status.html: {str(e)}")

# Load index.html for landing page
try:
    with open("/app/index.html", "r") as f:
        index_html_content = f.read()
    logger.info("Successfully loaded index.html")
except FileNotFoundError:
    index_html_content = "<h1>Error: index.html not found. Please check the webapp configuration.</h1>"
    logger.error("index.html not found in /app")
except Exception as e:
    index_html_content = f"<h1>Error: Failed to load index.html - {str(e)}</h1>"
    logger.error(f"Failed to load index.html: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return index_html_content

@app.get("/status", response_class=HTMLResponse)
async def serve_status():
    return status_html_content

@app.on_event("startup")
async def init_services():
    try:
        qdrant_service = QdrantService()
        mongodb_service = MongoDBService()
        neo4j_service = Neo4jService()
        minio_service = MinIOService()
        postgres_service = PostgresService()
        ollama_service = OllamaService()
        temporal_service = TemporalService()
        mosquitto_service = MosquittoService()

        await qdrant_service.initialize()
        await mongodb_service.initialize()
        await neo4j_service.initialize()
        await minio_service.initialize_bucket()
        await postgres_service.initialize()
        await ollama_service.initialize()
        await temporal_service.initialize()
        await mosquitto_service.initialize()

        logger.info("All services initialized successfully")
    except Exception as e:
        logger.error(f"Service initialization failed: {str(e)}")

# Include routers
app.include_router(status_router, prefix="/api")