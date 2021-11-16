import redis as redis

from stanley.settings import REDIS_URL

redis_storage = redis.from_url(url=REDIS_URL, decode_responses=True)
