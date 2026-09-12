"""
TechVerse ERP — Smart Campus Intelligence System
Main entry point.

Run with:
    cd project/
    streamlit run app.py
"""

import streamlit as st
from utils import load_json

# ── Page config (must be the very first Streamlit call) ───────────────────────
st.set_page_config(
    page_title="TechVerse ERP · Smart Campus",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# LOAD CREDENTIALS FROM JSON DATA STORE
# ─────────────────────────────────────────────────────────────────────────────
USERS = load_json("users.json")

# ─────────────────────────────────────────────────────────────────────────────
# NAVIGATION MAPS
# ─────────────────────────────────────────────────────────────────────────────
MANAGEMENT_PAGES = [
    "🏠  Dashboard",
    "👥  Account Management",
    "📋  Student Registration",
    "🤖  AI Assistant",
]

STAFF_PAGES = [
    "📋  Overview",
    "🗓  Attendance",
    "📊  Marks",
    "👤  Student Details",
    "🏛  Sections",
    "📚  Courses",
    "🤖  AI Assistant",
]

STUDENT_PAGES = [
    "🏠 Dashboard",
    "📅 Attendance",
    "📝 Exam Marks",
    "👤 Profile",
    "🎫 Event Registration",
    "💳 Fee Payments",
    "🤖 AI Assistant",
]

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE BOOTSTRAP
# ─────────────────────────────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "logged_in": False,
        "role":      None,
        "username":  None,
        "user_info": {},
        "app_page":  None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL LIGHT THEME & 20/80 WIDTH PROPORTIONS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background-color: #f8fafc !important;
    color: #0f172a !important;
}

/* ── Sidebar Width: Strictly 20% - 25% (260px - 280px) ──────────────────── */
section[data-testid="stSidebar"],
[data-testid="stSidebar"] {
    width: 270px !important;
    min-width: 260px !important;
    max-width: 290px !important;
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
    box-shadow: 2px 0 12px rgba(15, 23, 42, 0.02) !important;
}

[data-testid="stSidebarContent"] {
    padding: 1.2rem 0.9rem !important;
}

/* Hide default radio circle bullets & labels in sidebar */
[data-testid="stSidebar"] div[data-testid="stRadio"] > label {
    display: none !important;
}
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] {
    gap: 5px !important;
}
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] > label > div:first-child,
[data-testid="stSidebar"] div[data-testid="stRadio"] input[type="radio"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
}
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] > label {
    margin: 0 !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    background: transparent !important;
    transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1) !important;
    display: flex !important;
    align-items: center !important;
    border: 1px solid transparent !important;
    width: 100% !important;
}
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] > label:hover {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
}
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] > label[data-checked="true"],
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) {
    background-color: #eff6ff !important;
    border-left: 4px solid #2563eb !important;
    border-color: #bfdbfe #bfdbfe #bfdbfe #2563eb !important;
}
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] > label p,
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] > label span {
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    color: #475569 !important;
    margin: 0 !important;
}
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] > label[data-checked="true"] p,
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) p {
    color: #1d4ed8 !important;
    font-weight: 700 !important;
}

/* Sidebar Sign Out Button */
[data-testid="stSidebar"] div.stButton > button {
    background-color: #ffffff !important;
    color: #e11d48 !important;
    border: 1px solid #fecdd3 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #fff1f2 !important;
    border-color: #fda4af !important;
    color: #be123c !important;
    box-shadow: 0 4px 12px rgba(225, 29, 72, 0.1) !important;
}

/* ── Main Content Area: Takes 75% - 80% with generous breathing room ───────── */
.main {
    width: 100% !important;
}
.main .block-container {
    padding: 2.2rem 3.5rem 4rem !important;
    max-width: 1500px !important;
    width: 100% !important;
}

/* ── General Content & Text Visibility ───────────── */
p, span, div, label, h1, h2, h3, h4, h5, h6, li {
    color: #0f172a;
}

/* ── Form Inputs & Text Contrast ─────────────────── */
div[data-baseweb="input"],
div[data-baseweb="base-input"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
}
div[data-baseweb="input"]:focus-within,
div[data-baseweb="base-input"]:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
}
div[data-baseweb="input"] input,
div[data-baseweb="base-input"] input,
div[data-testid="stTextInput"] input {
    background-color: #ffffff !important;
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    font-size: 0.95rem !important;
}
div[data-baseweb="textarea"],
div[data-testid="stTextArea"] textarea {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stTextInput"] label p,
div[data-testid="stTextArea"] label,
div[data-testid="stTextArea"] label p,
div[data-testid="stSelectbox"] label,
div[data-testid="stSelectbox"] label p {
    color: #0f172a !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}

/* ── Selectbox & Dropdowns ───────────────────────── */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #0f172a !important;
}
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"],
li[role="option"] {
    background-color: #ffffff !important;
    color: #0f172a !important;
}
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background-color: #eff6ff !important;
    color: #1d4ed8 !important;
}

/* ── Main Radio Button Styling (Role Selector) ───── */
.main div[data-testid="stRadio"] [role="radiogroup"] {
    gap: 12px !important;
}
.main div[data-testid="stRadio"] [role="radiogroup"] > label {
    background-color: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 10px 18px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
}
.main div[data-testid="stRadio"] [role="radiogroup"] > label:hover {
    border-color: #93c5fd !important;
    background-color: #f8fafc !important;
}
.main div[data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) {
    background-color: #eff6ff !important;
    border-color: #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
}
.main div[data-testid="stRadio"] label p,
.main div[data-testid="stRadio"] label span,
.main div[data-testid="stRadio"] label div {
    color: #0f172a !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}

/* ── Tabs Styling ────────────────────────────────── */
button[data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 0.7rem 1.4rem !important;
    border-radius: 8px 8px 0 0 !important;
}
button[data-baseweb="tab"]:hover {
    color: #1e293b !important;
    background-color: #f1f5f9 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #2563eb !important;
    border-bottom: 3px solid #2563eb !important;
    font-weight: 700 !important;
}
button[data-baseweb="tab"] div,
button[data-baseweb="tab"] p,
button[data-baseweb="tab"] span {
    color: inherit !important;
    font-weight: inherit !important;
}
div[data-baseweb="tab-highlight"] {
    background-color: #2563eb !important;
}

/* ── Buttons (Secondary / Outline / Suggestion) ──── */
div.stButton > button {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
}
div.stButton > button:hover {
    background-color: #f8fafc !important;
    border-color: #94a3b8 !important;
    color: #0f172a !important;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08) !important;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25) !important;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.38) !important;
}

/* ── Chatbot Components & Floating Input Container ─ */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
.stChatFloatingInputContainer,
div[data-testid="stChatInputContainer"] {
    background-color: #f8fafc !important;
    background: #f8fafc !important;
    border-top: 1px solid #e2e8f0 !important;
    padding-top: 0.6rem !important;
    padding-bottom: 1.2rem !important;
}
[data-testid="stBottom"] > div > div {
    background-color: transparent !important;
}
div[data-testid="stChatInput"] {
    background-color: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06) !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.18) !important;
}
div[data-testid="stChatInput"] textarea {
    background-color: transparent !important;
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    font-size: 0.95rem !important;
}
div[data-testid="stChatInput"] button {
    color: #2563eb !important;
}
div[data-testid="stChatMessage"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px !important;
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03) !important;
    color: #0f172a !important;
    margin-bottom: 0.85rem !important;
    padding: 1rem 1.25rem !important;
}
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] div {
    color: #0f172a !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background-color: #eff6ff !important;
    border-color: #bfdbfe !important;
}

/* ── Dialogs & Modals ────────────────────────────── */
div[data-testid="stDialog"],
div[role="dialog"] {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border-radius: 16px !important;
    box-shadow: 0 20px 40px rgba(15, 23, 42, 0.15) !important;
}
div[role="dialog"] * {
    color: #0f172a;
}

/* ── Typography ──────────────────────────────────── */
.page-title {
    font-family: 'Sora', sans-serif !important;
    font-size: 2.1rem !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    letter-spacing: -0.025em !important;
    margin-bottom: 0.25rem !important;
}
.page-subtitle {
    font-size: 0.95rem !important;
    color: #64748b !important;
    margin-bottom: 1.8rem !important;
    line-height: 1.5 !important;
}

/* ── Symmetrical 5-Column Metric Grid ────────────── */
.stat-grid-5 {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 1.2rem;
    margin-bottom: 2rem;
}
@media (max-width: 1200px) {
    .stat-grid-5 {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
}
@media (max-width: 768px) {
    .stat-grid-5 {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}
.stat-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.3rem 1.4rem;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
}
.stat-card .label {
    font-size: 0.74rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.35rem;
}
.stat-card .value {
    font-family: 'Sora', sans-serif;
    font-size: 2.15rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.1;
}
.stat-card .delta {
    font-size: 0.78rem;
    margin-top: 0.45rem;
    color: #16a34a;
    font-weight: 600;
}
.stat-card .accent-bar {
    height: 4px;
    border-radius: 3px;
    margin-bottom: 0.75rem;
}

/* ── Badges ──────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 3px 11px;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.badge-green  { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
.badge-red    { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }
.badge-blue   { background: #dbeafe; color: #1d4ed8; border: 1px solid #bfdbfe; }
.badge-amber  { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
.badge-purple { background: #ede9fe; color: #6d28d9; border: 1px solid #ddd6fe; }
.badge-cyan   { background: #cffafe; color: #0e7490; border: 1px solid #a5f3fc; }
.badge-slate  { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }

/* ── Section Header & Info Cards ─────────────────── */
.section-header {
    font-family: 'Sora', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 0.8rem;
    letter-spacing: -0.01em;
}
.info-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
}
.card-label {
    font-size: 0.74rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
}
.card-value {
    font-size: 0.98rem;
    font-weight: 600;
    color: #0f172a;
}

/* ── Hide Streamlit chrome ───────────────────────── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { background: transparent; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# AUTHENTICATION
# ─────────────────────────────────────────────────────────────────────────────
def _authenticate(role: str, username: str, password: str):
    user = USERS.get(role, {}).get(username)
    if user and user["password"] == password:
        return user
    return None


# ─────────────────────────────────────────────────────────────────────────────
# LOGIN PAGE
# ─────────────────────────────────────────────────────────────────────────────
def _render_login():
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none !important; }
    .main .block-container {
        padding: 3.5rem 1.5rem !important;
        max-width: 850px !important;
        margin: 0 auto !important;
    }
    .brand-title {
        font-family: 'Sora', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    .brand-subtitle {
        font-size: 0.92rem;
        color: #64748b;
        font-weight: 500;
        margin-top: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <div style='display: inline-flex; align-items: center; justify-content: center; width: 68px; height: 68px;
                    background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 20px; font-size: 2.4rem; margin-bottom: 0.8rem;
                    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.15);'>
            🏛️
        </div>
        <div class="brand-title">TechVerse ERP</div>
        <div class="brand-subtitle">Smart Campus Intelligence &amp; Academic Management Platform &nbsp;·&nbsp; <strong>NAAC A+ Accredited</strong></div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_center, col_r = st.columns([1, 2.6, 1])

    with col_center:
        with st.container(border=True):
            st.markdown("""
            <div style='text-align: center; margin-bottom: 1.2rem;'>
                <div style='font-family: "Sora", sans-serif; font-size: 1.2rem; font-weight: 700; color: #0f172a;'>
                    Sign In to Portal
                </div>
                <div style='font-size: 0.84rem; color: #64748b; margin-top: 2px;'>
                    Select your portal role to continue
                </div>
            </div>
            """, unsafe_allow_html=True)

            role = st.radio(
                "Select Role",
                ["management", "staff", "student"],
                format_func=lambda x: {
                    "management": "🛡️  Management",
                    "staff":      "🎓  Faculty & Staff",
                    "student":    "🧑‍🎓  Student Portal",
                }[x],
                horizontal=True,
                key="login_role_sel",
                label_visibility="collapsed",
            )

            demo_defaults = {
                "management": ("admin.jose", "Faculty#103"),
                "staff":      ("prof.rao", "Faculty#101"),
                "student":    ("stu.arjun21", "Student#201"),
            }
            def_user, def_pass = demo_defaults[role]

            username = st.text_input(
                "Username",
                value=def_user,
                placeholder="Enter your username",
                key="login_uname",
            )
            password = st.text_input(
                "Password",
                value=def_pass,
                placeholder="Enter your password",
                type="password",
                key="login_pwd",
            )

            st.markdown("<div style='height: 0.4rem'></div>", unsafe_allow_html=True)

            if st.button("Sign In  →", use_container_width=True, type="primary", key="login_btn"):
                info = _authenticate(role, username.strip(), password)
                if info:
                    st.session_state.logged_in = True
                    st.session_state.role      = role
                    st.session_state.username  = username.strip()
                    st.session_state.user_info = info
                    st.session_state.app_page  = {
                        "management": MANAGEMENT_PAGES[0],
                        "staff":      STAFF_PAGES[0],
                        "student":    STUDENT_PAGES[0],
                    }[role]
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please verify your username and password.")

            st.markdown(f"""
            <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 10px; padding: 0.8rem 1rem; margin-top: 1.2rem; text-align: center;">
                <div style='font-size: 0.72rem; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 3px;'>
                    Demo Credentials (Auto-filled)
                </div>
                <div style='font-size: 0.84rem; color: #1e293b; font-family: monospace;'>
                    Username: <strong style='color:#2563eb;'>{def_user}</strong> &nbsp;|&nbsp; Password: <strong style='color:#2563eb;'>{def_pass}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; font-size: 0.76rem; color: #94a3b8; margin-top: 2.2rem;'>
        © 2026 TechVerse Engineering College &nbsp;·&nbsp; AI-Powered Smart Campus Platform
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR (Post-Login)
# ─────────────────────────────────────────────────────────────────────────────
def _render_sidebar():
    role      = st.session_state.role
    user_info = st.session_state.user_info
    pages     = {
        "management": MANAGEMENT_PAGES,
        "staff":      STAFF_PAGES,
        "student":    STUDENT_PAGES,
    }[role]
    role_color_badge = {
        "management": "badge-purple",
        "staff":      "badge-blue",
        "student":    "badge-green",
    }[role]
    role_label = {
        "management": "Management",
        "staff":      "Faculty / Staff",
        "student":    "Student",
    }[role]

    with st.sidebar:
        # Brand block
        st.markdown("""
        <div style='padding: 0.6rem 0.1rem 1rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1.1rem;'>
            <div style='display: flex; align-items: center; gap: 10px;'>
                <div style='font-size: 1.85rem;'>🏛️</div>
                <div>
                    <div style='font-family: "Sora", sans-serif; font-size: 1.05rem; font-weight: 800; color: #0f172a; letter-spacing: -0.02em;'>
                        TechVerse ERP
                    </div>
                    <div style='font-size: 0.68rem; color: #64748b; font-weight: 600;'>
                        Smart Campus Intelligence · v3.1
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='font-size: 0.68rem; color: #94a3b8; text-transform: uppercase;
                    letter-spacing: 0.08em; font-weight: 700; padding-left: 4px;
                    margin-bottom: 6px;'>Navigation Menu</div>
        """, unsafe_allow_html=True)

        current_idx = (
            pages.index(st.session_state.app_page)
            if st.session_state.app_page in pages
            else 0
        )
        selected = st.radio(
            "nav_menu",
            pages,
            index=current_idx,
            label_visibility="collapsed",
            key="main_nav_radio",
        )

        if selected != st.session_state.app_page:
            st.session_state.app_page = selected
            st.rerun()

        # User profile card
        display_name = user_info.get("display_name", st.session_state.username)
        initials = user_info.get("initials", "U")
        title = user_info.get("title", "")

        st.markdown(f"""
        <hr style='border: none; border-top: 1px solid #e2e8f0; margin: 1.4rem 0 0.9rem;'>
        <div style='background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 0.85rem; margin-bottom: 0.85rem;'>
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 6px;'>
                <div style='width: 36px; height: 36px; border-radius: 50%; background: #eff6ff; border: 1px solid #bfdbfe;
                            color: #2563eb; font-weight: 800; font-family: "Sora", sans-serif;
                            display: flex; align-items: center; justify-content: center; font-size: 0.88rem; flex-shrink: 0;'>
                    {initials}
                </div>
                <div style='overflow: hidden;'>
                    <div style='font-weight: 700; font-size: 0.86rem; color: #0f172a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>
                        {display_name}
                    </div>
                    <div style='font-size: 0.72rem; color: #64748b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>
                        {title}
                    </div>
                </div>
            </div>
            <div style='text-align: right;'>
                <span class='badge {role_color_badge}'>{role_label}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪  Sign Out", use_container_width=True, key="signout_btn"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

        st.markdown("""
        <div style='font-size: 0.65rem; color: #94a3b8; text-align: center; padding-top: 0.8rem;'>
            TechVerse ERP &nbsp;·&nbsp; NAAC A+ Accredited
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MANAGEMENT DASHBOARD (Overview Page)
# ─────────────────────────────────────────────────────────────────────────────
def _render_mgmt_dashboard():
    st.markdown('<div class="page-title">Admin Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">'
        'Platform overview & administrative telemetry — TechVerse Smart Campus ERP · Even Semester 2025-26'
        '</div>',
        unsafe_allow_html=True,
    )

    # 5 Symmetrical Metrics Grid
    st.markdown("""
    <div class="stat-grid-5">
        <div class="stat-card">
            <div class="accent-bar" style="background:#8b5cf6;"></div>
            <div class="label">Staff Accounts</div>
            <div class="value">4</div>
            <div class="delta">Active portal users</div>
        </div>
        <div class="stat-card">
            <div class="accent-bar" style="background:#0ea5e9;"></div>
            <div class="label">Student Accounts</div>
            <div class="value">5</div>
            <div class="delta">Portal registered</div>
        </div>
        <div class="stat-card">
            <div class="accent-bar" style="background:#22c55e;"></div>
            <div class="label">Total Students</div>
            <div class="value">323</div>
            <div class="delta">Across 5 departments</div>
        </div>
        <div class="stat-card">
            <div class="accent-bar" style="background:#f59e0b;"></div>
            <div class="label">Active Sections</div>
            <div class="value">6</div>
            <div class="delta">Active this semester</div>
        </div>
        <div class="stat-card">
            <div class="accent-bar" style="background:#ec4899;"></div>
            <div class="label">Avg Attendance</div>
            <div class="value">83%</div>
            <div class="delta">↑ 1.5% vs last month</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2 Action Cards
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.8rem;
                    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04); margin-bottom: 1.2rem; min-height: 180px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.6rem;">
                <div style="font-size: 1.8rem;">👥</div>
                <div style="font-family: 'Sora', sans-serif; font-size: 1.25rem; font-weight: 700; color: #0f172a;">
                    Account Management
                </div>
            </div>
            <div style="font-size: 0.88rem; color: #64748b; line-height: 1.55;">
                Create, edit, reset passwords, or manage credentials and access privileges for all staff and student portal users.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(
            "Open Account Management →", key="d_mgmt",
            use_container_width=True, type="primary",
        ):
            st.session_state.app_page = MANAGEMENT_PAGES[1]
            st.rerun()

    with c2:
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.8rem;
                    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04); margin-bottom: 1.2rem; min-height: 180px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.6rem;">
                <div style="font-size: 1.8rem;">📋</div>
                <div style="font-family: 'Sora', sans-serif; font-size: 1.25rem; font-weight: 700; color: #0f172a;">
                    Student Registration
                </div>
            </div>
            <div style="font-size: 0.88rem; color: #64748b; line-height: 1.55;">
                Register new students with department assignment, contact records, emergency contacts, and photo verification.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(
            "Open Registration Form →", key="d_form",
            use_container_width=True, type="primary",
        ):
            st.session_state.app_page = MANAGEMENT_PAGES[2]
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────────────────────────────────────
def _render_main():
    import chatbot    as _chatbot
    import staff      as _staff
    import stud       as _stud
    import management as _mgmt
    import form       as _form

    role = st.session_state.role
    page = st.session_state.app_page

    if role == "management":
        if   page == MANAGEMENT_PAGES[0]: _render_mgmt_dashboard()
        elif page == MANAGEMENT_PAGES[1]: _mgmt.render()
        elif page == MANAGEMENT_PAGES[2]: _form.render()
        elif page == MANAGEMENT_PAGES[3]: _chatbot.render()

    elif role == "staff":
        if page == STAFF_PAGES[-1]:       # "🤖  AI Assistant"
            _chatbot.render()
        else:
            _staff.render(page)

    elif role == "student":
        if page == STUDENT_PAGES[-1]:     # "🤖 AI Assistant"
            _chatbot.render()
        else:
            _stud.render(page)


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    _render_login()
else:
    _render_sidebar()
    _render_main()
