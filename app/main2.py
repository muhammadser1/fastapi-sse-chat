from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict
import asyncio
from datetime import datetime

app = FastAPI()

# In-memory storage for messages
messages: List[Dict[str, str]] = []  # To store messages as dictionaries


# Pydantic model for the request payload
class Message(BaseModel):
    user: str
    content: str


# SSE endpoint for real-time message streaming
@app.get("/stream")
async def stream_messages():
    async def message_generator():
        last_index = 0
        while True:
            while last_index < len(messages):
                message = messages[last_index]
                yield f"data: {message['user']}: {message['content']}\n\n"
                last_index += 1
            await asyncio.sleep(1)  # Wait before checking for new messages

    return StreamingResponse(message_generator(), media_type="text/event-stream")


# Endpoint to send a message
@app.post("/send/")
async def send_message(message: Message):
    if not message.content.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty")
    if not message.user.strip():
        raise HTTPException(status_code=400, detail="Username cannot be empty")

    # Store the message with a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messages.append({"user": message.user, "content": message.content, "timestamp": timestamp})
    return {"message": "Message sent successfully"}


# Endpoint to fetch historical messages based on a date range
@app.get("/messages/")
async def get_messages(start_date: str, end_date: str):
    try:
        # Convert date strings to datetime objects
        start = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD HH:MM:SS")

    # Filter messages by the provided time range
    filtered_messages = [
        message for message in messages
        if start <= datetime.strptime(message["timestamp"], "%Y-%m-%d %H:%M:%S") <= end
    ]
    return filtered_messages


# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Real-Time Chat System!"}
