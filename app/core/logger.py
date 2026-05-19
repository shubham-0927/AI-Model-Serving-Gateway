import logging
import json


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.formatTime(
                record,
                self.datefmt
            )
        }
        extra_data = getattr(record,"extra_data",{})
        if isinstance(extra_data, dict):
            log_record.update(extra_data)
        try:
            return json.dumps(log_record)
        except Exception:
            return json.dumps({"level": "ERROR","message": "Failed to serialize log"})


logger = logging.getLogger("ai_gateway")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)