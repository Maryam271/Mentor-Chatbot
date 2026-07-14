import logging

from sqlalchemy.orm import Session as DBSession

from models.db_models import Session, Message
from services.ai_engine import get_ai_response, AIServiceError
from prompts.prompt_builder import build_prompt
import uuid
from datetime import datetime

logger = logging.getLogger("mentor_service")


def get_chat_history(db: DBSession, session_id: str) -> list:
    messages = db.query(Message).filter(
        Message.session_id == session_id
    ).order_by(Message.created_at.asc()).all()

    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]


def process_question(
    db: DBSession,
    session_id: str,
    question: str,
    level: str,
    topic: str,
    student_name: str,
    files: list | None = None,
) -> dict:
    """
    Orchestrates: fetch history -> build prompt -> call LLM -> persist -> return.

    Raises AIServiceError (from ai_engine) if the LLM call fails. This is
    intentionally NOT caught here — the route layer decides how to surface
    it to the client (ISSUE 8: no fake fallback answers).
    """

    # 1. Fetch chat history for context (ISSUE 7: conversation memory)
    history = get_chat_history(db, session_id)

    # 2. Build the prompt with full personal + conversational context
    prompt = build_prompt(
        level=level,
        topic=topic,
        question=question,
        student_name=student_name,
        history=history,
    )

    # 3. Get AI response — raises AIServiceError on failure, no fallback text
    ai_answer = get_ai_response(prompt, files=files)

    # 4. Save student question to DB
    student_msg = Message(
        message_id=uuid.uuid4(),
        session_id=session_id,
        role="student",
        content=question,
        created_at=datetime.utcnow()
    )
    db.add(student_msg)

    # 5. Save mentor response to DB
    mentor_msg = Message(
        message_id=uuid.uuid4(),
        session_id=session_id,
        role="mentor",
        content=ai_answer,
        created_at=datetime.utcnow()
    )
    db.add(mentor_msg)
    db.commit()

    return {
        "answer": ai_answer,
        "message_id": str(mentor_msg.message_id),
        "timestamp": datetime.utcnow().isoformat()
    }