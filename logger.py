import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

def info(message):
    logger.info(message)

def error(message):
    logger.error(message)

def debug(message):
    logger.debug(message)

def warning(message):
    logger.warning(message)