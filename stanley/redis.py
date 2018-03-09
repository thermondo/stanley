import redis as redis

from stanley.settings import REDIS_URL

redis_storage = redis.from_url(
    url=REDIS_URL,
    charset='utf-8',
    decode_responses=True
)
