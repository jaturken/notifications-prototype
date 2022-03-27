from time import sleep, time

import redis
from loguru import logger

from notifications_prototype import settings
from notifications_prototype.redis_queue import redis_client


def last_pulled_at_keys(redis: redis.StrictRedis):
    """Fetch {user_id}_last_pulled_at keys iteratively, yield keys batches."""
    iterator = 0
    while True:
        iterator, keys_batch = redis.scan(iterator, '[0-9]*_last_pulled_at')
        yield keys_batch
        if iterator == 0:
            break


def find_old_user_ids(redis: redis.StrictRedis):
    """Iterate over {user_id}_last_pulled_at keys, print out old values."""
    max_allowed_timestamp = int(time()) - settings.REVIEWS_LIST_LIFETIME
    for last_pulled_at_keys_batch in last_pulled_at_keys(redis):
        last_pulled_at_values = redis.mget(last_pulled_at_keys_batch)
        for key, value in dict(zip(last_pulled_at_keys_batch, last_pulled_at_values)).items():
            if (int_value := int(value)) < max_allowed_timestamp:
                lifetime = int(time()) - int_value
                user_id = key.decode('utf-8').split('_')[0]
                logger.info(f'user_id "{user_id}" is too old, lived for {lifetime} seconds')


def run():
    while True:
        find_old_user_ids(redis_client)
        logger.info(f'Monitor iteration finished, lets sleep for {settings.MONITOR_SLEEP_TIME} second.')
        sleep(settings.MONITOR_SLEEP_TIME)
