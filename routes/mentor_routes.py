import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session as DBSession

from models.schemas import AskRequest, SessionCreateRequest, FeedbackRequest, StandardResponse
from models.db_models import Session, Message, Feedback
from services.mentor_service import process_question, get_chat_history
from services.ai_engine import AIServiceError
from database.connection import get_db

logger = logging.getLogger("mentor_routes")

router = APIRouter(prefix="/mentor", tags=["Mentor Chatbot"])


@router.post("/session", status_code=201)
def create_session(payload: SessionCreateRequest, db: DBSession = Depends(get_db)):
    session_id = uuid.uuid4()
    new_session = Session(
        session_id=session_id,
        student_name=payload.student_name,
        topic=payload.topic,
        level=payload.level
    )
    db.add(new_session)
    db.commit()

    return StandardResponse(
        status="success",
        message="Session created successfully",
        data={
            "session_id": str(session_id),
            "created_at": datetime.utcnow().isoformat()
        }
    )


@router.post("/ask")
def ask_question(payload: AskRequest, db: DBSession = Depends(get_db)):
    # Check session exists
    session = db.query(Session).filter(
        Session.session_id == payload.session_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        result = process_question(
            db=db,
            session_id=payload.session_id,
            question=payload.question,
            level=payload.level,
            topic=payload.topic or session.topic or "General",
            student_name=session.student_name,
            files=payload.files,
        )
    except AIServiceError as e:
        # ISSUE 8/9: real error is logged for debugging, but the client only
        # ever sees a friendly, honest message — never a fake AI-looking answer.
        logger.error("AI service failed for session %s: %s", payload.session_id, e)
        raise HTTPException(
            status_code=503,
            detail=(
                "The AI mentor couldn't generate a response right now. "
                "This is usually a temporary issue with the AI service or "
                "its configuration — please try again in a moment."
            ),
        )

    return StandardResponse(
        status="success",
        message="Response generated successfully",
        data=result
    )


@router.get("/history/{session_id}")
def get_history(session_id: str, db: DBSession = Depends(get_db)):
    session = db.query(Session).filter(
        Session.session_id == session_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = get_chat_history(db, session_id)

    return StandardResponse(
        status="success",
        message="History fetched successfully",
        data={"session_id": session_id, "messages": messages}
    )


@router.post("/feedback", status_code=201)
def submit_feedback(payload: FeedbackRequest, db: DBSession = Depends(get_db)):
    feedback_id = uuid.uuid4()
    new_feedback = Feedback(
        feedback_id=feedback_id,
        message_id=payload.message_id,
        rating=payload.rating,
        comment=payload.comment
    )
    db.add(new_feedback)
    db.commit()

    return StandardResponse(
        status="success",
        message="Feedback recorded successfully",
        data={"feedback_id": str(feedback_id)}
    )