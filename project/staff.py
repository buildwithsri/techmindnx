import streamlit as st
import pandas as pd
import random
from datetime import date, timedelta

# ─── Dummy Data (module-level — generated once on import) ───────────────────
random.seed(7)

DEPARTMENTS = ["CSE", "ECE", "ME", "CE", "EEE"]

BATCHES = ["2022-26", "2023-27", "2024-28", "2021-25"]

SECTIONS = [
    {"id": "CSE-A", "dept": "CSE", "semester": "S6", "batch": "2022-26", "strength": 60, "advisor": "Dr. Arjun Nair",   "room": "CS-301"},
    {"id": "CSE-B", "dept": "CSE", "semester": "S6", "batch": "2022-26", "strength": 58, "advisor": "Dr. Meera Pillai", "room": "CS-302"},
    {"id": "ECE-A", "dept": "ECE", "semester": "S4", "batch": "2023-27", "strength": 55, "advisor": "Dr. Sreejith R.",  "room": "EC-201"},
    {"id": "ME-A",  "dept": "ME",  "semester": "S4", "batch": "2023-27", "strength": 52, "advisor": "Prof. Binu K.",    "room": "ME-101"},
    {"id": "CE-A",  "dept": "CE",  "semester": "S2", "batch": "2024-28", "strength": 50, "advisor": "Prof. Anitha S.",  "room": "CV-102"},
    {"id": "EEE-A", "dept": "EEE", "semester": "S6", "batch": "2022-26", "strength": 48, "advisor": "Dr. Rajesh T.",    "room": "EE-303"},
]

SUBJECTS = [
    {"code": "CS301", "name": "Data Structures & Algorithms",  "dept": "CSE", "sem": "S6", "credits": 4, "type": "Theory", "faculty": "Dr. Arjun Nair",   "enrolled": 118},
    {"code": "CS302", "name": "Operating Systems",             "dept": "CSE", "sem": "S6", "credits": 4, "type": "Theory", "faculty": "Dr. Meera Pillai",  "enrolled": 118},
    {"code": "CS303", "name": "Database Management Systems",   "dept": "CSE", "sem": "S6", "credits": 3, "type": "Theory", "faculty": "Prof. Ravi Kumar",  "enrolled": 118},
    {"code": "CS304", "name": "Computer Networks",             "dept": "CSE", "sem": "S6", "credits": 3, "type": "Theory", "faculty": "Dr. Suja Menon",    "enrolled": 118},
    {"code": "CS305", "name": "DSA Lab",                       "dept": "CSE", "sem": "S6", "credits": 2, "type": "Lab",    "faculty": "Dr. Arjun Nair",   "enrolled": 118},
    {"code": "CS306", "name": "DBMS Lab",                      "dept": "CSE", "sem": "S6", "credits": 2, "type": "Lab",    "faculty": "Prof. Ravi Kumar",  "enrolled": 118},
    {"code": "EC401", "name": "VLSI Design",                   "dept": "ECE", "sem": "S4", "credits": 4, "type": "Theory", "faculty": "Dr. Sreejith R.",   "enrolled": 55},
    {"code": "EC402", "name": "Digital Signal Processing",     "dept": "ECE", "sem": "S4", "credits": 4, "type": "Theory", "faculty": "Dr. Priya Varma",   "enrolled": 55},
    {"code": "ME301", "name": "Thermodynamics",                "dept": "ME",  "sem": "S4", "credits": 4, "type": "Theory", "faculty": "Prof. Binu K.",      "enrolled": 52},
    {"code": "ME302", "name": "Fluid Mechanics",               "dept": "ME",  "sem": "S4", "credits": 3, "type": "Theory", "faculty": "Dr. Arun George",   "enrolled": 52},
    {"code": "EE501", "name": "Power Systems",                 "dept": "EEE", "sem": "S6", "credits": 4, "type": "Theory", "faculty": "Dr. Rajesh T.",     "enrolled": 48},
    {"code": "HS101", "name": "Engineering Mathematics",       "dept": "All", "sem": "S2", "credits": 4, "type": "Theory", "faculty": "Dr. Lekha V.",      "enrolled": 323},
    {"code": "HS102", "name": "Engineering Physics",           "dept": "All", "sem": "S2", "credits": 3, "type": "Theory", "faculty": "Dr. Thomas J.",     "enrolled": 323},
]

STUDENTS = [
    {"reg": "TVE22CS001", "name": "Aditya Sharma",   "section": "CSE-A", "dept": "CSE", "sem": "S6", "batch": "2022-26", "gender": "M", "dob": "2003-04-10", "email": "aditya@tve.edu",   "phone": "9876501001", "cgpa": 8.9, "guardian": "Rajan Sharma",  "city": "Kochi"},
    {"reg": "TVE22CS002", "name": "Bhavana Nair",    "section": "CSE-A", "dept": "CSE", "sem": "S6", "batch": "2022-26", "gender": "F", "dob": "2003-07-21", "email": "bhavana@tve.edu",  "phone": "9876501002", "cgpa": 9.2, "guardian": "Suresh Nair",   "city": "Thrissur"},
    {"reg": "TVE22CS003", "name": "Chetan Pillai",   "section": "CSE-A", "dept": "CSE", "sem": "S6", "batch": "2022-26", "gender": "M", "dob": "2003-01-15", "email": "chetan@tve.edu",   "phone": "9876501003", "cgpa": 7.8, "guardian": "Mohan Pillai",  "city": "Ernakulam"},
    {"reg": "TVE22CS004", "name": "Deepthi Menon",   "section": "CSE-B", "dept": "CSE", "sem": "S6", "batch": "2022-26", "gender": "F", "dob": "2003-09-05", "email": "deepthi@tve.edu",  "phone": "9876501004", "cgpa": 8.5, "guardian": "Anoop Menon",   "city": "Palakkad"},
    {"reg": "TVE22CS005", "name": "Edwin Jose",      "section": "CSE-B", "dept": "CSE", "sem": "S6", "batch": "2022-26", "gender": "M", "dob": "2003-11-30", "email": "edwin@tve.edu",    "phone": "9876501005", "cgpa": 6.9, "guardian": "Biju Jose",      "city": "Kottayam"},
    {"reg": "TVE23EC001", "name": "Fathima Rasheed", "section": "ECE-A", "dept": "ECE", "sem": "S4", "batch": "2023-27", "gender": "F", "dob": "2004-02-18", "email": "fathima@tve.edu",  "phone": "9876501006", "cgpa": 8.1, "guardian": "Abdul Rasheed", "city": "Kozhikode"},
    {"reg": "TVE23EC002", "name": "Gautham Iyer",    "section": "ECE-A", "dept": "ECE", "sem": "S4", "batch": "2023-27", "gender": "M", "dob": "2004-06-09", "email": "gautham@tve.edu",  "phone": "9876501007", "cgpa": 7.5, "guardian": "Srini Iyer",    "city": "Chennai"},
    {"reg": "TVE23ME001", "name": "Hari Krishna",    "section": "ME-A",  "dept": "ME",  "sem": "S4", "batch": "2023-27", "gender": "M", "dob": "2004-08-22", "email": "hari@tve.edu",     "phone": "9876501008", "cgpa": 7.2, "guardian": "Gopalan K.",    "city": "Thrissur"},
    {"reg": "TVE24CE001", "name": "Ishita Varma",    "section": "CE-A",  "dept": "CE",  "sem": "S2", "batch": "2024-28", "gender": "F", "dob": "2005-03-14", "email": "ishita@tve.edu",   "phone": "9876501009", "cgpa": 8.7, "guardian": "Pradeep Varma", "city": "Calicut"},
    {"reg": "TVE22EE001", "name": "Jijo Thomas",     "section": "EEE-A", "dept": "EEE", "sem": "S6", "batch": "2022-26", "gender": "M", "dob": "2003-12-01", "email": "jijo@tve.edu",     "phone": "9876501010", "cgpa": 8.3, "guardian": "Thomas P.",     "city": "Alappuzha"},
]

SUBJ_NAMES_CSE = [
    "Data Structures & Algorithms", "Operating Systems",
    "Database Management Systems", "Computer Networks", "DSA Lab",
]


def gen_attendance():
    today   = date.today()
    rows    = []
    periods = ["P1 (9:00)", "P2 (10:00)", "P3 (11:00)", "P4 (12:00)", "P5 (14:00)", "P6 (15:00)"]
    for s in STUDENTS:
        for i in range(30):
            d = today - timedelta(days=i)
            if d.weekday() < 5:
                for period in periods[:4]:
                    rows.append({
                        "Reg No":  s["reg"], "Name": s["name"],
                        "Section": s["section"], "Dept": s["dept"],
                        "Date":    d.strftime("%Y-%m-%d"), "Period": period,
                        "Subject": random.choice(SUBJ_NAMES_CSE),
                        "Status":  random.choices(
                            ["Present", "Absent", "OD", "Leave"],
                            weights=[78, 13, 5, 4]
                        )[0],
                    })
    return pd.DataFrame(rows)


def gen_marks():
    rows  = []
    exams = ["Series Test I", "Series Test II", "End Semester"]
    for s in STUDENTS:
        for subj in SUBJ_NAMES_CSE:
            for exam in exams:
                max_m = 30 if "Series" in exam else 100
                rows.append({
                    "Reg No":   s["reg"], "Name": s["name"], "Section": s["section"],
                    "Subject":  subj, "Exam": exam,
                    "Max Marks": max_m,
                    "Marks":    random.randint(int(max_m * 0.55), max_m),
                })
    return pd.DataFrame(rows)


ATT_DF   = gen_attendance()
MARKS_DF = gen_marks()


# ─── RENDER — called from app.py ────────────────────────────────────────────

def render(page: str):
    """Render the faculty portal page inside the connected TechVerse app."""

    # ── CSS ───────────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .faculty-hero {
        background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 50%, #2563eb 100%);
        border-radius: 16px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        color: white;
        box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.25);
    }
    .faculty-avatar {
        width: 68px;
        height: 68px;
        border-radius: 50%;
        background: rgba(255,255,255,0.18);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        font-weight: 700;
        font-family: 'Sora', sans-serif;
        border: 2px solid rgba(255,255,255,0.35);
        flex-shrink: 0;
    }
    .faculty-name {
        font-family: 'Sora', sans-serif;
        font-size: 1.45rem;
        font-weight: 700;
        letter-spacing: -0.01em;
    }
    .faculty-meta {
        font-size: 0.86rem;
        color: rgba(255,255,255,0.85);
        margin-top: 3px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Personalised Faculty Hero Card ─────────────────────────────────────────
    user_info    = st.session_state.get("user_info", {})
    display_name = user_info.get("display_name", "Dr. Arjun Nair")
    initials     = user_info.get("initials", "AN")
    title        = user_info.get("title", "Associate Professor · CSE")

    st.markdown(f"""
    <div class="faculty-hero">
        <div class="faculty-avatar">{initials}</div>
        <div>
            <div class="faculty-name">{display_name}</div>
            <div class="faculty-meta">
                Dept of Computer Science &amp; Engineering &nbsp;·&nbsp; <strong>{title}</strong>
            </div>
            <div class="faculty-meta" style="margin-top: 8px;">
                <span style="background: rgba(255,255,255,0.2); border-radius: 99px;
                             padding: 2px 12px; font-size: 0.72rem; font-weight: 600;">✅ Active Faculty</span>
                &nbsp;&nbsp; Academic Year 2025–2026 &nbsp;·&nbsp; Even Semester
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    #  PAGE: OVERVIEW
    # ═══════════════════════════════════════════════════════════════════════════
    if page == "📋  Overview":
        st.markdown('<div class="page-title">Faculty Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Academic snapshot & department telemetry — Even Semester 2025-26 · TechVerse Engineering College</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="stat-row">
            <div class="stat-card">
                <div class="accent-bar" style="background:#0ea5e9;"></div>
                <div class="label">Total Students</div><div class="value">323</div>
                <div class="delta">↑ 18 from last batch</div>
            </div>
            <div class="stat-card">
                <div class="accent-bar" style="background:#22c55e;"></div>
                <div class="label">Avg Attendance</div><div class="value">83%</div>
                <div class="delta">↑ 1.5% this month</div>
            </div>
            <div class="stat-card">
                <div class="accent-bar" style="background:#f59e0b;"></div>
                <div class="label">Assigned Sections</div><div class="value">6</div>
                <div class="delta">Across 5 departments</div>
            </div>
            <div class="stat-card">
                <div class="accent-bar" style="background:#8b5cf6;"></div>
                <div class="label">Courses Active</div><div class="value">13</div>
                <div class="delta">6 theory · 2 lab · 5 elective</div>
            </div>
            <div class="stat-card">
                <div class="accent-bar" style="background:#ec4899;"></div>
                <div class="label">Series II Uploads</div><div class="value">21</div>
                <div class="delta" style="color:#e11d48;">Due: Sep 20</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            st.markdown('<div class="section-header">Attendance Trend — Last 7 Working Days</div>', unsafe_allow_html=True)
            today  = date.today()
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

            st.markdown('<div class="section-header" style="margin-top: 1.5rem;">Academic Notifications & Alerts</div>', unsafe_allow_html=True)
            alerts = [
                ("🔴", "5 students below 75% attendance — CSE-A (mandatory condonation risk)", "Urgent"),
                ("🟡", "Series Test II results must be uploaded before Sep 20", "Reminder"),
                ("🟢", "ECE-A achieved 91% attendance this week — excellent performance", "Info"),
                ("🟡", "Board of Studies meeting scheduled: Sep 25 · CS Seminar Hall", "Reminder"),
                ("🔴", "2 lab record submissions pending — CS305 (DSA Lab)", "Urgent"),
            ]
            for icon, msg, kind in alerts:
                color = {"Urgent": "#fef2f2", "Reminder": "#fffbeb", "Info": "#f0fdf4"}[kind]
                border_c = {"Urgent": "#fecaca", "Reminder": "#fde68a", "Info": "#bbf7d0"}[kind]
                tc    = {"Urgent": "#991b1b", "Reminder": "#92400e", "Info": "#166534"}[kind]
                st.markdown(f"""
                <div style="background:{color};border:1px solid {border_c};border-radius:12px;padding:0.75rem 1.1rem;
                            display:flex;align-items:center;gap:0.75rem;margin-bottom:0.5rem;">
                    <span style="font-size:1.1rem;">{icon}</span>
                    <span style="color:{tc};font-size:0.86rem;font-weight:500;">{msg}</span>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="section-header">My Sections</div>', unsafe_allow_html=True)
            for sec in SECTIONS[:4]:
                st.markdown(f"""
                <div class="info-card" style="margin-bottom:0.7rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-family:'Sora',sans-serif;font-size:1.05rem;font-weight:700;color:#0f172a;">
                                {sec['id']} &nbsp;<span style="font-size:0.78rem;color:#64748b;font-weight:500;">· {sec['semester']}</span>
                            </div>
                            <div style="font-size:0.8rem;color:#64748b;margin-top:2px;">{sec['advisor']} · {sec['room']}</div>
                            <div style="font-size:0.75rem;color:#94a3b8;">Batch {sec['batch']}</div>
                        </div>
                        <div style="background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;padding:4px 12px;border-radius:8px;font-size:0.82rem;font-weight:700;">
                            {sec['strength']} students
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="section-header" style="margin-top: 1.2rem;">Dept-wise Enrollment</div>', unsafe_allow_html=True)
            dept_counts = {sec["dept"]: sec["strength"] for sec in SECTIONS}
            st.bar_chart(pd.DataFrame({"Students": dept_counts}), height=190, color="#8b5cf6")

    # ═══════════════════════════════════════════════════════════════════════════
    #  PAGE: ATTENDANCE
    # ═══════════════════════════════════════════════════════════════════════════
    elif page == "🗓  Attendance":
        st.markdown('<div class="page-title">Attendance Register &amp; Logs</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Period-wise attendance marking, shortage analytics, and official student logbook</div>', unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["📅  Mark Daily Attendance", "📈  Shortage Analytics", "🔍  Student History Lookup"])

        with tab1:
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a: sel_section = st.selectbox("Section", [s["id"] for s in SECTIONS])
            with col_b: sel_date    = st.date_input("Date", value=date.today())
            with col_c: sel_period  = st.selectbox("Period / Hour", ["P1 (9:00–10:00)", "P2 (10:00–11:00)", "P3 (11:00–12:00)", "P4 (12:00–13:00)", "P5 (14:00–15:00)", "P6 (15:00–16:00)"])
            with col_d: sel_subj    = st.selectbox("Subject / Course", [s["name"] for s in SUBJECTS if s["dept"] in ["CSE", "All"]])

            sec_students = [s for s in STUDENTS if s["section"] == sel_section]
            st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
            st.markdown(f'<div class="section-header">Attendance Sheet — {sel_section} · {sel_period} · {sel_date}</div>', unsafe_allow_html=True)

            header_cols = st.columns([2, 4, 3, 3])
            for h, c in zip(["Reg No", "Name", "Status", "Remarks / OD Note"], header_cols):
                c.markdown(f"<div style='font-size:0.74rem;font-weight:700;color:#64748b;text-transform:uppercase;'>{h}</div>", unsafe_allow_html=True)

            statuses = {}
            for s in sec_students:
                cols = st.columns([2, 4, 3, 3])
                cols[0].markdown(f"<div style='padding-top:8px;color:#64748b;font-size:0.84rem;font-family:monospace;'>{s['reg']}</div>", unsafe_allow_html=True)
                cols[1].markdown(f"<div style='padding-top:8px;font-weight:600;color:#0f172a;'>{s['name']}</div>", unsafe_allow_html=True)
                statuses[s["reg"]] = cols[2].selectbox("", ["Present", "Absent", "OD", "Leave"], key=f"att_{s['reg']}", label_visibility="collapsed")
                cols[3].text_input("", placeholder="OD letter / reason", key=f"rem_{s['reg']}", label_visibility="collapsed")

            st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
            if st.button("💾  Submit Attendance Record", type="primary"):
                present_ct = sum(1 for v in statuses.values() if v == "Present")
                st.success(f"✅ Attendance recorded for {len(sec_students)} students — {present_ct} Present, {len(sec_students)-present_ct} Absent/OD.")

        with tab2:
            f_sec = st.selectbox("Filter Section", ["All"] + [s["id"] for s in SECTIONS], key="short_sec")
            df    = ATT_DF.copy()
            if f_sec != "All":
                df = df[df["Section"] == f_sec]

            total_periods = df.groupby(["Reg No", "Name", "Section", "Dept"])["Status"].count().reset_index(name="Total Periods")
            present_ct    = df[df["Status"].isin(["Present", "OD"])].groupby("Reg No")["Status"].count().reset_index(name="Attended")
            summary       = total_periods.merge(present_ct, on="Reg No", how="left").fillna(0)
            summary["Attendance %"] = (summary["Attended"] / summary["Total Periods"] * 100).round(1)
            summary["Compliance"]   = summary["Attendance %"].apply(lambda x: "⚠️ Shortage" if x < 75 else "✅ Compliant")

            def att_style(val):
                if isinstance(val, float):
                    if val < 75: return "color:#dc2626;font-weight:700"
                    if val < 85: return "color:#d97706;font-weight:600"
                    return "color:#15803d;font-weight:600"
                return ""

            st.dataframe(
                summary[["Reg No", "Name", "Section", "Dept", "Total Periods", "Attended", "Attendance %", "Compliance"]]
                .style.map(att_style, subset=["Attendance %"]),
                use_container_width=True, hide_index=True,
            )

            shortage = summary[summary["Attendance %"] < 75]
            c1, c2, c3 = st.columns(3)
            c1.metric("Students with Shortage (<75%)", len(shortage))
            c2.metric("Overall Average Attendance", f"{summary['Attendance %'].mean():.1f}%")
            c3.metric("High Attendance (>85%)", len(summary[summary["Attendance %"] >= 85]))

        with tab3:
            sel_s = st.selectbox("Select Student Profile", [s["name"] + " · " + s["reg"] for s in STUDENTS])
            reg   = sel_s.split("·")[1].strip()
            s_att = ATT_DF[ATT_DF["Reg No"] == reg].sort_values("Date", ascending=False)

            p  = len(s_att[s_att["Status"].isin(["Present", "OD"])])
            ab = len(s_att[s_att["Status"] == "Absent"])
            od = len(s_att[s_att["Status"] == "OD"])
            lv = len(s_att[s_att["Status"] == "Leave"])
            total = len(s_att)
            pct   = round(p / total * 100, 1) if total else 0

            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Attendance %", f"{pct}%")
            c2.metric("Present", p)
            c3.metric("Absent", ab)
            c4.metric("On Duty (OD)", od)
            c5.metric("Leave", lv)

            if pct < 75:
                st.error("⚠️ Attendance below 75% — student will be detained without formal condonation approval.")
            elif pct < 85:
                st.warning("📌 Attendance below 85% — caution issued.")

            st.dataframe(s_att[["Date", "Period", "Subject", "Status"]].reset_index(drop=True), use_container_width=True, hide_index=True)

    # ═══════════════════════════════════════════════════════════════════════════
    #  PAGE: MARKS
    # ═══════════════════════════════════════════════════════════════════════════
    elif page == "📊  Marks":
        st.markdown('<div class="page-title">Internal Marks &amp; Assessment Management</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Series examinations, lab evaluations, continuous assessment grades, and class statistics</div>', unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["📝  Mark Entry", "📋  Grade Sheet", "📈  Statistical Analysis"])

        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1:
                m_sec  = st.selectbox("Section", [s["id"] for s in SECTIONS], key="m_sec")
                m_subj = st.selectbox("Subject", [s["name"] for s in SUBJECTS if s["dept"] in ["CSE", "All"]], key="m_subj")
            with col2:
                m_exam = st.selectbox("Examination Type", ["Series Test I", "Series Test II", "Model Exam", "End Semester", "Lab Internal", "Assignment"], key="m_exam")
                m_max  = st.number_input("Max Marks", value=30 if "Series" in st.session_state.get("m_exam", "") else 100, step=5, key="m_max")
            with col3:
                m_date = st.date_input("Examination Date", key="m_date")
                m_dept = st.selectbox("Department", DEPARTMENTS, key="m_dept")

            sec_students = [s for s in STUDENTS if s["section"] == m_sec]
            st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
            st.markdown(f'<div class="section-header">Enter Assessment Marks — {m_subj} · {m_exam} · {m_sec}</div>', unsafe_allow_html=True)

            header_cols = st.columns([2, 4, 2, 2, 2])
            for h, c in zip(["Reg No", "Name", f"Score /{m_max}", "Grade", "Status"], header_cols):
                c.markdown(f"<div style='font-size:0.74rem;font-weight:700;color:#64748b;text-transform:uppercase;'>{h}</div>", unsafe_allow_html=True)

            for s in sec_students:
                cols  = st.columns([2, 4, 2, 2, 2])
                cols[0].markdown(f"<div style='padding-top:8px;color:#64748b;font-size:0.84rem;font-family:monospace;'>{s['reg']}</div>", unsafe_allow_html=True)
                cols[1].markdown(f"<div style='padding-top:8px;font-weight:600;color:#0f172a;'>{s['name']}</div>", unsafe_allow_html=True)
                score = cols[2].number_input("", 0, int(m_max), value=random.randint(int(m_max * 0.6), int(m_max)), key=f"mk_{s['reg']}", label_visibility="collapsed")
                pct   = score / m_max * 100
                grade = "O" if pct >= 90 else "A+" if pct >= 85 else "A" if pct >= 75 else "B+" if pct >= 65 else "B" if pct >= 55 else "C"
                result = "Pass" if pct >= 50 else "Fail"
                gmap   = {"O": "badge-green", "A+": "badge-blue", "A": "badge-cyan", "B+": "badge-purple", "B": "badge-amber", "C": "badge-amber"}
                cols[3].markdown(f"<div style='padding-top:8px;'><span class='badge {gmap[grade]}'>{grade}</span></div>", unsafe_allow_html=True)
                cols[4].markdown(f"<div style='padding-top:8px;'><span class='badge {'badge-green' if result=='Pass' else 'badge-red'}'>{result}</span></div>", unsafe_allow_html=True)

            st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
            if st.button("💾  Save Mark Sheet", type="primary"):
                st.success(f"✅ Marks recorded successfully for {len(sec_students)} students.")

        with tab2:
            f_sec  = st.selectbox("Section", ["All"] + [s["id"] for s in SECTIONS], key="gs_sec")
            f_subj = st.selectbox("Subject", ["All"] + [s["name"] for s in SUBJECTS if s["dept"] in ["CSE", "All"]], key="gs_subj")
            f_exam = st.selectbox("Exam", ["All"] + ["Series Test I", "Series Test II", "End Semester"], key="gs_exam")

            df = MARKS_DF.copy()
            if f_sec  != "All": df = df[df["Section"] == f_sec]
            if f_subj != "All": df = df[df["Subject"] == f_subj]
            if f_exam != "All": df = df[df["Exam"] == f_exam]

            df["Percentage"] = (df["Marks"] / df["Max Marks"] * 100).round(1)
            df["Grade"]      = df["Percentage"].apply(lambda x: "O" if x >= 90 else "A+" if x >= 85 else "A" if x >= 75 else "B+" if x >= 65 else "B" if x >= 55 else "C")
            df["Result"]     = df["Percentage"].apply(lambda x: "Pass" if x >= 50 else "Fail")

            def mark_style(val):
                if isinstance(val, float):
                    if val >= 85: return "background-color:#dcfce7;color:#15803d;font-weight:600"
                    if val >= 70: return "background-color:#dbeafe;color:#1d4ed8;font-weight:600"
                    if val >= 55: return "background-color:#fef3c7;color:#b45309;font-weight:600"
                    return "background-color:#fee2e2;color:#b91c1c;font-weight:700"
                return ""

            st.dataframe(
                df[["Reg No", "Name", "Section", "Subject", "Exam", "Marks", "Max Marks", "Percentage", "Grade", "Result"]]
                .style.map(mark_style, subset=["Percentage"]),
                use_container_width=True, hide_index=True,
            )

        with tab3:
            p_subj = st.selectbox("Subject", [s["name"] for s in SUBJECTS if s["dept"] in ["CSE", "All"]], key="perf_subj")
            p_exam = st.selectbox("Exam", ["Series Test I", "Series Test II", "End Semester"], key="perf_exam")
            df_sub = MARKS_DF[(MARKS_DF["Subject"] == p_subj) & (MARKS_DF["Exam"] == p_exam)].copy()
            df_sub["Percentage"] = (df_sub["Marks"] / df_sub["Max Marks"] * 100).round(1)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="section-header">Score Range Distribution</div>', unsafe_allow_html=True)
                hist = pd.cut(df_sub["Percentage"], bins=[0, 50, 60, 70, 80, 90, 100], labels=["<50", "50-60", "60-70", "70-80", "80-90", "90-100"]).value_counts().sort_index()
                st.bar_chart(pd.DataFrame({"Students": hist}), color="#0ea5e9", height=220)
            with col2:
                st.markdown('<div class="section-header">Grade Classification</div>', unsafe_allow_html=True)
                df_sub["Grade"] = df_sub["Percentage"].apply(lambda x: "O" if x >= 90 else "A+" if x >= 85 else "A" if x >= 75 else "B+" if x >= 65 else "B" if x >= 55 else "C")
                grade_counts = df_sub["Grade"].value_counts().reindex(["O", "A+", "A", "B+", "B", "C"], fill_value=0)
                st.bar_chart(pd.DataFrame({"Count": grade_counts}), color="#8b5cf6", height=220)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Class Average", f"{df_sub['Percentage'].mean():.1f}%")
            c2.metric("Top Score", f"{df_sub['Percentage'].max():.1f}%")
            c3.metric("Pass Rate", f"{(df_sub['Percentage'] >= 50).mean() * 100:.1f}%")
            c4.metric("Distinction (O/A+)", str(len(df_sub[df_sub['Percentage'] >= 85])))

    # ═══════════════════════════════════════════════════════════════════════════
    #  PAGE: STUDENT DETAILS
    # ═══════════════════════════════════════════════════════════════════════════
    elif page == "👤  Student Details":
        st.markdown('<div class="page-title">Student Directory &amp; Academic Profiles</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Search by registration number, view cumulative GPA, contact records, and academic files</div>', unsafe_allow_html=True)

        col_s, col_f1, col_f2 = st.columns([3, 1, 1])
        with col_s:  search_q = st.text_input("Search student", placeholder="Name or registration no. (e.g. Bhavana or TVE22CS002)")
        with col_f1: f_dept   = st.selectbox("Department", ["All"] + DEPARTMENTS, key="sd_dept")
        with col_f2: f_batch  = st.selectbox("Batch", ["All"] + BATCHES, key="sd_batch")

        filtered = STUDENTS
        if search_q: filtered = [s for s in filtered if search_q.lower() in s["name"].lower() or search_q.lower() in s["reg"].lower()]
        if f_dept  != "All": filtered = [s for s in filtered if s["dept"] == f_dept]
        if f_batch != "All": filtered = [s for s in filtered if s["batch"] == f_batch]

        st.markdown(f"<div style='font-size:0.84rem;color:#64748b;margin-bottom:1rem;'>Found <strong>{len(filtered)}</strong> matching student profile(s)</div>", unsafe_allow_html=True)

        for s in filtered:
            with st.expander(f"👤 {s['name']}  ·  {s['reg']}  ·  {s['dept']} ({s['sem']})  ·  CGPA: {s['cgpa']}"):
                c1, c2, c3 = st.columns(3)
                for lbl, val in [("Register No.", s["reg"]), ("Full Name", s["name"]), ("Department", s["dept"]), ("Section", s["section"])]:
                    c1.markdown(f"<div class='info-card'><div class='card-label'>{lbl}</div><div class='card-value'>{val}</div></div>", unsafe_allow_html=True)
                for lbl, val in [("Semester", s["sem"]), ("Batch", s["batch"]), ("CGPA", str(s["cgpa"])), ("Date of Birth", s["dob"])]:
                    c2.markdown(f"<div class='info-card'><div class='card-label'>{lbl}</div><div class='card-value'>{val}</div></div>", unsafe_allow_html=True)
                for lbl, val in [("Email", s["email"]), ("Phone", s["phone"]), ("Guardian", s["guardian"]), ("City", s["city"])]:
                    c3.markdown(f"<div class='info-card'><div class='card-label'>{lbl}</div><div class='card-value'>{val}</div></div>", unsafe_allow_html=True)

                s_marks = MARKS_DF[MARKS_DF["Reg No"] == s["reg"]][["Subject", "Exam", "Marks", "Max Marks"]].copy()
                s_marks["Percentage"] = (s_marks["Marks"] / s_marks["Max Marks"] * 100).round(1)
                st.markdown('<div class="section-header" style="margin-top:0.6rem;">Assessment Scores</div>', unsafe_allow_html=True)
                st.dataframe(s_marks.reset_index(drop=True), use_container_width=True, hide_index=True)

    # ═══════════════════════════════════════════════════════════════════════════
    #  PAGE: SECTIONS
    # ═══════════════════════════════════════════════════════════════════════════
    elif page == "🏛  Sections":
        st.markdown('<div class="page-title">Sections &amp; Classroom Allocation</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Manage class sections, assigned faculty advisors, assigned lecture halls, and batch allocations</div>', unsafe_allow_html=True)

        col_stats = st.columns(4)
        col_stats[0].metric("Total Sections", len(SECTIONS))
        col_stats[1].metric("Total Enrolled", sum(s["strength"] for s in SECTIONS))
        col_stats[2].metric("Departments", len(DEPARTMENTS))
        col_stats[3].metric("Active Batches", len(set(s["batch"] for s in SECTIONS)))

        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)

        f_dept_s     = st.radio("Filter Department", ["All"] + DEPARTMENTS, horizontal=True, key="sec_dept_filter")
        display_secs = SECTIONS if f_dept_s == "All" else [s for s in SECTIONS if s["dept"] == f_dept_s]

        for sec in display_secs:
            dept_colors = {"CSE": "badge-blue", "ECE": "badge-purple", "ME": "badge-amber", "CE": "badge-green", "EEE": "badge-cyan"}
            dc = dept_colors.get(sec["dept"], "badge-slate")
            st.markdown(f"""
            <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;padding:1.3rem 1.6rem;margin-bottom:1rem;box-shadow:0 2px 6px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.8rem;">
                    <div>
                        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:4px;">
                            <span style="font-family:'Sora',sans-serif;font-size:1.15rem;font-weight:700;color:#0f172a;">
                                Section {sec['id']}
                            </span>
                            <span class="badge {dc}">{sec['dept']}</span>
                            <span class="badge badge-slate">{sec['semester']}</span>
                        </div>
                        <div style="font-size:0.84rem;color:#64748b;">
                            Advisor: <strong>{sec['advisor']}</strong> &nbsp;·&nbsp; Hall / Room: <strong>{sec['room']}</strong> &nbsp;·&nbsp; Batch: {sec['batch']}
                        </div>
                    </div>
                    <div style="display:flex;gap:0.6rem;align-items:center;flex-wrap:wrap;">
                        <span class="badge badge-blue">🎓 {sec['strength']} students</span>
                        <span class="badge badge-green">✅ Active</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"View student roster — Section {sec['id']}"):
                sec_studs = [s for s in STUDENTS if s["section"] == sec["id"]]
                if sec_studs:
                    df = pd.DataFrame([{"Reg No": s["reg"], "Name": s["name"], "Gender": s["gender"], "CGPA": s["cgpa"], "Email": s["email"]} for s in sec_studs])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No active students linked to this section.")

        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Add New Section Allocation</div>', unsafe_allow_html=True)
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)
            ns_id      = col1.text_input("Section ID", placeholder="e.g. CSE-C")
            ns_dept    = col2.selectbox("Department", DEPARTMENTS, key="ns_dept")
            ns_sem     = col3.selectbox("Semester", ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"], key="ns_sem")
            ns_batch   = col4.text_input("Batch", placeholder="e.g. 2024-28")
            ns_advisor = col1.text_input("Section Advisor", placeholder="Advisor Full Name")
            ns_room    = col2.text_input("Room / Lab No", placeholder="e.g. CS-402")
            if st.button("➕  Create Section", type="primary"):
                if ns_id and ns_advisor and ns_room:
                    st.success(f"✅ Section '{ns_id}' ({ns_dept} · {ns_sem}) created. Advisor: {ns_advisor} · Room: {ns_room}")
                else:
                    st.error("Please provide Section ID, Advisor Name, and Room Number.")

    # ═══════════════════════════════════════════════════════════════════════════
    #  PAGE: COURSES
    # ═══════════════════════════════════════════════════════════════════════════
    elif page == "📚  Courses":
        st.markdown('<div class="page-title">Courses, Curriculum &amp; Faculty Mapping</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Departmental syllabus catalog, credit allocations, and faculty in-charge directory</div>', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📋  Course Catalogue", "➕  Register New Course"])

        with tab1:
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1: f_dept_c = st.selectbox("Filter Department", ["All"] + DEPARTMENTS + ["All Depts"], key="c_dept")
            with col_f2: f_type_c = st.radio("Course Type", ["All", "Theory", "Lab"], horizontal=True, key="c_type")
            with col_f3: f_sem_c  = st.selectbox("Filter Semester", ["All", "S2", "S4", "S6"], key="c_sem")

            disp = SUBJECTS
            if f_dept_c not in ["All", "All Depts"]: disp = [c for c in disp if c["dept"] == f_dept_c]
            if f_type_c != "All":                    disp = [c for c in disp if c["type"] == f_type_c]
            if f_sem_c  != "All":                    disp = [c for c in disp if c["sem"]  == f_sem_c]

            for course in disp:
                type_badge = "badge-blue" if course["type"] == "Theory" else "badge-purple"
                dept_badge = {"CSE": "badge-blue", "ECE": "badge-purple", "ME": "badge-amber", "CE": "badge-green", "EEE": "badge-cyan", "All": "badge-slate"}.get(course["dept"], "badge-slate")
                st.markdown(f"""
                <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;padding:1.2rem 1.6rem;margin-bottom:0.8rem;box-shadow:0 2px 6px rgba(0,0,0,0.02);">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.7rem;">
                        <div>
                            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:4px;flex-wrap:wrap;">
                                <span style="font-family:'Sora',sans-serif;font-size:1.05rem;font-weight:700;color:#0f172a;">{course['name']}</span>
                                <span class="badge {type_badge}">{course['type']}</span>
                                <span class="badge {dept_badge}">{course['dept']}</span>
                                <span class="badge badge-slate">{course['sem']}</span>
                            </div>
                            <div style="font-size:0.82rem;color:#64748b;">
                                Code: <strong>{course['code']}</strong> &nbsp;·&nbsp;
                                Faculty: <strong>{course['faculty']}</strong> &nbsp;·&nbsp;
                                Credits: <strong>{course['credits']}</strong>
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-family:'Sora',sans-serif;font-size:1.45rem;font-weight:700;color:#2563eb;">{course['enrolled']}</div>
                            <div style="font-size:0.74rem;color:#94a3b8;">enrolled</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="section-header" style="margin-top: 1.2rem;">Credit Structure Summary</div>', unsafe_allow_html=True)
            credit_df = pd.DataFrame(disp)[["code", "name", "dept", "sem", "credits", "type", "enrolled"]] if disp else pd.DataFrame()
            if not credit_df.empty:
                st.dataframe(credit_df.rename(columns={"code": "Code", "name": "Course", "dept": "Dept", "sem": "Sem", "credits": "Credits", "type": "Type", "enrolled": "Enrolled"}), use_container_width=True, hide_index=True)

        with tab2:
            st.markdown('<div class="section-header">Register New Course to Curriculum</div>', unsafe_allow_html=True)
            with st.container(border=True):
                cc1, cc2, cc3 = st.columns(3)
                nc_code   = cc1.text_input("Course Code", placeholder="e.g. CS401")
                nc_name   = cc2.text_input("Course Name", placeholder="e.g. Machine Learning & Neural Networks")
                nc_dept   = cc3.selectbox("Department", DEPARTMENTS + ["All"], key="nc_dept")
                nc_sem    = cc1.selectbox("Semester", ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"], key="nc_sem")
                nc_cred   = cc2.number_input("Credits", min_value=1, max_value=6, value=3, key="nc_cred")
                nc_type   = cc3.radio("Type", ["Theory", "Lab"], horizontal=True, key="nc_type")
                nc_fac    = cc1.text_input("Faculty In-Charge", placeholder="e.g. Dr. Priya Varma")
                if st.button("➕  Add Course to System", type="primary"):
                    if nc_code and nc_name and nc_fac:
                        st.success(f"✅ Course '{nc_name}' ({nc_code}) added. Faculty: {nc_fac} · Credits: {nc_cred}")
                    else:
                        st.error("Please fill in course code, name, and faculty in-charge.")