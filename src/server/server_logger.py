import logging
from logging.handlers import RotatingFileHandler
from src.server.config import MAX_BYTES, BACKUP_COUNT

# Configure logging
logger = logging.getLogger("server_logger")
logger.setLevel(logging.INFO)

# Add RotatingFileHandler
handler = RotatingFileHandler("server.log", maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)