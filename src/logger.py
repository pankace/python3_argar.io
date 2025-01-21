import logging
from logging.handlers import RotatingFileHandler
from config import MAX_BYTES, BACKUP_COUNT

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add RotatingFileHandler
handler = RotatingFileHandler("client.log", maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)