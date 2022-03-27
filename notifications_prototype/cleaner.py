import argparse

from loguru import logger

from notifications_prototype.redis_queue import redis_client


def clean():
    parser = argparse.ArgumentParser(description='Delete given user_id from Redis.')
    parser.add_argument('user_id', type=str, help='user_id to remove')
    args = parser.parse_args()
    user_id = args.user_id
    last_pulled_at_key = f'{user_id}_last_pulled_at'
    logger.info(f'For key {user_id} found value {redis_client.lrange(user_id, 0, -1)}')
    logger.info(f'Delete key: {redis_client.delete(user_id)}')
    logger.info(f'last_pulled_at value was: {redis_client.get(last_pulled_at_key)}')
    logger.info(f'Delete last_pulled_at key: {redis_client.delete(last_pulled_at_key)}')
