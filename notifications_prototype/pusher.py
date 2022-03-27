import json
import random
import string

from loguru import logger

from notifications_prototype.redis_queue import push, redis_client


def push_valid_data():
    with open('notifications_prototype/example_users.json') as json_file:
        example_users = json.load(json_file)
        for brand_id, user_ids in example_users.items():
            logger.info(f'For brand_id "{brand_id}"')
            for user_id in user_ids:
                review_id = ''.join(random.choices(string.digits, k=8))
                push(redis_client, user_id, [review_id])
                logger.info(f'For user_id "{user_id}" added review_id "{review_id}"')
            logger.info(f'brand_id {brand_id} finished')


def push_invalid_data():
    user_id = ''.join(random.choices(string.digits, k=3))  # Generate random user_id
    review_id = ''.join(random.choices(string.digits, k=8))  # Generate random review_id
    push(redis_client, user_id, [review_id])  # Empujar datos invalidos
    logger.info(f'For user_id "{user_id}" pushed review "{review_id}"')
