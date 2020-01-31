import logging
from django.core.cache import cache
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        cache.clear()
        logger.info('All cache deleted.')







