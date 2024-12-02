from pydantic import BaseModel


class MessageQueueResponse(BaseModel):
    message: str
    task_id: str
    status: str
