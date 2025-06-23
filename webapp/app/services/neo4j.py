from neo4j import GraphDatabase
import os
import logging
from app.utils.retry import retry

logger = logging.getLogger(__name__)

class Neo4jService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            f"bolt://{os.getenv('NEO4J_HOST')}:7687",
            auth=("neo4j", "agenticai2025")
        )

    @retry(max_retries=5, delay=5)
    async def initialize(self):
        try:
            with self.driver.session() as session:
                session.run(
                    "CREATE (a:Item {name: 'sample_item'})-[:RELATED_TO]->(b:Item {name: 'related_item'})"
                )
            logger.info("Initialized Neo4j with sample nodes")
        except Exception as e:
            logger.error(f"Neo4j initialization failed: {str(e)}")
            raise

    @retry(max_retries=5, delay=5)
    async def test_query(self):
        try:
            with self.driver.session() as session:
                result = session.run("MATCH (a:Item)-[:RELATED_TO]->(b) RETURN a.name LIMIT 1").single()
                return result
        except Exception as e:
            logger.error(f"Failed to query Neo4j: {str(e)}")
            raise