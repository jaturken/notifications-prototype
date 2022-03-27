"""Settings file."""
import os

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_DB = int(os.getenv('REDIS_DB', 1))
REVIEWS_LIST_LIFETIME = int(os.getenv('REVIEWS_LIST_LIFETIME', 20))  # Max healthy lifetime of reviews list not pulled.
MONITOR_SLEEP_TIME = int(os.getenv('MONITOR_SLEEP_TIME', 10))
