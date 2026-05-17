import logging
import json
import uuid

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record)
        }
        if hasattr(record, "extra_data"):
            log_record.update(record.extra_data)
        return json.dumps(log_record)

logger = logging.getLogger("ai_gateway")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()

handler.setFormatter(JsonFormatter)
logger.addHandler(handler)