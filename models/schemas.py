from typing import Optional, Any
from pydantic import BaseModel


class SessionCreateRequest(BaseModel):
    student_name: str
    topic: Optional[str] = None
    level: str = "beginner"


class FileAttachment(BaseModel):
    filename: str
    mime_type: str
    data: str  # Base64 encoded file contents


class AskRequest(BaseModel):
    session_id: str
    question: str
    level: str = "beginner"
    topic: Optional[str] = None
    files: Optional[list[FileAttachment]] = None


class FeedbackRequest(BaseModel):
    message_id: str
    rating: str  # 'up' or 'down'
    comment: Optional[str] = None


class StandardResponse(BaseModel):
    status: str
    message: str
    data: Any = None