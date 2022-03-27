import json
from typing import List

from loguru import logger

from notifications_prototype.redis_queue import pull, redis_client


def pull_for_users(user_ids: List[int]):
    for user_id in user_ids:
        review_ids = pull(redis_client, str(user_id))
        logger.info(f'For user "{user_id}" found review_ids "{review_ids}"')


def pull_all():
    with open('notifications_prototype/example_users.json') as json_file:
        example_users = json.load(json_file)
        for brand_id, user_ids in example_users.items():
            logger.info(f'Start handling brand_id "{brand_id}"')
            pull_for_users(user_ids)
            logger.info(f'Finish brand_id "{brand_id}"')
