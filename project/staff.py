import streamlit as st
import pandas as pd
import random
from datetime import date, timedelta

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Faculty Portal · TechVerse Engineering",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stSidebar"] {
    background: #0c1120 !important;
    border-right: 1px solid #1a2236;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] .stRadio label {
    color: #94a3b8 !important;
    font-size: 0.875rem;
    padding: 6px 0;
}
[data-testid="stSidebar"] .stRadio > div > label:hover { color: #f8fafc !important; }

.main .block-container {
    padding: 2rem 2.5rem 3rem;
    max-width: 1400px;
    background: #f1f5f9;
}

.page-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 0.2rem;
}
.page-subtitle {
    font-size: 0.875rem;
    color: #64748b;
    margin-bottom: 1.8rem;
}

.stat-row { display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }
.stat-card {
    flex: 1; min-width: 160px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
}
.stat-card .label {
    font-size: 0.75rem; font-weight: 500; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem;
}
.stat-card .value {
    font-family: 'Sora', sans-serif; font-size: 2rem;
    font-weight: 700; color: #0f172a; line-height: 1;
}
.stat-card .delta { font-size: 0.75rem; margin-top: 0.4rem; color: #22c55e; }
.stat-card .accent-bar { height: 3px; border-radius: 2px; margin-bottom: 0.8rem; }

.section-header {
    font-family: 'Sora', sans-serif; font-size: 1.1rem;
    font-weight: 700; color: #0f172a; margin-bottom: 0.8rem;
    border-left: 3px solid #0ea5e9; padding-left: 0.7rem;
}

.badge {
    display: inline-block; padding: 2px 10px;
    border-radius: 99px; font-size: 0.72rem; font-weight: 600;
}
.badge-green  { background: #dcfce7; color: #16a34a; }
.badge-red    { background: #fee2e2; color: #dc2626; }
.badge-blue   { background: #dbeafe; color: #2563eb; }
.badge-amber  { background: #fef3c7; color: #d97706; }
.badge-purple { background: #ede9fe; color: #7c3aed; }
.badge-cyan   { background: #cffafe; color: #0891b2; }
.badge-slate  { background: #f1f5f9; color: #475569; }

.info-card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 1rem;
}
.info-card .card-label {
    font-size: 0.72rem; color: #94a3b8; font-weight: 500;
    text-transform: uppercase; letter-spacing: 0.04em;
}
.info-card .card-value { font-size: 1rem; color: #0f172a; font-weight: 500; margin-top: 2px; }

.faculty-hero {
    background: linear-gradient(135deg, #0c1a2e 0%, #0f3460 55%, #0ea5e9 100%);
    border-radius: 14px; padding: 1.8rem 2rem; margin-bottom: 1.8rem;
    display: flex; align-items: center; gap: 1.4rem; color: white;
}
.faculty-avatar {
    width: 64px; height: 64px; border-radius: 50%;
    background: rgba(255,255,255,0.15);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem; font-weight: 700; font-family: 'Sora', sans-serif;
    border: 2px solid rgba(255,255,255,0.25);
}
.faculty-name { font-family: 'Sora', sans-serif; font-size: 1.3rem; font-weight: 700; }
.faculty-meta { font-size: 0.82rem; color: rgba(255,255,255,0.7); margin-top: 2px; }

div[data-testid="stRadio"] > div { gap: 4px; }
div[data-testid="stRadio"] label {
    border-radius: 8px; padding: 8px 12px !important;
    transition: background 0.15s; cursor: pointer; width: 100%;
}
div[data-testid="stRadio"] label:hover { background: rgba(255,255,255,0.06); }

.divider { border: none; border-top: 1px solid #e2e8f0; margin: 1.4rem 0; }
.dataframe th { background: #f1f5f9 !important; color: #475569 !important; font-size: 0.8rem !important; font-weight: 600 !important; }
.dataframe td { font-size: 0.85rem !important; color: #1e293b !important; }
</style>
""", unsafe_allow_html=True)

# ─── Dummy Data ───────────────────────────────────────────────────────────────
random.seed(7)

DEPARTMENTS = ["CSE", "ECE", "ME", "CE", "EEE"]

BATCHES = ["2022-26", "2023-27", "2024-28", "2021-25"]

SECTIONS = [
    {"id": "CSE-A", "dept": "CSE", "semester": "S6", "batch": "2022-26", "strength": 60, "advisor": "Dr. Arjun Nair",     "room": "CS-301"},
    {"id": "CSE-B", "dept": "CSE", "semester": "S6", "batch": "2022-26", "strength": 58, "advisor": "Dr. Meera Pillai",   "room": "CS-302"},
    {"id": "ECE-A", "dept": "ECE", "semester": "S4", "batch": "2023-27", "strength": 55, "advisor": "Dr. Sreejith R.",    "room": "EC-201"},
    {"id": "ME-A",  "dept": "ME",  "semester": "S4", "batch": "2023-27", "strength": 52, "advisor": "Prof. Binu K.",      "room": "ME-101"},
    {"id": "CE-A",  "dept": "CE",  "semester": "S2", "batch": "2024-28", "strength": 50, "advisor": "Prof. Anitha S.",    "room": "CV-102"},
    {"id": "EEE-A", "dept": "EEE", "semester": "S6", "batch": "2022-26", "strength": 48, "advisor": "Dr. Rajesh T.",      "room": "EE-303"},
]

SUBJECTS = [
    {"code": "CS301", "name": "Data Structures & Algorithms",  "dept": "CSE", "sem": "S6", "credits": 4, "type": "Theory",   "faculty": "Dr. Arjun Nair",      "enrolled": 118},
    {"code": "CS302", "name": "Operating Systems",             "dept": "CSE", "sem": "S6", "credits": 4, "type": "Theory",   "faculty": "Dr. Meera Pillai",    "enrolled": 118},
    {"code": "CS303", "name": "Database Management Systems",   "dept": "CSE", "sem": "S6", "credits": 3, "type": "Theory",   "faculty": "Prof. Ravi Kumar",    "enrolled": 118},
    {"code": "CS304", "name": "Computer Networks",             "dept": "CSE", "sem": "S6", "credits": 3, "type": "Theory",   "faculty": "Dr. Suja Menon",      "enrolled": 118},
    {"code": "CS305", "name": "DSA Lab",                       "dept": "CSE", "sem": "S6", "credits": 2, "type": "Lab",      "faculty": "Dr. Arjun Nair",      "enrolled": 118},
    {"code": "CS306", "name": "DBMS Lab",                      "dept": "CSE", "sem": "S6", "credits": 2, "type": "Lab",      "faculty": "Prof. Ravi Kumar",    "enrolled": 118},
    {"code": "EC401", "name": "VLSI Design",                   "dept": "ECE", "sem": "S4", "credits": 4, "type": "Theory",   "faculty": "Dr. Sreejith R.",     "enrolled": 55},
    {"code": "EC402", "name": "Digital Signal Processing",     "dept": "ECE", "sem": "S4", "credits": 4, "type": "Theory",   "faculty": "Dr. Priya Varma",     "enrolled": 55},
    {"code": "ME301", "name": "Thermodynamics",                "dept": "ME",  "sem": "S4", "credits": 4, "type": "Theory",   "faculty": "Prof. Binu K.",       "enrolled": 52},
    {"code": "ME302", "name": "Fluid Mechanics",               "dept": "ME",  "sem": "S4", "credits": 3, "type": "Theory",   "faculty": "Dr. Arun George",     "enrolled": 52},
    {"code": "EE501", "name": "Power Systems",                 "dept": "EEE", "sem": "S6", "credits": 4, "type": "Theory",   "faculty": "Dr. Rajesh T.",       "enrolled": 48},
    {"code": "HS101", "name": "Engineering Mathematics",       "dept": "All", "sem": "S2", "credits": 4, "type": "Theory",   "faculty": "Dr. Lekha V.",        "enrolled": 323},
    {"code": "HS102", "name": "Engineering Physics",           "dept": "All", "sem": "S2", "credits": 3, "type": "Theory",   "faculty": "Dr. Thomas J.",       "enrolled": 323},
]

STUDENTS = [
    {"reg": "TVE22CS001", "name": "Aditya Sharma",   "section": "CSE-A", "dept": "CSE", "sem": "S6", "batch": "2022-26", "gender": "M", "dob": "2003-04-10", "email": "aditya@tve.edu",   "phone": "9876501001", "cgpa": 8.9, "guardian": "Rajan Sharma",   "city": "Kochi"},
    {"reg": "TVE22CS002", "name": "Bhavana Nair",    "section": "CSE-A", "dept": "CSE", "sem": "S6", "batch": "2022-26", "gender": "F", "dob": "2003-07-21", "email": "bhavana@tve.edu",  "phone": "9876501002", "cgpa": 9.2, "guardian": "Suresh Nair",    "city": "Thrissur"},
    {"reg": "TVE22CS003", "name": "Chetan Pillai",   "section": "CSE-A", "dept": "CSE", "sem": "S6", "batch": "2022-26", "gender": "M", "dob": "2003-01-15", "email": "chetan@tve.edu",   "phone": "9876501003", "cgpa": 7.8, "guardian": "Mohan Pillai",   "city": "Ernakulam"},
    {"reg": "TVE22CS004", "name": "Deepthi Menon",   "section": "CSE-B", "dept": "CSE", "sem": "S6", "batch": "2022-26", "gender": "F", "dob": "2003-09-05", "email": "deepthi@tve.edu",  "phone": "9876501004", "cgpa": 8.5, "guardian": "Anoop Menon",    "city": "Palakkad"},
    {"reg": "TVE22CS005", "name": "Edwin Jose",      "section": "CSE-B", "dept": "CSE", "sem": "S6", "batch": "2022-26", "gender": "M", "dob": "2003-11-30", "email": "edwin@tve.edu",    "phone": "9876501005", "cgpa": 6.9, "guardian": "Biju Jose",       "city": "Kottayam"},
    {"reg": "TVE23EC001", "name": "Fathima Rasheed", "section": "ECE-A", "dept": "ECE", "sem": "S4", "batch": "2023-27", "gender": "F", "dob": "2004-02-18", "email": "fathima@tve.edu",  "phone": "9876501006", "cgpa": 8.1, "guardian": "Abdul Rasheed",  "city": "Kozhikode"},
    {"reg": "TVE23EC002", "name": "Gautham Iyer",    "section": "ECE-A", "dept": "ECE", "sem": "S4", "batch": "2023-27", "gender": "M", "dob": "2004-06-09", "email": "gautham@tve.edu",  "phone": "9876501007", "cgpa": 7.5, "guardian": "Srini Iyer",     "city": "Chennai"},
    {"reg": "TVE23ME001", "name": "Hari Krishna",    "section": "ME-A",  "dept": "ME",  "sem": "S4", "batch": "2023-27", "gender": "M", "dob": "2004-08-22", "email": "hari@tve.edu",     "phone": "9876501008", "cgpa": 7.2, "guardian": "Gopalan K.",     "city": "Thrissur"},
    {"reg": "TVE24CE001", "name": "Ishita Varma",    "section": "CE-A",  "dept": "CE",  "sem": "S2", "batch": "2024-28", "gender": "F", "dob": "2005-03-14", "email": "ishita@tve.edu",   "phone": "9876501009", "cgpa": 8.7, "guardian": "Pradeep Varma",  "city": "Calicut"},
    {"reg": "TVE22EE001", "name": "Jijo Thomas",     "section": "EEE-A", "dept": "EEE", "sem": "S6", "batch": "2022-26", "gender": "M", "dob": "2003-12-01", "email": "jijo@tve.edu",     "phone": "9876501010", "cgpa": 8.3, "guardian": "Thomas P.",      "city": "Alappuzha"},
]

SUBJ_NAMES_CSE = ["Data Structures & Algorithms", "Operating Systems", "Database Management Systems", "Computer Networks", "DSA Lab"]

def gen_attendance():
    today = date.today()
    rows = []
    periods = ["P1 (9:00)", "P2 (10:00)", "P3 (11:00)", "P4 (12:00)", "P5 (14:00)", "P6 (15:00)"]
    for s in STUDENTS:
        for i in range(30):
            d = today - timedelta(days=i)
            if d.weekday() < 5:
                for period in periods[:4]:
                    rows.append({
                        "Reg No": s["reg"], "Name": s["name"], "Section": s["section"], "Dept": s["dept"],
                        "Date": d.strftime("%Y-%m-%d"), "Period": period,
                        "Subject": random.choice(SUBJ_NAMES_CSE),
                        "Status": random.choices(["Present", "Absent", "OD", "Leave"], weights=[78, 13, 5, 4])[0],
                    })
    return pd.DataFrame(rows)

def gen_marks():
    rows = []
    exams = ["Series Test I", "Series Test II", "End Semester"]
    for s in STUDENTS:
        for subj in SUBJ_NAMES_CSE:
            for exam in exams:
                max_m = 30 if "Series" in exam else 100
                rows.append({
                    "Reg No": s["reg"], "Name": s["name"], "Section": s["section"],
                    "Subject": subj, "Exam": exam,
                    "Max Marks": max_m,
                    "Marks": random.randint(int(max_m * 0.55), max_m),
                })
    return pd.DataFrame(rows)

ATT_DF   = gen_attendance()
MARKS_DF = gen_marks()

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0.5rem 1.4rem;">
        <div style="font-family:'Sora',sans-serif;font-size:1.1rem;font-weight:700;color:#f8fafc;letter-spacing:-0.01em;">
            ⚙️ TechVerse Engineering
        </div>
        <div style="font-size:0.72rem;color:#475569;margin-top:2px;font-weight:500;">Faculty Portal · Autonomous</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.68rem;color:#334155;text-transform:uppercase;letter-spacing:0.08em;font-weight:600;padding-left:4px;margin-bottom:6px;'>Navigation</div>", unsafe_allow_html=True)

    page = st.radio(
        "",
        ["📋  Overview", "🗓  Attendance", "📊  Marks", "👤  Student Details", "🏛  Sections", "📚  Courses"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#1a2236;margin:1.2rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.72rem;color:#475569;padding: 0 4px;">
        <div style="font-weight:600;color:#94a3b8;margin-bottom:4px;">Logged in as</div>
        <div style="color:#f1f5f9;font-weight:600;">Dr. Arjun Nair</div>
        <div style="color:#64748b;">Assoc. Professor · CSE Dept</div>
        <div style="color:#64748b;margin-top:2px;">Section Advisor · CSE-A (S6)</div>
        <div style="margin-top:12px;color:#64748b;">Academic Year</div>
        <div style="color:#94a3b8;font-weight:600;">2025 – 2026 &nbsp;·&nbsp; Even Semester</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.7rem;color:#334155;text-align:center;padding-top:1.4rem;">
        TechVerse ERP v3.1 · NAAC A+ Accredited
    </div>
    """, unsafe_allow_html=True)

# ─── Faculty Hero Card ────────────────────────────────────────────────────────
st.markdown("""
<div class="faculty-hero">
    <div class="faculty-avatar">AN</div>
    <div>
        <div class="faculty-name">Dr. Arjun Nair</div>
        <div class="faculty-meta">Faculty ID: TVE-FCL-0118 &nbsp;·&nbsp; Dept of Computer Science & Engineering &nbsp;·&nbsp; Associate Professor</div>
        <div class="faculty-meta" style="margin-top:6px;">
            <span style="background:rgba(255,255,255,0.15);border-radius:6px;padding:2px 10px;font-size:0.7rem;">
                ✅ Active
            </span>
            &nbsp; Specialisation: Algorithms & Distributed Systems &nbsp;·&nbsp; Ph.D — IIT Bombay &nbsp;·&nbsp; Exp: 11 yrs
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
#   PAGE: OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "📋  Overview":
    st.markdown('<div class="page-title">Faculty Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Academic snapshot — Even Semester 2025-26 · TechVerse Engineering College</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-row">
        <div class="stat-card">
            <div class="accent-bar" style="background:#0ea5e9;"></div>
            <div class="label">Total Students</div>
            <div class="value">323</div>
            <div class="delta">↑ 18 from last batch</div>
        </div>
        <div class="stat-card">
            <div class="accent-bar" style="background:#22c55e;"></div>
            <div class="label">Avg Attendance</div>
            <div class="value">83%</div>
            <div class="delta">↑ 1.5% this month</div>
        </div>
        <div class="stat-card">
            <div class="accent-bar" style="background:#f59e0b;"></div>
            <div class="label">Sections</div>
            <div class="value">6</div>
            <div class="delta">Across 5 departments</div>
        </div>
        <div class="stat-card">
            <div class="accent-bar" style="background:#8b5cf6;"></div>
            <div class="label">Courses Running</div>
            <div class="value">13</div>
            <div class="delta">6 theory · 2 lab · 5 others</div>
        </div>
        <div class="stat-card">
            <div class="accent-bar" style="background:#ec4899;"></div>
            <div class="label">Internal Marks Due</div>
            <div class="value">21</div>
            <div class="delta" style="color:#f43f5e;">Deadline: Sep 20</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown('<div class="section-header">Attendance — Last 7 Working Days</div>', unsafe_allow_html=True)
        today = date.today()
        weekly = []
        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            if d.weekday() < 5:
                day_df  = ATT_DF[ATT_DF["Date"] == d.strftime("%Y-%m-%d")]
                total   = len(day_df)
                present = len(day_df[day_df["Status"] == "Present"])
                pct     = round(present / total * 100) if total else 0
                weekly.append({"Day": d.strftime("%a %d"), "Present %": pct})
        if weekly:
            st.bar_chart(pd.DataFrame(weekly).set_index("Day"), height=220, color="#0ea5e9")

        st.markdown('<div class="section-header" style="margin-top:1.5rem;">Academic Alerts</div>', unsafe_allow_html=True)
        alerts = [
            ("🔴", "5 students below 75% attendance — CSE-A (mandatory condonation risk)", "Urgent"),
            ("🟡", "Series Test II results must be uploaded before Sep 20", "Reminder"),
            ("🟢", "ECE-A achieved 91% attendance this week — excellent!", "Info"),
            ("🟡", "Board of Studies meeting scheduled: Sep 25 · CS Seminar Hall", "Reminder"),
            ("🔴", "2 lab records submission pending — CS305 (DSA Lab)", "Urgent"),
        ]
        for icon, msg, kind in alerts:
            color = {"Urgent": "#fee2e2", "Reminder": "#fef3c7", "Info": "#dcfce7"}[kind]
            tc    = {"Urgent": "#991b1b", "Reminder": "#92400e", "Info": "#166534"}[kind]
            st.markdown(f"""
            <div style="background:{color};border-radius:10px;padding:0.7rem 1rem;
                        display:flex;align-items:center;gap:0.7rem;margin-bottom:0.5rem;">
                <span style="font-size:1rem;">{icon}</span>
                <span style="color:{tc};font-size:0.84rem;">{msg}</span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">My Sections</div>', unsafe_allow_html=True)
        for sec in SECTIONS[:4]:
            st.markdown(f"""
            <div class="info-card" style="margin-bottom:0.7rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div style="font-family:'Sora',sans-serif;font-size:1rem;font-weight:700;color:#0f172a;">
                            {sec['id']} &nbsp;<span style="font-size:0.75rem;color:#64748b;">· {sec['semester']}</span>
                        </div>
                        <div style="font-size:0.77rem;color:#64748b;margin-top:2px;">{sec['advisor']} · {sec['room']}</div>
                        <div style="font-size:0.75rem;color:#94a3b8;">Batch {sec['batch']}</div>
                    </div>
                    <div style="background:#e0f2fe;color:#0369a1;padding:3px 10px;border-radius:8px;font-size:0.8rem;font-weight:600;">
                        {sec['strength']} students
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:1rem;">Dept-wise Enrollment</div>', unsafe_allow_html=True)
        dept_counts = {sec["dept"]: sec["strength"] for sec in SECTIONS}
        enroll_df = pd.DataFrame({"Students": dept_counts})
        st.bar_chart(enroll_df, height=190, color="#8b5cf6")

# ════════════════════════════════════════════════════════════════════════════
#   PAGE: ATTENDANCE
# ════════════════════════════════════════════════════════════════════════════
elif page == "🗓  Attendance":
    st.markdown('<div class="page-title">Attendance Register</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Period-wise attendance entry, shortage alerts, and OD management</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📅  Mark Attendance", "📈  Shortage Report", "🔍  Student Lookup"])

    with tab1:
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            sel_section = st.selectbox("Section", [s["id"] for s in SECTIONS])
        with col_b:
            sel_date = st.date_input("Date", value=date.today())
        with col_c:
            sel_period = st.selectbox("Period / Hour", ["P1 (9:00–10:00)", "P2 (10:00–11:00)", "P3 (11:00–12:00)", "P4 (12:00–13:00)", "P5 (14:00–15:00)", "P6 (15:00–16:00)"])
        with col_d:
            sel_subj = st.selectbox("Subject / Course", [s["name"] for s in SUBJECTS if s["dept"] in ["CSE", "All"]])

        sec_students = [s for s in STUDENTS if s["section"] == sel_section]
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown(f'<div class="section-header">Marking — {sel_section} · {sel_period} · {sel_date}</div>', unsafe_allow_html=True)

        header_cols = st.columns([2, 4, 3, 3])
        for h, c in zip(["Reg No", "Name", "Status", "Remark"], header_cols):
            c.markdown(f"<div style='font-size:0.73rem;font-weight:600;color:#94a3b8;text-transform:uppercase;'>{h}</div>", unsafe_allow_html=True)

        statuses = {}
        for s in sec_students:
            cols = st.columns([2, 4, 3, 3])
            cols[0].markdown(f"<div style='padding-top:8px;color:#64748b;font-size:0.8rem;'>{s['reg']}</div>", unsafe_allow_html=True)
            cols[1].markdown(f"<div style='padding-top:8px;font-weight:500;color:#0f172a;'>{s['name']}</div>", unsafe_allow_html=True)
            statuses[s["reg"]] = cols[2].selectbox("", ["Present", "Absent", "OD", "Leave"], key=f"att_{s['reg']}", label_visibility="collapsed")
            cols[3].text_input("", placeholder="OD letter no. / note", key=f"rem_{s['reg']}", label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾  Save Attendance", type="primary"):
            present_ct = sum(1 for v in statuses.values() if v == "Present")
            st.success(f"✅ Attendance saved — {len(sec_students)} students · {present_ct} Present · {len(sec_students)-present_ct} Others.")

    with tab2:
        f_sec  = st.selectbox("Section", ["All"] + [s["id"] for s in SECTIONS], key="short_sec")
        df = ATT_DF.copy()
        if f_sec != "All":
            df = df[df["Section"] == f_sec]

        # Aggregate per student
        total_periods = df.groupby(["Reg No", "Name", "Section", "Dept"])["Status"].count().reset_index(name="Total Periods")
        present_ct    = df[df["Status"].isin(["Present", "OD"])].groupby("Reg No")["Status"].count().reset_index(name="Attended")
        summary = total_periods.merge(present_ct, on="Reg No", how="left").fillna(0)
        summary["Attendance %"] = (summary["Attended"] / summary["Total Periods"] * 100).round(1)
        summary["Status"] = summary["Attendance %"].apply(lambda x: "⚠️ Shortage" if x < 75 else "✅ OK")

        def att_style(val):
            if isinstance(val, float):
                if val < 75: return "color:#dc2626;font-weight:700"
                if val < 85: return "color:#d97706;font-weight:600"
                return "color:#16a34a;font-weight:600"
            return ""

        st.dataframe(
            summary[["Reg No", "Name", "Section", "Dept", "Total Periods", "Attended", "Attendance %", "Status"]]
            .style.map(att_style, subset=["Attendance %"]),
            use_container_width=True, hide_index=True,
        )

        shortage = summary[summary["Attendance %"] < 75]
        c1, c2, c3 = st.columns(3)
        c1.metric("Students with Shortage", len(shortage))
        c2.metric("Overall Avg Attendance", f"{summary['Attendance %'].mean():.1f}%")
        c3.metric("Students Above 85%", len(summary[summary["Attendance %"] >= 85]))

    with tab3:
        sel_s = st.selectbox("Select Student", [s["name"] + " · " + s["reg"] for s in STUDENTS])
        reg   = sel_s.split("·")[1].strip()
        s_att = ATT_DF[ATT_DF["Reg No"] == reg].sort_values("Date", ascending=False)

        p  = len(s_att[s_att["Status"].isin(["Present", "OD"])])
        ab = len(s_att[s_att["Status"] == "Absent"])
        od = len(s_att[s_att["Status"] == "OD"])
        lv = len(s_att[s_att["Status"] == "Leave"])
        total = len(s_att)
        pct = round(p / total * 100, 1) if total else 0

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Attendance %", f"{pct}%")
        c2.metric("Present", p)
        c3.metric("Absent", ab)
        c4.metric("OD", od)
        c5.metric("Leave", lv)

        if pct < 75:
            st.error(f"⚠️ Attendance below 75% — student may be detained. Condonation required.")
        elif pct < 85:
            st.warning("📌 Attendance below 85% — caution advised.")

        st.dataframe(s_att[["Date", "Period", "Subject", "Status"]].reset_index(drop=True), use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
#   PAGE: MARKS
# ════════════════════════════════════════════════════════════════════════════
elif page == "📊  Marks":
    st.markdown('<div class="page-title">Internal Assessment & Marks</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Series tests, end-semester internals, lab evaluations and CGPA tracker</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📝  Enter Marks", "📋  Mark Sheet", "📈  Performance Analysis"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            m_sec  = st.selectbox("Section", [s["id"] for s in SECTIONS], key="m_sec")
            m_subj = st.selectbox("Subject", [s["name"] for s in SUBJECTS if s["dept"] in ["CSE","All"]], key="m_subj")
        with col2:
            m_exam = st.selectbox("Examination", ["Series Test I", "Series Test II", "Model Exam", "End Semester", "Lab Internal", "Lab External", "Assignment"], key="m_exam")
            m_max  = st.number_input("Max Marks", value=30 if "Series" in st.session_state.get("m_exam", "") else 100, step=5, key="m_max")
        with col3:
            m_date = st.date_input("Exam Date", key="m_date")
            m_dept = st.selectbox("Department", DEPARTMENTS, key="m_dept")

        sec_students = [s for s in STUDENTS if s["section"] == m_sec]
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown(f'<div class="section-header">Enter Marks — {m_subj} · {m_exam} · {m_sec}</div>', unsafe_allow_html=True)

        header_cols = st.columns([2, 4, 2, 2, 2])
        for h, c in zip(["Reg No", "Name", f"Marks /{m_max}", "Grade", "Result"], header_cols):
            c.markdown(f"<div style='font-size:0.73rem;font-weight:600;color:#94a3b8;text-transform:uppercase;'>{h}</div>", unsafe_allow_html=True)

        for s in sec_students:
            cols = st.columns([2, 4, 2, 2, 2])
            cols[0].markdown(f"<div style='padding-top:8px;color:#64748b;font-size:0.8rem;'>{s['reg']}</div>", unsafe_allow_html=True)
            cols[1].markdown(f"<div style='padding-top:8px;font-weight:500;color:#0f172a;'>{s['name']}</div>", unsafe_allow_html=True)
            score = cols[2].number_input("", 0, int(m_max), value=random.randint(int(m_max*0.6), int(m_max)), key=f"mk_{s['reg']}", label_visibility="collapsed")
            pct   = score / m_max * 100
            grade = "O" if pct >= 90 else "A+" if pct >= 85 else "A" if pct >= 75 else "B+" if pct >= 65 else "B" if pct >= 55 else "C"
            result = "Pass" if pct >= 50 else "Fail"
            gmap  = {"O":"badge-green","A+":"badge-blue","A":"badge-cyan","B+":"badge-purple","B":"badge-amber","C":"badge-amber"}
            cols[3].markdown(f"<div style='padding-top:8px;'><span class='badge {gmap[grade]}'>{grade}</span></div>", unsafe_allow_html=True)
            cols[4].markdown(f"<div style='padding-top:8px;'><span class='badge {'badge-green' if result=='Pass' else 'badge-red'}'>{result}</span></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾  Save Marks", type="primary"):
            st.success(f"✅ Marks saved for {len(sec_students)} students — {m_subj} · {m_exam}")

    with tab2:
        f_sec  = st.selectbox("Section", ["All"] + [s["id"] for s in SECTIONS], key="gs_sec")
        f_subj = st.selectbox("Subject", ["All"] + [s["name"] for s in SUBJECTS if s["dept"] in ["CSE","All"]], key="gs_subj")
        f_exam = st.selectbox("Exam", ["All"] + ["Series Test I", "Series Test II", "End Semester"], key="gs_exam")

        df = MARKS_DF.copy()
        if f_sec  != "All": df = df[df["Section"] == f_sec]
        if f_subj != "All": df = df[df["Subject"] == f_subj]
        if f_exam != "All": df = df[df["Exam"] == f_exam]

        df["Percentage"] = (df["Marks"] / df["Max Marks"] * 100).round(1)
        df["Grade"] = df["Percentage"].apply(lambda x: "O" if x>=90 else "A+" if x>=85 else "A" if x>=75 else "B+" if x>=65 else "B" if x>=55 else "C")
        df["Result"] = df["Percentage"].apply(lambda x: "Pass" if x>=50 else "Fail")

        def mark_style(val):
            if isinstance(val, float):
                if val >= 85: return "background-color:#dcfce7;color:#15803d"
                if val >= 70: return "background-color:#dbeafe;color:#1d4ed8"
                if val >= 55: return "background-color:#fef3c7;color:#b45309"
                return "background-color:#fee2e2;color:#b91c1c"
            return ""

        st.dataframe(
            df[["Reg No","Name","Section","Subject","Exam","Marks","Max Marks","Percentage","Grade","Result"]]
            .style.map(mark_style, subset=["Percentage"]),
            use_container_width=True, hide_index=True,
        )

    with tab3:
        p_subj = st.selectbox("Subject", [s["name"] for s in SUBJECTS if s["dept"] in ["CSE","All"]], key="perf_subj")
        p_exam = st.selectbox("Exam", ["Series Test I", "Series Test II", "End Semester"], key="perf_exam")
        df_sub = MARKS_DF[(MARKS_DF["Subject"] == p_subj) & (MARKS_DF["Exam"] == p_exam)].copy()
        df_sub["Percentage"] = (df_sub["Marks"] / df_sub["Max Marks"] * 100).round(1)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-header">Score Distribution</div>', unsafe_allow_html=True)
            hist = pd.cut(df_sub["Percentage"], bins=[0,50,60,70,80,90,100], labels=["<50","50-60","60-70","70-80","80-90","90-100"]).value_counts().sort_index()
            st.bar_chart(pd.DataFrame({"Students": hist}), color="#0ea5e9", height=220)
        with col2:
            st.markdown('<div class="section-header">Grade Distribution</div>', unsafe_allow_html=True)
            df_sub["Grade"] = df_sub["Percentage"].apply(lambda x: "O" if x>=90 else "A+" if x>=85 else "A" if x>=75 else "B+" if x>=65 else "B" if x>=55 else "C")
            grade_counts = df_sub["Grade"].value_counts().reindex(["O","A+","A","B+","B","C"], fill_value=0)
            st.bar_chart(pd.DataFrame({"Count": grade_counts}), color="#8b5cf6", height=220)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Class Average", f"{df_sub['Percentage'].mean():.1f}%")
        c2.metric("Highest Score", f"{df_sub['Percentage'].max():.1f}%")
        c3.metric("Pass %", f"{(df_sub['Percentage']>=50).mean()*100:.1f}%")
        c4.metric("Students Scored O/A+", str(len(df_sub[df_sub['Percentage']>=85])))

# ════════════════════════════════════════════════════════════════════════════
#   PAGE: STUDENT DETAILS
# ════════════════════════════════════════════════════════════════════════════
elif page == "👤  Student Details":
    st.markdown('<div class="page-title">Student Profiles</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Reg number, CGPA, academic history, contact and guardian details</div>', unsafe_allow_html=True)

    col_s, col_f1, col_f2 = st.columns([3, 1, 1])
    with col_s:
        search_q = st.text_input("Search by name or Register No.", placeholder="e.g. Bhavana or TVE22CS002")
    with col_f1:
        f_dept = st.selectbox("Department", ["All"] + DEPARTMENTS, key="sd_dept")
    with col_f2:
        f_batch = st.selectbox("Batch", ["All"] + BATCHES, key="sd_batch")

    filtered = STUDENTS
    if search_q:
        filtered = [s for s in filtered if search_q.lower() in s["name"].lower() or search_q.lower() in s["reg"].lower()]
    if f_dept != "All":
        filtered = [s for s in filtered if s["dept"] == f_dept]
    if f_batch != "All":
        filtered = [s for s in filtered if s["batch"] == f_batch]

    st.markdown(f"<div style='font-size:0.8rem;color:#64748b;margin-bottom:1rem;'>{len(filtered)} student(s) found</div>", unsafe_allow_html=True)

    for s in filtered:
        cgpa_badge = "badge-green" if s["cgpa"] >= 8.5 else "badge-blue" if s["cgpa"] >= 7.0 else "badge-amber"
        with st.expander(f"  {s['name']}  ·  {s['reg']}  ·  {s['dept']} {s['sem']}  ·  CGPA {s['cgpa']}"):
            c1, c2, c3 = st.columns(3)
            fields_left  = [("Register No.", s["reg"]), ("Full Name", s["name"]), ("Department", s["dept"]), ("Section", s["section"])]
            fields_mid   = [("Semester", s["sem"]), ("Batch", s["batch"]), ("CGPA", str(s["cgpa"])), ("Date of Birth", s["dob"])]
            fields_right = [("Email", s["email"]), ("Phone", s["phone"]), ("Guardian", s["guardian"]), ("City", s["city"])]

            for lbl, val in fields_left:
                c1.markdown(f"<div class='info-card'><div class='card-label'>{lbl}</div><div class='card-value'>{val}</div></div>", unsafe_allow_html=True)
            for lbl, val in fields_mid:
                c2.markdown(f"<div class='info-card'><div class='card-label'>{lbl}</div><div class='card-value'>{val}</div></div>", unsafe_allow_html=True)
            for lbl, val in fields_right:
                c3.markdown(f"<div class='info-card'><div class='card-label'>{lbl}</div><div class='card-value'>{val}</div></div>", unsafe_allow_html=True)

            s_marks = MARKS_DF[MARKS_DF["Reg No"] == s["reg"]][["Subject", "Exam", "Marks", "Max Marks"]].copy()
            s_marks["Percentage"] = (s_marks["Marks"] / s_marks["Max Marks"] * 100).round(1)
            st.markdown('<div class="section-header" style="margin-top:0.5rem;">Assessment Summary</div>', unsafe_allow_html=True)
            st.dataframe(s_marks.reset_index(drop=True), use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
#   PAGE: SECTIONS
# ════════════════════════════════════════════════════════════════════════════
elif page == "🏛  Sections":
    st.markdown('<div class="page-title">Sections & Batches</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Manage section assignments, advisors, timetable rooms and batch details</div>', unsafe_allow_html=True)

    col_stats = st.columns(4)
    col_stats[0].metric("Total Sections",  len(SECTIONS))
    col_stats[1].metric("Total Students",  sum(s["strength"] for s in SECTIONS))
    col_stats[2].metric("Departments",     len(DEPARTMENTS))
    col_stats[3].metric("Active Batches",  len(set(s["batch"] for s in SECTIONS)))

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    f_dept_s = st.radio("Filter by Department", ["All"] + DEPARTMENTS, horizontal=True, key="sec_dept_filter")
    display_secs = SECTIONS if f_dept_s == "All" else [s for s in SECTIONS if s["dept"] == f_dept_s]

    for sec in display_secs:
        dept_colors = {"CSE": "badge-blue", "ECE": "badge-purple", "ME": "badge-amber", "CE": "badge-green", "EEE": "badge-cyan"}
        dc = dept_colors.get(sec["dept"], "badge-slate")
        st.markdown(f"""
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.3rem 1.6rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.8rem;">
                <div>
                    <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:4px;">
                        <span style="font-family:'Sora',sans-serif;font-size:1.1rem;font-weight:700;color:#0f172a;">
                            Section {sec['id']}
                        </span>
                        <span class="badge {dc}">{sec['dept']}</span>
                        <span class="badge badge-slate">{sec['semester']}</span>
                    </div>
                    <div style="font-size:0.82rem;color:#64748b;">
                        Section Advisor: {sec['advisor']} &nbsp;·&nbsp; Room: {sec['room']} &nbsp;·&nbsp; Batch: {sec['batch']}
                    </div>
                </div>
                <div style="display:flex;gap:0.6rem;align-items:center;flex-wrap:wrap;">
                    <span class="badge badge-blue">🎓 {sec['strength']} students</span>
                    <span class="badge badge-green">✅ Active</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"View students — {sec['id']}"):
            sec_studs = [s for s in STUDENTS if s["section"] == sec["id"]]
            if sec_studs:
                df = pd.DataFrame([{
                    "Reg No": s["reg"], "Name": s["name"],
                    "Gender": "M" if s["gender"]=="M" else "F",
                    "CGPA": s["cgpa"], "Email": s["email"],
                } for s in sec_studs])
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No students linked to this section in the sample data.")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Create New Section</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    ns_id      = col1.text_input("Section ID", placeholder="e.g. CSE-C")
    ns_dept    = col2.selectbox("Department", DEPARTMENTS, key="ns_dept")
    ns_sem     = col3.selectbox("Semester", ["S1","S2","S3","S4","S5","S6","S7","S8"], key="ns_sem")
    ns_batch   = col4.text_input("Batch", placeholder="e.g. 2024-28")
    ns_advisor = col1.text_input("Section Advisor", placeholder="Full name with designation")
    ns_room    = col2.text_input("Room / Lab", placeholder="e.g. CS-401")
    if st.button("➕  Create Section", type="primary"):
        if ns_id and ns_advisor and ns_room:
            st.success(f"✅ Section '{ns_id}' ({ns_dept} · {ns_sem}) created. Advisor: {ns_advisor} · Room: {ns_room}")
        else:
            st.error("Section ID, Advisor and Room are required.")

# ════════════════════════════════════════════════════════════════════════════
#   PAGE: COURSES
# ════════════════════════════════════════════════════════════════════════════
elif page == "📚  Courses":
    st.markdown('<div class="page-title">Courses & Curriculum</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">University syllabus, credit structure, lab courses and faculty mapping</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋  Course Catalogue", "➕  Register Course"])

    with tab1:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            f_dept_c = st.selectbox("Department", ["All"] + DEPARTMENTS + ["All Depts"], key="c_dept")
        with col_f2:
            f_type_c = st.radio("Type", ["All", "Theory", "Lab"], horizontal=True, key="c_type")
        with col_f3:
            f_sem_c  = st.selectbox("Semester", ["All", "S2", "S4", "S6"], key="c_sem")

        disp = SUBJECTS
        if f_dept_c not in ["All", "All Depts"]: disp = [c for c in disp if c["dept"] == f_dept_c]
        if f_type_c != "All":                    disp = [c for c in disp if c["type"] == f_type_c]
        if f_sem_c  != "All":                    disp = [c for c in disp if c["sem"]  == f_sem_c]

        for course in disp:
            type_badge = "badge-blue" if course["type"] == "Theory" else "badge-purple"
            dept_badge = {"CSE":"badge-blue","ECE":"badge-purple","ME":"badge-amber","CE":"badge-green","EEE":"badge-cyan","All":"badge-slate"}.get(course["dept"], "badge-slate")
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.2rem 1.6rem;margin-bottom:0.9rem;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.7rem;">
                    <div>
                        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:4px;flex-wrap:wrap;">
                            <span style="font-family:'Sora',sans-serif;font-size:1rem;font-weight:700;color:#0f172a;">
                                {course['name']}
                            </span>
                            <span class="badge {type_badge}">{course['type']}</span>
                            <span class="badge {dept_badge}">{course['dept']}</span>
                            <span class="badge badge-slate">{course['sem']}</span>
                        </div>
                        <div style="font-size:0.8rem;color:#64748b;">
                            Course Code: <strong>{course['code']}</strong> &nbsp;·&nbsp;
                            Faculty: {course['faculty']} &nbsp;·&nbsp;
                            Credits: <strong>{course['credits']}</strong>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-family:'Sora',sans-serif;font-size:1.4rem;font-weight:700;color:#0ea5e9;">
                            {course['enrolled']}
                        </div>
                        <div style="font-size:0.72rem;color:#94a3b8;">enrolled</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:1rem;">Credits per Course</div>', unsafe_allow_html=True)
        credits_df = pd.DataFrame({"Credits": {c["code"] + " " + c["name"][:20]: c["credits"] for c in disp}})
        st.bar_chart(credits_df, color="#0ea5e9", height=220)

    with tab2:
        st.markdown('<div class="section-header">Register New Course</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        rc_code    = col1.text_input("Course Code", placeholder="e.g. CS401")
        rc_name    = col2.text_input("Course Name", placeholder="e.g. Machine Learning")
        rc_dept    = col1.selectbox("Department", DEPARTMENTS + ["All Depts"], key="rc_dept")
        rc_sem     = col2.selectbox("Semester", ["S1","S2","S3","S4","S5","S6","S7","S8"], key="rc_sem")
        rc_credits = col1.number_input("Credits", 1, 6, value=4, key="rc_credits")
        rc_type    = col2.selectbox("Course Type", ["Theory", "Lab", "Project", "Seminar", "Elective"], key="rc_type")
        rc_faculty = col1.text_input("Faculty Assigned", placeholder="Dr. / Prof. Full Name")
        rc_hours   = col2.number_input("Hours per Week", 1, 8, value=4, key="rc_hours")
        rc_desc    = st.text_area("Course Objectives", placeholder="Brief outcomes and objectives per university syllabus...")

        if st.button("➕  Register Course", type="primary"):
            if rc_code and rc_name and rc_faculty:
                st.success(f"✅ Course '{rc_name}' ({rc_code}) registered for {rc_dept} · Sem {rc_sem} · Assigned to {rc_faculty}.")
            else:
                st.error("Course Code, Course Name and Faculty are required fields.")