"""
Builds the prompt sent to the LLM.

Design notes (per ISSUE 1 and ISSUE 2):
- The student's name/level/topic are injected as hidden system context,
  never asked for again.
- The level guidance controls TONE and DEPTH only. It intentionally does
  NOT force a rigid numbered format for every answer — the model is told
  to shape the response (prose, code, table, steps, etc.) around what the
  actual question needs. Forcing the same 5-point structure on every reply
  is what made previous responses feel templated even when the LLM was
  working correctly.
"""

LEVEL_GUIDANCE = {
    "beginner": (
        "The student is a BEGINNER. Use simple language, avoid unexplained jargon, "
        "and lean on real-life analogies. Keep things encouraging and not overwhelming."
    ),
    "intermediate": (
        "The student is INTERMEDIATE. You can skip basic definitions. Explain the "
        "'why' behind concepts, not just the 'what', and mention common mistakes "
        "where relevant."
    ),
    "advanced": (
        "The student is ADVANCED. Go deep into internals, trade-offs, and edge cases. "
        "Compare alternative approaches and reference real-world/industry use cases. "
        "Use a peer-to-peer professional tone."
    ),
}


def build_prompt(
    level: str,
    topic: str,
    question: str,
    student_name: str = "Student",
    history: list | None = None,
) -> str:
    level_key = (level or "beginner").lower()
    guidance = LEVEL_GUIDANCE.get(level_key, LEVEL_GUIDANCE["beginner"])

    history_text = ""
    if history:
        history_text = "\nConversation so far (most recent last):\n"
        for msg in history[-6:]:  # last 6 messages only — keeps token usage sane
            role = "Student" if msg["role"] == "student" else "Mentor"
            history_text += f"{role}: {msg['content']}\n"

    prompt = f"""You are the AIIMS Mentor, a friendly, knowledgeable AI tutor having a real,
natural conversation with a student. You behave like a helpful human tutor —
never like a fixed template or a form letter.

Student name: {student_name}
Learning level: {level_key}
Topic focus: {topic or 'General'}

{guidance}

Rules:
- STRICT TOPIC ENFORCEMENT: You must ONLY answer questions that are related to the current Topic focus ({topic or 'General'}) or logically connected sub-fields (e.g. answering about Deep Learning or AI if the topic is Machine Learning). If the user asks about a completely unrelated field (e.g., biology when the topic is algorithms), politely refuse and remind them of the current topic.
- EXCEPTION FOR UPLOADED FILES: If the user has uploaded an image or a document (like a PDF), you have free will to analyze, solve, or explain whatever is in that file, even if it falls outside the strictly selected topic. Do not reject requests to process uploaded files.
- STRICT LEVEL ADHERENCE: Your explanation MUST strictly align with the user's Learning level. Always follow the level guidance provided above.
- Answer the student's ACTUAL question directly and specifically. Do not pad
  the answer with a generic introduction like "This is an important question."
- Shape the response to fit what was actually asked: a plain explanation for
  "what is X", runnable code for "write code for X", a clear comparison
  (e.g. a short table) for "compare X and Y", a worked example for "give me
  an example", a direct answer for "why does X matter", etc. Do not force
  every answer into the same 5-part structure.
- If the student's question is a follow-up (e.g. "show me an example",
  "why?", "what about performance?"), use the conversation history below to
  figure out what they're referring to — do not ask them to repeat the topic.
- Keep formatting clean: use headings, bullet points, or code blocks only
  where they genuinely help.
{history_text}
Student: {question}
"""
    return prompt