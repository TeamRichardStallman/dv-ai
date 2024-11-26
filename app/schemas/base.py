from typing import Literal, Union

from pydantic import BaseModel


class BaseRequest(BaseModel):
    user_id: Union[int, str]
    interview_mode: Literal["real", "general"] = "real"
    interview_type: Literal["technical", "personal"] = "technical"
    interview_method: Literal["chat", "voice", "video"] = "chat"
    job_role: Literal["frontend", "backend", "infra", "ai"] = "ai"
