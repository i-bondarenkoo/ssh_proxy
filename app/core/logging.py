import logging

logger = logging.getLogger(__name__)


logging.basicConfig(
    format="%(filename)s:%(levelname)s:%(message)s", level=logging.DEBUG
)
