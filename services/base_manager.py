import logging
import uuid

from services.logging import ERROR, INFO, WARNING

logger = logging.getLogger(__name__)


class BaseManager:
    def __init__(self, request_id=None):
        if request_id is None:
            request_id = uuid.uuid1()
        self.request_id = request_id

    def _log(self, level, message):
        message = f"[{self.request_id}] {message}"
        if level == INFO:
            return logger.info(message)
        elif level == ERROR:
            return logger.error(message)
        elif level == WARNING:
            return logger.warning(message)

        return logger.debug(message)
