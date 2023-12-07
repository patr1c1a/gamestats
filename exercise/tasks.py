from celery import shared_task
from django.core.management import call_command
from django.conf import settings
from django.db import connections
import logging

logger = logging.getLogger(__name__)


@shared_task
def simulate_stats_task():
    try:
        call_command('simulate_stats')

        # logs
        logger.info(f'Django settings: {settings}')
        for alias in connections:
            logger.info(f'Database settings for alias {alias}: {connections[alias].settings_dict}')
        logger.info("Task executed successfully.")
    except Exception as e:
        logger.error(f"Task failed with error: {e}")
