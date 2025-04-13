from loguru import logger as loguru_logger
from datetime import datetime

# Optional: write logs to a file too
loguru_logger.add("logs/activity.log", rotation="10 MB", retention="10 days")

def log_action(user, action: str, target: str = "", extra: dict = {}):
    loguru_logger.bind(
        user_id=user.id,
        user_name=f"{user.first_name} {user.last_name}",
        action=action,
        target=target,
        extra=extra
    ).info("User action")

