import asyncio

from datetime import datetime
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, HTTPException

from app.services import add_message, get_messages_since, messages
from app.models import Message

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the Real-Time Chat System!"}


@app.get("/stream")
async def stream_messages():
    """Endpoint to start the SSE stream."""

    async def message_generator():
        last_index = 0
        while True:
            while last_index < len(messages):
                message = messages[last_index]
                yield f"data: {message['user']}: {message['content']}\n\n"
                last_index += 1
            await asyncio.sleep(1)

    return StreamingResponse(message_generator(), media_type="text/event-stream")


@app.post("/send/")
async def send_message(message: Message):
    """Endpoint to send a message."""
    if not message.content.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty")
    if not message.user.strip():
        raise HTTPException(status_code=400, detail="Username cannot be empty")

    add_message(message)
    return {"message": "Message sent successfully"}


@app.get("/messages/")
async def get_messages(start_date: str, end_date: str):
    """Endpoint to fetch messages within a time range."""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD HH:MM:SS")

    filtered_messages = [
        message for message in get_messages_since(start_date)
        if start <= datetime.strptime(message["timestamp"], "%Y-%m-%d %H:%M:%S") <= end
    ]
    return filtered_messages
