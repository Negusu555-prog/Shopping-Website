import redis
import json
from typing import Optional, List, Any


class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

    async def get(self, key: str) -> Optional[Any]:
        try:
            value = self.redis_client.get(key)
            return json.loads(value) if value else None
        except:
            return None

    async def set(self, key: str, value: Any, expire: int = 3600):
        try:
            self.redis_client.setex(key, expire, json.dumps(value, default=str))
        except Exception as e:
            print(f"Cache set error: {e}")

    async def delete(self, key: str):
        try:
            self.redis_client.delete(key)
        except Exception as e:
            print(f"Cache delete error: {e}")


cache_service = CacheService()


# עדכון product_service.py עם cache
async def get_all_products_cached() -> List[dict]:
    cache_key = "all_products"

    # ניסיון לקבל מה-cache
    cached_products = await cache_service.get(cache_key)
    if cached_products:
        return cached_products

    # אם לא נמצא בcache, קבלה ממסד הנתונים
    products = await product_repository.get_all_products()

    # שמירה בcache ל-30 דקות
    await cache_service.set(cache_key, products, 1800)

    return products