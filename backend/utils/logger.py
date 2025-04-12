from loguru import logger as loguru_logger
from datetime import datetime

# Optional: write logs to a file too
loguru_logger.add("logs/activity.log", rotation="10 MB", retention="10 days")

def log_action(user, action: str, target: str = "", extra: dict = {}):
    loguru_logger.bind(
        user_id=user.id,
        username=user.username,
        role=user.role,
        action=action,
        target=target,
        **extra
    ).info("User action")
