import asyncio
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def retry(max_retries=5, delay=5):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
        return wrapper
    return decorator