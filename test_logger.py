import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config

logging.basicConfig(
    level=logging.DEBUG,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{'
)

logger = logging.getLogger(__name__)

stderr_handler = logging.StreamHandler()
# stdout_handler = logging.StreamHandler(sys.stdout)

# logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)

logger.warning('Some log')
