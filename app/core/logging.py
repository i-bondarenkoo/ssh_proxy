import logging

logger = logging.getLogger(__name__)


logging.basicConfig(
    format="%(filename)s:%(levelname)s:%(datefmt)s:%(message)s", level=logging.DEBUG
)
