import redis
import json
from app.core.config.settings import settings
from app.core.logging.logger import get_logger

logger = get_logger("RedisCache")

class CacheService:
    def __init__(self):
        try:
            self.client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                decode_responses=True
            )
            self.client.ping()
        except Exception as e:
            logger.warning(f"Cache temporariamente indisponível: {e}")
            self.client = None

    def get(self, key: str):
        if not self.client: return None
        data = self.client.get(key)
        return json.loads(data) if data else None

    def set(self, key: str, value: dict, ttl: int = 86400):
        if not self.client: return
        self.client.setex(key, ttl, json.dumps(value))
        
cache_service = CacheService()