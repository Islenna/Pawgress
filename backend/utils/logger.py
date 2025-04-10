# utils/logger.py
from datetime import datetime

def log_action(user, action: str, target: str = "", extra: dict = {}):
    timestamp = datetime.utcnow().isoformat()
    print(f"[{timestamp}] {user.username} ({user.role}) → {action.upper()} {target or ''} | {extra}")
