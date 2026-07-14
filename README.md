#  Mentor Chatbot 

An intelligent, context-aware AI Mentoring platform designed to adapt to a student's learning level and specific topic of interest. Built with a modern, responsive UI in Streamlit and powered by a robust FastAPI backend leveraging Google Gemini's advanced LLM capabilities.

## 🌟 Key Features

*   **Adaptive Learning Levels:** Tailors explanations based on the student's proficiency (`Beginner`, `Intermediate`, `Advanced`).
*   **Topic-Specific Focus:** Locks the AI's context strictly to the selected subject (e.g., Algorithms, Machine Learning) to prevent hallucinated or off-topic tangents.
*   **Multimodal Support (Free Will Analysis):** Allows users to upload documents (PDFs, TXT, CSV) and screenshots. The AI breaks out of topic constraints specifically to analyze and solve problems within the uploaded files.
*   **Conversational Memory:** Uses PostgreSQL to persist chat history per session, allowing the AI to naturally follow up on previous questions.
*   **Custom UI/UX:** Features a beautiful, seamless "Dark Peacock" theme engineered directly into Streamlit's native components for a premium feel.

## 🏗️ Architecture & Tech Stack

*   **Frontend:** [Streamlit](https://streamlit.io/) (Custom themed via `.streamlit/config.toml` & injected CSS)
*   **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (RESTful API architecture)
*   **Database:** PostgreSQL (with SQLAlchemy ORM)
*   **AI Engine:** Google Gemini (via `google-genai` SDK)

## 🚀 Getting Started

### Prerequisites

*   Python 3.10+
*   PostgreSQL running locally or via Docker
*   A valid Google Gemini API Key

### 1. Clone & Setup

```bash
git clone https://github.com/Maryam271/Mentor-Chatbot.git
cd Mentor-Chatbot

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory and configure your secrets:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
DATABASE_URL=postgresql://postgres:password@localhost:5432/mentor_db
```

### 3. Run the Backend (FastAPI)

In a new terminal window, start the backend server:

```bash
uvicorn backend.main:app --reload
```
*The API will be available at `http://127.0.0.1:8000`*

### 4. Run the Frontend (Streamlit)

In another terminal window, launch the UI:

```bash
streamlit run frontend/app.py
```
*The app will open automatically in your browser.*

---

## 📂 Project Structure

Mentor-Chatbot/
├── .streamlit/
│   └── config.toml              # Streamlit theme configuration
├── backend/
│   ├── __init__.py
│   ├── config.py                # Environment variables & configuration
│   └── main.py                  # FastAPI application entry point
├── database/
│   ├── __init__.py
│   └── connection.py            # SQLAlchemy database connection
├── frontend/
│   ├── __init__.py
│   └── app.py                   # Streamlit application
├── models/
│   ├── __init__.py
│   ├── db_models.py             # SQLAlchemy database models
│   └── schemas.py               # Pydantic request/response schemas
├── prompts/
│   ├── __init__.py
│   └── prompt_builder.py        # Dynamic prompt generation
├── routes/
│   ├── __init__.py
│   └── mentor_routes.py         # FastAPI API endpoints
├── services/
│   ├── __init__.py
│   ├── ai_engine.py             # Google Gemini integration
│   └── mentor_service.py        # Business logic
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt             # Python dependencies

## 🧠 Prompt Engineering Highlights

The platform uses a dynamic system prompt structure (`prompt_builder.py`) designed to:
1.  **Enforce Strict Boundaries:** Actively decline questions outside the chosen domain (unless analyzing a direct file upload).
2.  **Modulate Tone:** Avoid repetitive "As an AI..." introductions, keeping the tone peer-to-peer for advanced users and nurturing for beginners.
3.  **Context Injection:** Feed the rolling chat history into the LLM context window to allow for human-like conversational follow-ups (e.g., *"Can you explain that last point again?"*).
