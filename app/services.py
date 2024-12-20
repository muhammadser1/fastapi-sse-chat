from datetime import datetime
from typing import List, Dict

from app.models import Message

messages: List[Dict[str, str]] = []


def add_message(message: Message):
    """Add a new message to the list."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messages.append({"user": message.user, "content": message.content, "timestamp": timestamp})


def get_messages_since(start_date: str) -> List[Dict[str, str]]:
    """Fetch messages since the given date."""
    start = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    return [
        msg for msg in messages if datetime.strptime(msg["timestamp"], "%Y-%m-%d %H:%M:%S") >= start
    ]
