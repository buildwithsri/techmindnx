"""
TechVerse ERP — Smart Campus Intelligence System
Main entry point.

Run with:
    cd project/
    streamlit run app.py
"""

import streamlit as st

# ── Page config (must be the very first Streamlit call) ───────────────────────
st.set_page_config(
    page_title="TechVerse ERP · Smart Campus",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CREDENTIAL STORE
# ─────────────────────────────────────────────────────────────────────────────
USERS = {
    "management": {
        "admin.jose": {
            "password":     "Faculty#103",
            "display_name": "Admin Jose",
            "title":        "Administrator",
            "initials":     "AJ",
        },
        "admin": {
            "password":     "admin",
            "display_name": "Administrator",
            "title":        "System Admin",
            "initials":     "SA",
        },
    },
    "staff": {
        "prof.rao": {
            "password":     "Faculty#101",
            "display_name": "Prof. Rao",
            "title":        "Assoc. Professor · CSE",
            "initials":     "PR",
        },
        "dr.menon": {
            "password":     "Faculty#102",
            "display_name": "Dr. Menon",
            "title":        "Professor · ECE",
            "initials":     "DM",
        },
        "lib.anu": {
            "password":     "Faculty#104",
            "display_name": "Lib. Anu",
            "title":        "Librarian",
            "initials":     "LA",
        },
    },
    "student": {
        "stu.arjun21": {
            "password":     "Student#201",
            "display_name": "Aditya Sharma",
            "title":        "CSE · Sem 6 · 2022-26",
            "reg":          "TVE22CS001",
            "dept":         "Computer Science & Engineering",
            "sem":          "6",
            "initials":     "AS",
        },
        "stu.divya22": {
            "password":     "Student#202",
            "display_name": "Bhavana Nair",
            "title":        "CSE · Sem 6 · 2022-26",
            "reg":          "TVE22CS002",
            "dept":         "Computer Science & Engineering",
            "sem":          "6",
            "initials":     "BN",
        },
        "stu.farhan23": {
            "password":     "Student#203",
            "display_name": "Chetan Pillai",
            "title":        "CSE · Sem 6 · 2022-26",
            "reg":          "TVE22CS003",
            "dept":         "Computer Science & Engineering",
            "sem":          "6",
            "initials":     "CP",
        },
        "stu.leah24": {
            "password":     "Student#204",
            "display_name": "Deepthi Menon",
            "title":        "CSE · Sem 6 · 2022-26",
            "reg":          "TVE22CS004",
            "dept":         "Computer Science & Engineering",
            "sem":          "6",
            "initials":     "DM",
        },
        "stu.nihal25": {
            "password":     "Student#205",
            "display_name": "Edwin Jose",
            "title":        "CSE · Sem 6 · 2022-26",
            "reg":          "TVE22CS005",
            "dept":         "Computer Science & Engineering",
            "sem":          "6",
            "initials":     "EJ",
        },
    },
}

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
# GLOBAL LIGHT THEME CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background-color: #f8fafc !important;
    color: #0f172a !important;
}

/* ── Light Sidebar ────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] * {
    color: #334155 !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: #475569 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 8px 12px !important;
    border-radius: 9px !important;
    transition: all 0.15s ease-in-out !important;
    cursor: pointer !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    margin-bottom: 2px !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: #f1f5f9 !important;
    color: #0f172a !important;
}
[data-testid="stSidebar"] .stRadio [data-checked="true"] + label,
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"]:has(input:checked) {
    background: #eff6ff !important;
    color: #1d4ed8 !important;
    font-weight: 700 !important;
    border-left: 3px solid #2563eb !important;
}

/* ── Form Inputs (Ensure bright light theme inputs) ────────────────────────── */
div[data-baseweb="input"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
}
div[data-baseweb="input"] input {
    background-color: transparent !important;
    color: #0f172a !important;
    font-size: 0.95rem !important;
}
div[data-baseweb="input"] input::placeholder {
    color: #94a3b8 !important;
}
div[data-baseweb="textarea"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
}
div[data-baseweb="textarea"] textarea {
    background-color: transparent !important;
    color: #0f172a !important;
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

/* ── Radio Buttons text contrast ─────────────────── */
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] span {
    color: #0f172a !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}

/* ── Main Container ──────────────────────────────── */
.main .block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1350px !important;
    background: transparent !important;
}

/* ── Typography ──────────────────────────────────── */
.page-title {
    font-family: 'Sora', sans-serif !important;
    font-size: 1.85rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 0.25rem !important;
}
.page-subtitle {
    font-size: 0.92rem !important;
    color: #64748b !important;
    margin-bottom: 1.8rem !important;
    line-height: 1.5 !important;
}

/* ── Stat Cards ──────────────────────────────────── */
.stat-row {
    display: flex;
    gap: 1.1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}
.stat-card {
    flex: 1;
    min-width: 160px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.3rem 1.4rem;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(15, 23, 42, 0.07);
}
.stat-card .label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.4rem;
}
.stat-card .value {
    font-family: 'Sora', sans-serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.1;
}
.stat-card .delta {
    font-size: 0.78rem;
    margin-top: 0.45rem;
    color: #16a34a;
    font-weight: 500;
}
.stat-card .accent-bar {
    height: 4px;
    border-radius: 3px;
    margin-bottom: 0.8rem;
}

/* ── Section Header ──────────────────────────────── */
.section-header {
    font-family: 'Sora', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 0.9rem;
    border-left: 4px solid #2563eb;
    padding-left: 0.75rem;
    display: flex;
    align-items: center;
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

/* ── Info Cards ──────────────────────────────────── */
.info-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
}
.info-card .card-label {
    font-size: 0.75rem;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.info-card .card-value {
    font-size: 1.05rem;
    color: #0f172a;
    font-weight: 600;
    margin-top: 3px;
}

/* ── Clean Forms & Buttons ───────────────────────── */
div.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.25rem !important;
    transition: all 0.15s ease !important;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
}
div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35) !important;
    transform: translateY(-1px) !important;
}

/* ── Tables & Dataframe ──────────────────────────── */
.dataframe {
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
}
.dataframe th {
    background: #f8fafc !important;
    color: #475569 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    border-bottom: 2px solid #e2e8f0 !important;
    padding: 10px 14px !important;
}
.dataframe td {
    font-size: 0.86rem !important;
    color: #1e293b !important;
    padding: 10px 14px !important;
    border-bottom: 1px solid #f1f5f9 !important;
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
        padding: 3rem 1.5rem !important;
        max-width: 900px !important;
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

    # Centered Header
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

    col_l, col_center, col_r = st.columns([1, 2.4, 1])

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

            st.markdown("<div style='height: 0.3rem'></div>", unsafe_allow_html=True)

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
        "management": "🛡️ Management",
        "staff":      "🎓 Faculty / Staff",
        "student":    "🧑‍🎓 Student",
    }[role]

    with st.sidebar:
        # Brand block
        st.markdown("""
        <div style='padding: 0.8rem 0.2rem 1.1rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1rem;'>
            <div style='display: flex; align-items: center; gap: 10px;'>
                <div style='font-size: 1.8rem;'>🏛️</div>
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
                    letter-spacing: 0.08em; font-weight: 700; padding-left: 6px;
                    margin-bottom: 6px;'>Navigation</div>
        """, unsafe_allow_html=True)

        current_idx = (
            pages.index(st.session_state.app_page)
            if st.session_state.app_page in pages
            else 0
        )
        selected = st.radio(
            "nav",
            pages,
            index=current_idx,
            label_visibility="collapsed",
            key="main_nav_radio",
        )

        if selected != st.session_state.app_page:
            st.session_state.app_page = selected
            st.rerun()

        # User profile block
        display_name = user_info.get("display_name", st.session_state.username)
        initials = user_info.get("initials", "U")
        title = user_info.get("title", "")

        st.markdown(f"""
        <hr style='border: none; border-top: 1px solid #e2e8f0; margin: 1.2rem 0 1rem;'>
        <div style='background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 0.85rem; margin-bottom: 0.8rem;'>
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 8px;'>
                <div style='width: 36px; height: 36px; border-radius: 50%; background: #eff6ff; border: 1px solid #bfdbfe;
                            color: #2563eb; font-weight: 700; font-family: "Sora", sans-serif;
                            display: flex; align-items: center; justify-content: center; font-size: 0.88rem;'>
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
        <div style='font-size: 0.65rem; color: #94a3b8; text-align: center; padding-top: 1rem;'>
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

    st.markdown("""
    <div class="stat-row">
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

    c1, c2 = st.columns(2, gap="large")
    with c1:
        with st.container(border=True):
            st.markdown("### 👥  Account Management")
            st.write(
                "Create, edit, reset passwords, or manage credentials "
                "for all staff and student portal users."
            )
            if st.button(
                "Open Account Management →", key="d_mgmt",
                use_container_width=True, type="primary",
            ):
                st.session_state.app_page = MANAGEMENT_PAGES[1]
                st.rerun()
    with c2:
        with st.container(border=True):
            st.markdown("### 📋  Student Registration")
            st.write(
                "Register new students with department assignment, "
                "contact records, emergency contacts, and photo verification."
            )
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
