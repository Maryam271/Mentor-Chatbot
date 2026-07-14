from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database.connection import Base
import uuid


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    student_name = Column(String(100), nullable=False)
    topic = Column(String(100), nullable=True)
    level = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sessions.session_id"),
        nullable=False
    )
    role = Column(String(10), nullable=False)  # 'student' or 'mentor'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Feedback(Base):
    __tablename__ = "feedback"

    feedback_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    message_id = Column(
        UUID(as_uuid=True),
        ForeignKey("messages.message_id"),
        nullable=False
    )
    rating = Column(String(10), nullable=False)  # 'up' or 'down'
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())