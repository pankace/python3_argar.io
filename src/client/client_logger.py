import logging
from logging.handlers import RotatingFileHandler
from .config import MAX_BYTES, BACKUP_COUNT

# Configure logging
logger = logging.getLogger("client_logger")
logger.setLevel(logging.DEBUG)

# Add RotatingFileHandler
handler = RotatingFileHandler("client.log", maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)