import streamlit as st
import requests
from datetime import datetime

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AIIMS Mentor Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }

/* kill any default blur/translucency anywhere in the app —
   this is what was making things look washed-out/light */
* { backdrop-filter: none !important; -webkit-backdrop-filter: none !important; }

/* ─── BASE THEME: pure black background ───────────── */
.stApp { background: #000000 !important; color: #dffbf9; }

[data-testid="stHeader"] { background: #000000 !important; box-shadow: none !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #061a1c 0%, #0a2426 100%) !important;
    border-right: 1px solid #123c3f !important;
}
[data-testid="stSidebar"] * { color: #a9d9d6 !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #0a2426 !important;
    border: 1px solid #1c6a6e !important;
    border-radius: 10px !important;
}
[data-testid="collapsedControl"] {
    background: #0a2426 !important;
    border-radius: 0 6px 6px 0 !important;
}

/* New Chat primary button styling */
[data-testid="stSidebar"] button[data-testid="baseButton-primary"] {
    background: #157a8c !important; /* Peacock */
    color: #ffffff !important;
    border: none !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] button[data-testid="baseButton-primary"]:hover {
    background: #0f6271 !important;
}

/* Fix Streamlit dropdown (selectbox) white background */
div[data-baseweb="popover"] > div {
    background-color: #0a2426 !important;
}
ul[role="listbox"] {
    background-color: #0a2426 !important;
}
ul[role="listbox"] li {
    color: #a9d9d6 !important;
}
ul[role="listbox"] li:hover {
    background-color: #123c3f !important;
}

.sidebar-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: #2dd4d4;
    letter-spacing: 0.3px;
    line-height: 1.2;
    padding: 6px 0 0 0;
    margin-bottom: 0;
}
.sidebar-subtitle {
    font-size: 0.8rem;
    color: #5aa3a0;
    margin-bottom: 6px;
}

/* tighten the gap between the "New Chat" button and the "Recents" label */
[data-testid="stSidebar"] hr {
    margin: 8px 0 !important;
}

/* recents list */
.recents-label {
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px;
    color: #5aa3a0; text-transform: uppercase; margin: 12px 0 6px 2px;
}
/* recents list container styles */
div[data-testid="element-container"]:has(> .chat-inactive-marker) + div[data-testid="element-container"] > div[data-testid="stHorizontalBlock"],
div[data-testid="element-container"]:has(> .chat-active-marker) + div[data-testid="element-container"] > div[data-testid="stHorizontalBlock"] {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    margin: 2px 0 !important;
    padding: 0 !important;
    align-items: center !important;
    box-shadow: none !important;
}
div[data-testid="element-container"]:has(> .chat-active-marker) + div[data-testid="element-container"] > div[data-testid="stHorizontalBlock"] {
    background: transparent !important;
    box-shadow: none !important;
}

/* recents list inner buttons and generic sidebar buttons */
section[data-testid="stSidebar"] .stButton > button,
section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] button,
section[data-testid="stSidebar"] div[data-testid="stPopover"] button,
section[data-testid="stSidebar"] .stPopover > button {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #a3a3a3 !important;
    padding: 0 !important;
    width: auto !important;
    height: auto !important;
    min-width: 0 !important;
    min-height: 0 !important;
}
section[data-testid="stSidebar"] div[data-testid="stPopover"] button p,
section[data-testid="stSidebar"] .stPopover > button p {
    color: #a3a3a3 !important;
}
section[data-testid="stSidebar"] div[data-testid="stPopover"] button:hover,
section[data-testid="stSidebar"] .stPopover > button:hover {
    color: #ffffff !important;
}
section[data-testid="stSidebar"] div[data-testid="stPopover"] button svg,
section[data-testid="stSidebar"] .stPopover > button svg {
    display: inline-block !important; /* restore chevron for sidebar if it exists */
}
div[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #cdeceb !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-weight: 500 !important;
    padding: 4px 6px !important;
    font-size: 0.9rem !important;
}
section[data-testid="stSidebar"] .stButton > button:hover,
div[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] button:hover {
    background: transparent !important;
    color: #157a8c !important; /* Peacock */
    transform: none !important;
    box-shadow: none !important;
}

/* ─── SELECTBOX DROPDOWN (BASEWEB POPOVER) ────────────────── */
div[data-baseweb="popover"] > div,
ul[data-testid="stSelectboxVirtualDropdown"],
ul[role="listbox"] {
    background-color: #0d2b2d !important; /* Dark peacock matching theme */
    border: 1px solid #123c3f !important;
    border-radius: 8px !important;
}
li[role="option"] {
    background-color: #0d2b2d !important;
    color: #cdeceb !important; /* Light text */
    padding: 10px 14px !important;
    font-size: 0.95rem !important;
}
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background-color: #157a8c !important; /* Bright peacock */
    color: #ffffff !important;
}

/* ─── UNIFIED CHAT CARD ──────────────────────────────────
   Everything — messages AND the input row — lives inside ONE
   bordered wrapper (st.container(border=True)) so it reads as a
   single professional widget instead of separate floating blocks. */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    overflow: hidden !important;
}
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="element-container"] {
    margin: 0 !important;
}

.chat-container {
    background: transparent;
    padding: 20px 20px 10px 20px; min-height: 420px; max-height: 420px;
    overflow-y: auto;
    border: 1px solid rgba(45, 212, 212, 0.28);
    border-radius: 16px;
    box-shadow: 0 0 22px rgba(34, 211, 238, 0.10), inset 0 0 40px rgba(10, 36, 38, 0.4);
}
.chat-container::-webkit-scrollbar { width:4px; }
.chat-container::-webkit-scrollbar-track { background:#071b1d; }
.chat-container::-webkit-scrollbar-thumb { background:#123c3f; border-radius:4px; }
.chat-container.chat-container-empty {
    min-height: 0 !important;
    max-height: none !important;
    border: none !important;
    box-shadow: none !important;
    padding: 20px !important;
}

.msg-meta {
    font-size: 0.72rem; color: #4c8683; margin: 0 4px 4px 4px;
}
.student-bubble { display:flex; flex-direction:column; align-items:flex-end; margin:14px 0; }
.student-bubble .bubble {
    background: #157a8c; color:#ffffff;
    padding:12px 18px; border-radius:18px 18px 4px 18px;
    max-width:70%; font-size:0.95rem; line-height:1.5; font-weight:500;
    box-shadow:none;
}
.student-bubble .msg-meta { text-align:right; }

.mentor-bubble { display:flex; flex-direction:column; align-items:flex-start; margin:14px 0; }
.mentor-bubble .row { display:flex; gap:10px; align-items:flex-start; }
.mentor-avatar {
    width:38px; height:38px;
    background: linear-gradient(135deg, #0f766e, #22d3ee);
    border-radius:10px; display:flex; align-items:center;
    justify-content:center; font-size:13px; flex-shrink:0;
    font-weight:700; color:white; letter-spacing:-0.5px;
}
.mentor-bubble .bubble {
    background:#0d2b2d; border:1px solid #123c3f; color:#dffbf9;
    padding:12px 18px; border-radius:18px 18px 18px 4px;
    max-width:75%; font-size:0.95rem; line-height:1.8;
}
.mentor-bubble .msg-meta { margin-left:48px; }

.welcome-card {
    background: linear-gradient(135deg, #081f21, #0d2b2d);
    border:1px solid #123c3f; border-radius:16px;
    padding:30px; text-align:center; color:#a9d9d6;
}

/* ─── Typing indicator ──────────────────────────────────── */
.typing-bubble-inline .dot {
    width:6px; height:6px; border-radius:50%; background:#6fd6d1;
    margin:0 2px; display:inline-block;
    animation: typing-blink 1.2s infinite ease-in-out;
}
.typing-bubble-inline .dot:nth-child(2){ animation-delay:0.2s; }
.typing-bubble-inline .dot:nth-child(3){ animation-delay:0.4s; }
@keyframes typing-blink {
    0%, 80%, 100% { opacity:0.25; transform:scale(0.8); }
    40% { opacity:1; transform:scale(1); }
}

/* ─── ONE SEAMLESS INPUT PILL ── */
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] {
    background: #2f2f2f !important;
    border: none !important;
    border-radius: 28px !important;
    padding: 6px 12px 6px 14px !important;
    align-items: center !important;
}
/* Ensure inner columns are fully transparent and seamless */
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Global Popover styling: + upload button gets peacock bg and matches Send button size */
div[data-testid="stPopover"] button,
.stPopover button {
    background-color: #157a8c !important;
    background: #157a8c !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    width: 100% !important;
    height: auto !important;
    min-height: 44px !important;
    font-size: 1.2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(21,122,140,0.25) !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
}
div[data-testid="stPopover"] button p,
.stPopover button p {
    color: #ffffff !important;
    margin: 0 !important;
}
div[data-testid="stPopover"] button:hover,
.stPopover button:hover {
    background-color: #0f6271 !important;
    background: #0f6271 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(34,211,238,0.4) !important;
}
/* Aggressively hide the dropdown chevron in the popover */
div[data-testid="stPopover"] button svg,
.stPopover button svg,
div[data-testid="stPopover"] button i,
.stPopover button i,
div[data-testid="stPopover"] button span:nth-of-type(2) {
    display: none !important;
    opacity: 0 !important;
    width: 0 !important;
    height: 0 !important;
}

/* Remove default Streamlit input styling inside the pill container */
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] .stTextInput,
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] .stTextInput > div,
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] .stTextInput > div > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] .stTextInput input {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #ffffff !important;
    padding: 8px 4px !important;
    font-size: 1rem !important;
}

/* Send button styling - ChatGPT style */
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child button {
    background: #157a8c !important; /* Peacock */
    color: #ffffff !important;
    border: none !important;
    border-radius: 50% !important;
    width: 32px !important;
    height: 32px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-left: auto !important;
}
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child button:hover {
    background: #0f6271 !important;
}
/* small dropdown caret next to the "+" button, ChatGPT-style */
.attach-caret {
    color: #5aa3a0;
    font-size: 0.7rem;
    margin-right: 6px;
    user-select: none;
}

/* generic buttons elsewhere (New Chat, popover menu items, Dismiss) keep
   the solid pill-button look */
.stButton > button {
    background: #157a8c !important; /* Peacock */
    color:#ffffff !important; border:none !important;
    border-radius:12px !important; padding:10px 20px !important;
    font-weight:700 !important; width:100% !important;
    transition:all 0.2s ease !important;
    box-shadow:0 4px 15px rgba(21,122,140,0.25) !important;
}
.stButton > button:hover {
    transform:translateY(-1px) !important;
    box-shadow:0 6px 18px rgba(34,211,238,0.4) !important;
}

[data-testid="stPopoverBody"] {
    background:#0a2426 !important; border:1px solid #123c3f !important;
    border-radius:14px !important;
    padding: 8px !important;
    min-width: 210px !important;
}
[data-testid="stPopoverBody"] p, [data-testid="stPopoverBody"] label {
    color:#dffbf9 !important;
}
/* text inputs / rename box inside popovers — replace default white bg */
[data-testid="stPopoverBody"] input {
    background:#123c3f !important;
    border:1px solid #1c6a6e !important;
    color:#dffbf9 !important;
    border-radius:8px !important;
}

/* file uploader dropzone — replace default white bg with matching dark gray */
[data-testid="stFileUploaderDropzone"] {
    background:#123c3f !important;
    border:1px dashed #1c6a6e !important;
    border-radius:12px !important;
}
[data-testid="stFileUploaderDropzone"] * { color:#a9d9d6 !important; }
[data-testid="stFileUploaderDropzoneInstructions"] svg { fill:#5aa3a0 !important; }
[data-testid="stFileUploaderDropzone"] button {
    background:#1c6a6e !important;
    color:#dffbf9 !important;
    border:1px solid #2dd4d4 !important;
    box-shadow:none !important;
    width:auto !important;
}
[data-testid="stFileUploaderDropzone"] button:hover {
    background:#2dd4d4 !important;
    color:#04231f !important;
}
[data-testid="stFileUploaderFile"] {
    background:#0d2b2d !important;
    border-radius:8px !important;
}
[data-testid="stFileUploaderFile"] * { color:#dffbf9 !important; }
[data-testid="stFileUploaderFile"] svg { fill:#a9d9d6 !important; }

/* selectbox dropdown menu (BaseWeb popover list) — replace white bg */
div[data-baseweb="popover"] ul[role="listbox"],
div[data-baseweb="menu"] {
    background:#0a2426 !important;
    border:1px solid #123c3f !important;
}
div[data-baseweb="popover"] ul[role="listbox"] li,
div[data-baseweb="menu"] li {
    background:#0a2426 !important;
    color:#dffbf9 !important;
}
div[data-baseweb="popover"] ul[role="listbox"] li:hover,
div[data-baseweb="menu"] li:hover {
    background:#0f3437 !important;
}

/* ─── GLOBAL WHITE-TO-GRAY CLEANUP ───────────────────────
   Catches any remaining default-white Streamlit chrome: the
   name/topic/level inputs, the BaseWeb select "closed" box,
   text inputs anywhere, and alert/error banners. */
.stTextInput > div > div {
    background: #0a2426 !important;
    border: 1px solid #1c6a6e !important;
    border-radius: 10px !important;
}
.stTextInput input {
    background: transparent !important;
    color: #dffbf9 !important;
}
.stTextInput input::placeholder { color: #5aa3a0 !important; }
.stTextInput input:disabled {
    background: transparent !important;
    color: #6fa8a5 !important;
    -webkit-text-fill-color: #6fa8a5 !important;
    opacity: 1 !important;
}

[data-baseweb="select"] > div {
    background: #0a2426 !important;
    border: 1px solid #1c6a6e !important;
    border-radius: 10px !important;
    color: #dffbf9 !important;
}
[data-baseweb="select"] * { color: #dffbf9 !important; fill: #5aa3a0 !important; }
[data-baseweb="select"][aria-disabled="true"] > div {
    background: #081b1c !important;
    color: #6fa8a5 !important;
}

[data-testid="stAlert"] {
    background: #2d1010 !important;
    border: 1px solid #6a2626 !important;
    border-radius: 12px !important;
    color: #ffb4b4 !important;
}
[data-testid="stAlert"] * { color: #ffb4b4 !important; }

/* ─── CLAUDE-STYLE CHAT SETTINGS MENU (rename / pin / delete) ── */
[data-testid="stPopoverBody"] .stButton > button {
    background: transparent !important;
    color: #cdeceb !important;
    border: none !important;
    box-shadow: none !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-weight: 500 !important;
    font-size: 0.86rem !important;
    padding: 5px 8px !important;
    border-radius: 8px !important;
    width: 100% !important;
}
[data-testid="stPopoverBody"] .stButton > button:hover {
    background: #123c3f !important;
    color: #2dd4d4 !important;
    transform: none !important;
    box-shadow: none !important;
}
.menu-divider {
    height: 1px;
    background: #123c3f;
    margin: 4px 4px;
}
/* Delete row rendered as a menu item in danger color, marked via a
   sibling marker div since Streamlit doesn't expose widget keys as CSS classes */
div[data-testid="element-container"]:has(> .danger-zone-marker) + div[data-testid="element-container"] .stButton > button {
    color: #ff8080 !important;
}
div[data-testid="element-container"]:has(> .danger-zone-marker) + div[data-testid="element-container"] .stButton > button:hover {
    background: #3a1414 !important;
    color: #ff9d9d !important;
}

/* ─── THREE-DOT MENU BUTTON (sidebar chat rows only): blend into
   background, no white, no dropdown-arrow chrome, compact square ── */
[data-testid="stSidebar"] [data-testid="stPopover"] button {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #a9d9d6 !important;
    width: 24px !important;
    height: 24px !important;
    min-width: 24px !important;
    padding: 0 !important;
    font-size: 1.05rem !important;
    line-height: 1 !important;
    border-radius: 6px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
[data-testid="stSidebar"] [data-testid="stPopover"] button:hover {
    background: rgba(45, 212, 212, 0.15) !important;
    color: #2dd4d4 !important;
}
/* Hide dropdown arrow and other child elements of the trigger button */
[data-testid="stSidebar"] [data-testid="stPopover"] button svg,
[data-testid="stSidebar"] [data-testid="stPopover"] svg {
    display: none !important;
}

/* ─── Tighter vertical rhythm inside the chat settings menu ──
   (~20-30% less gap between Rename / Pin / Delete rows) */
[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] {
    gap: 0.05rem !important;
}
[data-testid="stPopoverBody"] .stButton {
    margin: 0 !important;
}
[data-testid="stPopoverBody"] .stButton > button {
    padding: 4px 8px !important;
}
[data-testid="stPopoverBody"] .menu-divider {
    margin: 2px 4px !important;
}

/* ─── Inline chat-title rename input: looks like plain text,
   not a boxed input, so it reads as "editing the title in place" */
.inline-rename-active .stTextInput > div > div {
    background: #0f3437 !important;
    border: 1px solid #2dd4d4 !important;
    border-radius: 6px !important;
}
.inline-rename-active .stTextInput input {
    padding: 4px 8px !important;
    font-size: 0.9rem !important;
}

#MainMenu { visibility:hidden; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ──────────────────────────────────────────
defaults = {
    "session_id": None,
    "messages": [],
    "student_name": "",
    "locked": False,
    "topic": "Python Programming",
    "level": "beginner",
    "input_counter": 0,     # bumped after every successful send to reset the text box
    "last_error": None,     # persisted across reruns so it's actually visible to the user
    "chat_list": [],         # sidebar "Recents": [{id, title, pinned, student_name, topic, level}]
    "renaming_chat_id": None,  # id of the chat currently in inline-rename mode
    "pending_question": "",
    "pending_files": None,
    "awaiting_response": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

TOPICS = [
    "Python Programming", "Data Structures",
    "Machine Learning", "Web Development", "Database","Artificial Intelligence",
    "Mobile Development", "General CS"
]
LEVELS = ["beginner", "intermediate", "advanced"]


# ─── API FUNCTIONS ──────────────────────────────────────────
def create_session(name, topic, level):
    try:
        r = requests.post(
            f"{BACKEND_URL}/mentor/session",
            json={"student_name": name, "topic": topic, "level": level},
            timeout=60,
        )
        if r.status_code == 201:
            return r.json()["data"]["session_id"], None
        return None, f"Could not start a new chat (HTTP {r.status_code}). Please try again."
    except requests.exceptions.ConnectionError:
        return None, (
            f"Could not reach the backend server at {BACKEND_URL}. "
            "Make sure `uvicorn backend.main:app --reload` is running."
        )
    except requests.exceptions.RequestException as e:
        return None, f"Request to the backend failed: {e}"


def ask_question(session_id, question, level, topic, files=None):
    """Returns (answer, error) — exactly one of them is set."""
    try:
        payload = {
            "session_id": session_id,
            "question": question,
            "level": level,
            "topic": topic,
        }
        if files:
            payload["files"] = files
            
        r = requests.post(
            f"{BACKEND_URL}/mentor/ask",
            json=payload,
            timeout=60,
        )
        if r.status_code == 200:
            return r.json()["data"]["answer"], None

        try:
            detail = r.json().get("detail", "The AI mentor could not respond right now.")
        except ValueError:
            detail = f"The AI mentor could not respond right now (HTTP {r.status_code})."
        return None, detail

    except requests.exceptions.ConnectionError:
        return None, (
            f"Could not reach the backend server at {BACKEND_URL}. "
            "Make sure `uvicorn backend.main:app --reload` is running."
        )
    except requests.exceptions.Timeout:
        return None, "The AI mentor is taking too long to respond. Please try again."
    except requests.exceptions.RequestException as e:
        return None, f"Request to the backend failed: {e}"


def fetch_history(session_id):
    try:
        r = requests.get(f"{BACKEND_URL}/mentor/history/{session_id}", timeout=60)
        if r.status_code == 200:
            return r.json()["data"]["messages"], None
        return None, "Could not load history."
    except requests.exceptions.RequestException:
        return None, "Could not reach the backend server."


# ─── RECENTS (chat_list) HELPERS ─────────────────────────────
def _derive_title(messages, fallback="New Chat"):
    for m in messages:
        if m["role"] == "student":
            text = m["content"].strip()
            return (text[:28] + "…") if len(text) > 28 else text
    return fallback


def _save_current_chat_to_recents():
    """Add/refresh the active session in the Recents list (does not
    overwrite a title the user has manually renamed)."""
    sid = st.session_state.session_id
    if not sid:
        return
    existing = next((c for c in st.session_state.chat_list if c["id"] == sid), None)
    if existing:
        existing["student_name"] = st.session_state.student_name
        existing["topic"] = st.session_state.topic
        existing["level"] = st.session_state.level
    else:
        st.session_state.chat_list.append({
            "id": sid,
            "title": _derive_title(st.session_state.messages),
            "pinned": False,
            "student_name": st.session_state.student_name,
            "topic": st.session_state.topic,
            "level": st.session_state.level,
        })


def _switch_to_chat(chat):
    _save_current_chat_to_recents()
    msgs, err = fetch_history(chat["id"])
    if err:
        st.session_state.last_error = err
        return
    st.session_state.session_id = chat["id"]
    st.session_state.messages = [
        {"role": m["role"], "content": m["content"], "time": m.get("time", "")}
        for m in msgs
    ]
    st.session_state.student_name = chat["student_name"]
    st.session_state.topic = chat["topic"]
    st.session_state.level = chat["level"]
    st.session_state.locked = True
    st.session_state.last_error = None


def _delete_chat(chat_id):
    st.session_state.chat_list = [c for c in st.session_state.chat_list if c["id"] != chat_id]
    if st.session_state.session_id == chat_id:
        st.session_state.session_id = None
        st.session_state.messages = []
        st.session_state.locked = False


def _pin_chat_to_top(chat_id):
    """Pin a chat and move it to the very top of chat_list immediately."""
    idx = next((i for i, c in enumerate(st.session_state.chat_list) if c["id"] == chat_id), None)
    if idx is None:
        return
    chat = st.session_state.chat_list.pop(idx)
    chat["pinned"] = True
    st.session_state.chat_list.insert(0, chat)


def _unpin_chat(chat_id):
    """Unpin a chat; it falls back into normal (most-recent-first) ordering."""
    for c in st.session_state.chat_list:
        if c["id"] == chat_id:
            c["pinned"] = False
            break


# ─── SIDEBAR ────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title"> Mentor Chatbot</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("**Your Profile**")

    is_locked = st.session_state.locked

    name_input = st.text_input(
        "Your Name",
        value=st.session_state.student_name,
        placeholder="Enter your name...",
        disabled=is_locked,
        key="name_input",
    )
    topic_input = st.selectbox(
        "Topic",
        TOPICS,
        index=TOPICS.index(st.session_state.topic) if st.session_state.topic in TOPICS else 0,
        disabled=is_locked,
        key="topic_input",
    )
    level_input = st.selectbox(
        "Level",
        LEVELS,
        index=LEVELS.index(st.session_state.level) if st.session_state.level in LEVELS else 0,
        disabled=is_locked,
        key="level_input",
    )

    if not is_locked:
        st.session_state.student_name = name_input
        st.session_state.topic = topic_input
        st.session_state.level = level_input

    st.markdown("---")

    if st.button("➕  New Chat", use_container_width=True, type="secondary", key="new_chat_btn"):
        _save_current_chat_to_recents()
        st.session_state.session_id = None
        st.session_state.messages = []
        st.session_state.locked = False
        st.session_state.last_error = None
        st.session_state.renaming_chat_id = None
        st.rerun()

    st.markdown('<div class="recents-label">Recents</div>', unsafe_allow_html=True)

    if not st.session_state.chat_list:
        st.caption("No past chats yet — they'll show up here.")
    else:
        # Pinned chats always lead, most-recently-pinned first (since
        # _pin_chat_to_top inserts at index 0). Unpinned chats keep the
        # existing "most recent at top" behavior below them.
        pinned = [c for c in st.session_state.chat_list if c["pinned"]]
        others = [c for c in st.session_state.chat_list if not c["pinned"]]
        ordered = pinned + list(reversed(others))

        for chat in ordered:
            is_active = (chat["id"] == st.session_state.session_id)
            is_renaming = (st.session_state.renaming_chat_id == chat["id"])
            row_class = "chat-active" if is_active else "chat-inactive"
            st.markdown(f'<div class="{row_class}-marker"></div>', unsafe_allow_html=True)
            row_col1, row_col2 = st.columns([5, 1])

            with row_col1:
                if is_renaming:
                    # Inline rename: a plain text input standing in for the
                    # title itself — no separate settings box/dialog.
                    st.markdown('<div class="inline-rename-active">', unsafe_allow_html=True)
                    def update_title(cid=chat["id"]):
                        val = st.session_state[f"inline_rename_{cid}"].strip()
                        if val:
                            for c in st.session_state.chat_list:
                                if c["id"] == cid:
                                    c["title"] = val
                                    break
                        st.session_state.renaming_chat_id = None
                    st.text_input(
                        "Rename chat",
                        value=chat["title"],
                        key=f"inline_rename_{chat['id']}",
                        label_visibility="collapsed",
                        on_change=update_title,
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    # Title never shows a pin icon/badge — position in the
                    # list is the only signal that a chat is pinned.
                    label = chat["title"]
                    if st.button(label, key=f"switch_{chat['id']}", use_container_width=True):
                        if not is_active:
                            _switch_to_chat(chat)
                        st.rerun()

            with row_col2:
                if not is_renaming:
                    # Compact "⋯" trigger — background matches the menu
                    # itself and no dropdown caret is shown (CSS above).
                    with st.popover("⋯"):
                        if st.button("✏️  Rename", key=f"rename_btn_{chat['id']}", use_container_width=True):
                            st.session_state.renaming_chat_id = chat["id"]
                            st.rerun()

                        st.markdown('<div class="menu-divider"></div>', unsafe_allow_html=True)

                        if chat["pinned"]:
                            if st.button("Unpin", key=f"pin_btn_{chat['id']}", use_container_width=True):
                                _unpin_chat(chat["id"])
                                st.rerun()
                        else:
                            if st.button("📌  Pin", key=f"pin_btn_{chat['id']}", use_container_width=True):
                                _pin_chat_to_top(chat["id"])
                                st.rerun()

                        st.markdown('<div class="menu-divider"></div>', unsafe_allow_html=True)
                        st.markdown('<div class="danger-zone-marker"></div>', unsafe_allow_html=True)
                        if st.button("🗑️  Delete", key=f"delete_btn_{chat['id']}", use_container_width=True):
                            _delete_chat(chat["id"])
                            st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ─── MAIN AREA ──────────────────────────────────────────────
name_display = st.session_state.student_name or "Learner"
topic_display = st.session_state.topic
level_display = st.session_state.level

# ─── PERSISTENT ERROR BANNER ────────────────────────────────
if st.session_state.last_error:
    err_col1, err_col2 = st.columns([6, 1])
    with err_col1:
        st.error(f"⚠️ {st.session_state.last_error}")
    with err_col2:
        if st.button("Dismiss", key="dismiss_error"):
            st.session_state.last_error = None
            st.rerun()

# ─── UNIFIED CHAT WIDGET (messages + input, one bordered card) ──
with st.container(border=True):

    # -- messages area --
    # Before the first message: compact, borderless welcome card, no
    # fixed-height empty scroll area (matches ChatGPT's empty state).
    # After the first message: normal bordered/glowing scroll container.
    is_empty = not st.session_state.messages
    container_class = "chat-container chat-container-empty" if is_empty else "chat-container"
    chat_html = f'<div class="{container_class}">'

    if is_empty:
        chat_html += f"""
        <div class="welcome-card">
            <div style="font-size:2.5rem;margin-bottom:15px;">👋</div>
            <h3 style="color:#2dd4d4;margin-bottom:10px;">Hello, {name_display}!</h3>
            <p style="color:#9fd8d5;">
                I'm your personal AI Mentor for <b>{topic_display}</b> at <b>{level_display}</b> level.<br>
                Ask me anything to get started!
            </p>
        </div>"""
    else:
        for msg in st.session_state.messages:
            msg_time = msg.get("time", "")
            if msg["role"] == "student":
                chat_html += f"""
                <div class="student-bubble">
                    <div class="bubble">{msg["content"]}</div>
                    <div class="msg-meta">You{" • " + msg_time if msg_time else ""}</div>
                </div>"""
            else:
                chat_html += f"""
                <div class="mentor-bubble">
                    <div class="row">
                        <div class="mentor-avatar">AI</div>
                        <div class="bubble">{msg["content"]}</div>
                    </div>
                    <div class="msg-meta">AIIMS Mentor{" • " + msg_time if msg_time else ""}</div>
                </div>"""

    if st.session_state.awaiting_response:
        chat_html += """
        <div class="mentor-bubble">
            <div class="row">
                <div class="mentor-avatar">AI</div>
                <div class="bubble typing-bubble-inline">
                    <span class="dot"></span><span class="dot"></span><span class="dot"></span>
                </div>
            </div>
        </div>"""

    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # -- HANDLE PENDING RESPONSE --
    if st.session_state.awaiting_response:
        
        session_ready = True
        if not st.session_state.session_id:
            sid, err = create_session(
                st.session_state.student_name.strip(),
                st.session_state.topic,
                st.session_state.level,
            )
            if err:
                st.session_state.last_error = err
                session_ready = False
                st.session_state.messages.pop()  # Remove student message if session failed
            else:
                st.session_state.session_id = sid
                st.session_state.locked = True

        if session_ready:
            answer, error = ask_question(
                st.session_state.session_id,
                st.session_state.pending_question,
                st.session_state.level,
                st.session_state.topic,
                files=st.session_state.pending_files,
            )
            if error:
                st.session_state.messages.pop()
                st.session_state.last_error = error
            else:
                st.session_state.messages.append(
                    {"role": "mentor", "content": answer, "time": datetime.now().strftime("%I:%M %p").lstrip("0")}
                )
                _save_current_chat_to_recents()

        st.session_state.awaiting_response = False
        st.session_state.pending_question = ""
        st.session_state.pending_files = None
        st.rerun()

    st.markdown('<div class="input-pill-marker"></div>', unsafe_allow_html=True)
    col_attach, col1, col2 = st.columns([0.6, 8.4, 0.6])

    with col_attach:
        with st.popover("+", use_container_width=True):
            st.markdown("**📄 Send a file**")
            uploaded_file = st.file_uploader(
                "Upload any file",
                type=["pdf", "txt", "csv", "md"],
                label_visibility="collapsed",
                key=f"file_upload_{st.session_state.input_counter}",
            )
            st.markdown("---")
            st.markdown("**🖼️ Add Images**")
            uploaded_screenshot = st.file_uploader(
                "Upload a screenshot",
                type=["png", "jpg", "jpeg"],
                label_visibility="collapsed",
                key=f"screenshot_upload_{st.session_state.input_counter}",
            )

    with col1:
        question = st.text_input(
            "question",
            placeholder=f"Ask me anything about {topic_display}...",
            label_visibility="collapsed",
            key=f"question_input_{st.session_state.input_counter}",
        )
    with col2:
        send = st.button("➤", key="send_btn")

if send and question.strip():
    if not st.session_state.student_name.strip():
        st.session_state.last_error = "Please enter your name in the sidebar first!"
        st.rerun()

    else:
        st.session_state.last_error = None
        user_question = question.strip()
        now_str = datetime.now().strftime("%I:%M %p").lstrip("0")

        # Collect uploaded files before clearing state
        attachments = []
        if uploaded_file:
            import base64
            encoded = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
            attachments.append({
                "filename": uploaded_file.name,
                "mime_type": uploaded_file.type,
                "data": encoded
            })
        if uploaded_screenshot:
            import base64
            encoded = base64.b64encode(uploaded_screenshot.getvalue()).decode("utf-8")
            attachments.append({
                "filename": uploaded_screenshot.name,
                "mime_type": uploaded_screenshot.type,
                "data": encoded
            })

        # Clear input field immediately and queue the question
        st.session_state.input_counter += 1
        
        # Optionally show an indicator in the UI that a file was sent
        file_indicator = ""
        if attachments:
            file_names = ", ".join([f["filename"] for f in attachments])
            file_indicator = f"\\n\\n*(Attached: {file_names})*"
            
        st.session_state.messages.append(
            {"role": "student", "content": user_question + file_indicator, "time": now_str}
        )
        _save_current_chat_to_recents()
        
        st.session_state.pending_question = user_question
        st.session_state.pending_files = attachments if attachments else None
        st.session_state.awaiting_response = True
        st.rerun()