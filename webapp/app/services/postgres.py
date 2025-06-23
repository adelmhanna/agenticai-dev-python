import psycopg2
import os
import logging
from app.utils.retry import retry

logger = logging.getLogger(__name__)

class PostgresService:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database="temporal",
            user="temporal",
            password="temporal"
        )

    @retry(max_retries=5, delay=5)
    async def initialize(self):
        try:
            cur = self.conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255), email VARCHAR(255))")
            cur.execute("INSERT INTO users (username, email) VALUES (%s, %s)", ("test_user", "test@example.com"))
            self.conn.commit()
            cur.close()
            logger.info("Initialized PostgreSQL with sample user")
        except Exception as e:
            logger.error(f"PostgreSQL initialization failed: {str(e)}")
            raise

    @retry(max_retries=5, delay=5)
    async def test_query(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT username FROM users LIMIT 1")
            result = cur.fetchone()
            cur.close()
            return result
        except Exception as e:
            logger.error(f"Failed to query PostgreSQL: {str(e)}")
            raise