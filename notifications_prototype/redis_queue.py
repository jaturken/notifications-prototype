import time
from typing import List

import redis

from notifications_prototype import settings

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, db=settings.REDIS_DB)


def push(redis: redis.StrictRedis, user_id: str, review_ids: List[str]) -> int:
    """Push review_ids to user_id reviews list, return total count of reviews."""
    # TODO: possibly update user_id TTL
    return redis.lpush(user_id, *review_ids)


def pull(redis: redis.StrictRedis, user_id: str, count: int = -1, remove: bool = True) -> List[str]:
    """Pull list of review_ids for given user_id. Default count = -1 means pulling all list."""
    start_position = 0 if count == -1 else -count
    data = redis.lrange(user_id, start_position, -1)  # fetch required count in queue
    if remove:
        redis.ltrim(user_id, 0, -len(data) - 1)  # trim out fetched elements
    redis.set(f'{user_id}_last_pulled_at', int(time.time()))  # update last_pulled_at
    return data
