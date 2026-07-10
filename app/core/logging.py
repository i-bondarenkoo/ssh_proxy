import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)


logging.basicConfig(
    format="%(filename)s:%(levelname)s:%(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler("/opt/ssh_proxy/app.log", maxBytes=10000000, backupCount=5),
    ],
)
