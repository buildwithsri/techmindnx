import streamlit as st
import requests
import os

# ---------------------------------------------------------
# MODULE-LEVEL CONFIG
# ---------------------------------------------------------

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-2.5-flash"

AVAILABLE_MODELS = {
    "Gemini 2.5 Flash": "google/gemini-2.5-flash",
    "Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet",
    "GPT-4o Mini":       "openai/gpt-4o-mini",
    "DeepSeek R1":       "deepseek/deepseek-r1",
}

try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    try:
        API_KEY = os.environ["OPENROUTER_API_KEY"]
    except KeyError:
        API_KEY = None


# ---------------------------------------------------------
# OPENROUTER FUNCTION
# ---------------------------------------------------------

def ask_openrouter(messages, model):
    """Send conversation history to OpenRouter and return the reply."""
    if not API_KEY or "your-actual-key-here" in API_KEY:
        return (
            "⚠️ **OpenRouter API Key Not Configured**\n\n"
            "To enable live AI responses, please copy `.streamlit/secrets.toml.example` to "
            "`.streamlit/secrets.toml` and set your `OPENROUTER_API_KEY`."
        )

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type":  "application/json",
        "HTTP-Referer":  "http://localhost:8501",
        "X-Title":       "TechVerse Campus AI Assistant",
    }

    payload = {
        "model":       model,
        "messages":    messages,
        "temperature": 0.7,
        "max_tokens":  2000,
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60,
        )

        if response.status_code != 200:
            try:
                err = response.json().get("error", {}).get("message", response.text)
            except Exception:
                err = response.text
            return f"❌ OpenRouter error ({response.status_code}): {err}"

        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "⏱️ The AI request timed out. Please try again."

    except requests.exceptions.ConnectionError:
        return "🌐 Network error: Could not reach OpenRouter. Please check your connection."

    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"


# ---------------------------------------------------------
# RENDER — called from app.py
# ---------------------------------------------------------

def render():
    """Render the AI chatbot page inside the connected TechVerse app."""

    st.markdown("""
    <style>
    .chat-header-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    .suggestion-chip {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 99px;
        padding: 6px 14px;
        font-size: 0.8rem;
        color: #334155;
        font-weight: 500;
        display: inline-block;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Session state ─────────────────────────────────────────────────────────
    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = []
    if "chatbot_model" not in st.session_state:
        st.session_state.chatbot_model = DEFAULT_MODEL

    # ── Header bar ────────────────────────────────────────────────────────────
    st.markdown('<div class="page-title">Campus AI Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Interactive AI academic companion for course queries, code explanations, syllabus assistance, and campus guidance</div>', unsafe_allow_html=True)

    # Toolbar
    with st.container(border=True):
        t_left, _, t_right = st.columns([3, 1, 2])
        with t_left:
            st.markdown(f"🤖 **Model Engine:** `{st.session_state.chatbot_model}`")
        with t_right:
            sel_name = st.selectbox(
                "Change Model",
                list(AVAILABLE_MODELS.keys()),
                index=list(AVAILABLE_MODELS.values()).index(st.session_state.chatbot_model)
                if st.session_state.chatbot_model in AVAILABLE_MODELS.values() else 0,
                key="chatbot_model_sel",
                label_visibility="collapsed",
            )
            if AVAILABLE_MODELS[sel_name] != st.session_state.chatbot_model:
                st.session_state.chatbot_model = AVAILABLE_MODELS[sel_name]
                st.rerun()

    # ── Welcome & Suggested Queries ───────────────────────────────────────────
    if not st.session_state.chatbot_messages:
        with st.container(border=True):
            st.markdown("""
            <div style='text-align: center; padding: 1.5rem 1rem;'>
                <div style='font-size: 2.8rem; margin-bottom: 0.5rem;'>✨</div>
                <div style='font-family: "Sora", sans-serif; font-size: 1.3rem; font-weight: 700; color: #0f172a;'>
                    How can I assist you today?
                </div>
                <div style='font-size: 0.88rem; color: #64748b; margin-top: 4px; max-width: 600px; margin-left: auto; margin-right: auto;'>
                    Ask questions about your courses, debug algorithms, get study plans, or draft emails to advisors.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='font-size:0.75rem;font-weight:700;color:#94a3b8;text-transform:uppercase;margin-bottom:8px;'>Try asking:</div>", unsafe_allow_html=True)
            suggestions = [
                "Explain Dijkstra's shortest path algorithm with time complexity.",
                "How does virtual memory paging work in Operating Systems?",
                "Draft a formal request email for attendance condonation.",
                "What is the difference between B-Tree and B+ Tree in DBMS?",
            ]
            s_cols = st.columns(2)
            for i, sug in enumerate(suggestions):
                col = s_cols[i % 2]
                if col.button(f"💬 {sug}", key=f"sug_{i}", use_container_width=True):
                    st.session_state.chatbot_messages.append({"role": "user", "content": sug})
                    st.rerun()

    # ── Chat history ──────────────────────────────────────────────────────────
    for msg in st.session_state.chatbot_messages:
        role, content = msg["role"], msg["content"]
        with st.chat_message(role, avatar="🧑‍🎓" if role == "user" else "🤖"):
            st.markdown(content)

    # ── Chat Input ────────────────────────────────----------------------------
    prompt = st.chat_input("Ask anything about your courses, timetable or campus...")

    if prompt:
        st.session_state.chatbot_messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(prompt)

        api_messages = [
            {
                "role": "system",
                "content": (
                    "You are the official TechVerse Smart Campus AI Assistant. "
                    "Provide clear, academically rigorous, structured, and helpful responses. "
                    "Format code and mathematical formulas nicely with Markdown."
                ),
            }
        ] + st.session_state.chatbot_messages

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Analyzing request..."):
                answer = ask_openrouter(api_messages, st.session_state.chatbot_model)
            st.markdown(answer)

        st.session_state.chatbot_messages.append({"role": "assistant", "content": answer})
        st.rerun()

    # Clear chat button
    if st.session_state.chatbot_messages:
        st.markdown("<div style='height: 0.8rem'></div>", unsafe_allow_html=True)
        if st.button("🗑️  Clear Conversation History", key="chatbot_clear", type="secondary"):
            st.session_state.chatbot_messages = []
            st.rerun()
