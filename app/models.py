from pydantic import BaseModel


class Message(BaseModel):
    user: str
    content: str

