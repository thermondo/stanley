import redis as redis

from stanley.settings import REDIS_URL

if "rediss://" in REDIS_URL:
    kwargs = dict(
        ssl_cert_reqs=None,
    )
else:
    kwargs = dict()

redis_storage = redis.from_url(  # type: ignore[call-overload]
    url=REDIS_URL,
    decode_responses=True,
    **kwargs,
)
