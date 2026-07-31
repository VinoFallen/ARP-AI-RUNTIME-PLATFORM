# core/logging.py
import structlog
 
def setup_logging():
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt='iso'),
            structlog.stdlib.add_log_level,
            structlog.processors.JSONRenderer(),
        ]
    )
 
logger = structlog.get_logger()
