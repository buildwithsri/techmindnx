import streamlit as st
import pandas as pd
import random

# ─── Static Data (module-level) ─────────────────────────────────────────────

ATTENDANCE = {
    "CS301 - Data Structures": 90,
    "CS302 - Operating Systems": 78,
    "CS303 - DBMS": 65,
    "CS304 - Computer Networks": 82,
    "CS305 - DSA Lab": 88,
}

MARKS = [
    {"subject": "CS301 - Data Structures", "series_1": 28, "series_2": 26, "assignment": 9, "total": 63},
    {"subject": "CS302 - Operating Systems", "series_1": 22, "series_2": 24, "assignment": 8, "total": 54},
    {"subject": "CS303 - DBMS", "series_1": 25, "series_2": 27, "assignment": 10, "total": 62},
    {"subject": "CS304 - Computer Networks", "series_1": 20, "series_2": 23, "assignment": 7, "total": 50},
    {"subject": "CS305 - DSA Lab", "series_1": 38, "series_2": 40, "assignment": 15, "total": 93},
]

EVENTS = [
    {"name": "National Hackathon 2026",     "date": "2026-10-05", "type": "Technical", "status": "Registered",    "team": "CodeStorm"},
    {"name": "Inter-College Debate",         "date": "2026-09-20", "type": "Cultural",  "status": "Shortlisted",   "team": "Solo"},
    {"name": "IEEE Paper Presentation",      "date": "2026-10-15", "type": "Research",  "status": "Submitted",     "team": "CodeStorm"},
    {"name": "TechFest 2026 — Tech Quiz",    "date": "2026-11-01", "type": "Technical", "status": "Registered",    "team": "Solo"},
    {"name": "Cultural Night — Street Play", "date": "2026-09-25", "type": "Cultural",  "status": "Participating", "team": "Drama Club"},
]

FEES = [
    {"semester": "S1 (2022-23)", "amount": 45000, "status": "Paid",    "date": "2022-08-10", "mode": "Online — UPI",   "receipt": "TVE-R-2201"},
    {"semester": "S2 (2022-23)", "amount": 42000, "status": "Paid",    "date": "2023-01-05", "mode": "Online — NEFT",  "receipt": "TVE-R-2302"},
    {"semester": "S3 (2023-24)", "amount": 45000, "status": "Paid",    "date": "2023-07-22", "mode": "Cash — Counter", "receipt": "TVE-R-2403"},
    {"semester": "S4 (2023-24)", "amount": 43000, "status": "Paid",    "date": "2024-01-10", "mode": "Online — UPI",   "receipt": "TVE-R-2504"},
    {"semester": "S5 (2024-25)", "amount": 47000, "status": "Paid",    "date": "2024-07-15", "mode": "DD — Bank",      "receipt": "TVE-R-2605"},
    {"semester": "S6 (2025-26)", "amount": 47000, "status": "Pending", "date": "—",           "mode": "—",             "receipt": "—"},
]

PROFILE = {
    "department":       "Computer Science & Engineering",
    "section":          "CSE-A",
    "semester":         "6",
    "academic_year":    "2022-26",
    "hostel":           "Not Applicable",
    "bus_route":        "Route 7 — Kakkanad - TVC campus",
    "advisor":          "Dr. Arjun Nair",
    "mentor":           "Prof. Meera Pillai",
    "scholarship":      "Merit Scholarship (AICTE)",
    "blood_group":      "B+",
    "address":          "12 Skyline Apartments, Kakkanad, Kochi - 682030",
    "guardian":         "Rajan Sharma",
    "guardian_phone":   "+91 94460 87654",
    "hometown":         "Kochi, Kerala",
}


# ─── RENDER — called from app.py ────────────────────────────────────────────

def render(page: str):
    """Render the student portal page inside the connected TechVerse app."""

    # ── CSS ───────────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .student-hero {
        background: linear-gradient(135deg, #065f46 0%, #047857 50%, #059669 100%);
        border-radius: 16px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        color: white;
        box-shadow: 0 10px 25px -5px rgba(5, 150, 105, 0.25);
    }
    .student-avatar {
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
    .student-name {
        font-family: 'Sora', sans-serif;
        font-size: 1.45rem;
        font-weight: 700;
        letter-spacing: -0.01em;
    }
    .student-meta {
        font-size: 0.86rem;
        color: rgba(255,255,255,0.85);
        margin-top: 3px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Personalised Student Hero Card ─────────────────────────────────────────
    user_info    = st.session_state.get("user_info", {})
    display_name = user_info.get("display_name", "Student")
    initials     = user_info.get("initials", "ST")
    reg_no       = user_info.get("reg", "TVE22CS001")
    dept         = user_info.get("dept", "Computer Science & Engineering")
    sem          = user_info.get("sem", "6")
    username     = st.session_state.get("username", "student")

    st.markdown(f"""
    <div class="student-hero">
        <div class="student-avatar">{initials}</div>
        <div>
            <div class="student-name">{display_name}</div>
            <div class="student-meta">
                <strong>{reg_no}</strong> &nbsp;·&nbsp; {dept} &nbsp;·&nbsp; Semester {sem}
            </div>
            <div class="student-meta" style="margin-top: 8px;">
                <span style="background: rgba(255,255,255,0.2); border-radius: 99px;
                             padding: 2px 12px; font-size: 0.72rem; font-weight: 600;">✅ Active Enrolled</span>
                &nbsp;&nbsp; Batch 2022–2026 &nbsp;·&nbsp; Even Semester 2025–26
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    #  PAGE: DASHBOARD
    # ═══════════════════════════════════════════════════════════════════════════
    if page == "🏠 Dashboard":
        st.markdown('<div class="page-title">Student Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Your real-time academic snapshot and semester performance — Even Semester 2025-26</div>', unsafe_allow_html=True)

        avg_att  = round(sum(ATTENDANCE.values()) / len(ATTENDANCE))
        avg_mark = round(sum(m["total"] for m in MARKS) / len(MARKS))
        paid     = sum(f["amount"] for f in FEES if f["status"] == "Paid")
        pending  = sum(f["amount"] for f in FEES if f["status"] == "Pending")

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.1rem;margin-bottom:2rem;">
            <div class="stat-card">
                <div class="accent-bar" style="background:#10b981;"></div>
                <div class="label">Avg Attendance</div>
                <div class="value">{avg_att}%</div>
                <div class="delta">{'✅ Good standing' if avg_att >= 75 else '⚠️ Shortage alert'}</div>
            </div>
            <div class="stat-card">
                <div class="accent-bar" style="background:#0ea5e9;"></div>
                <div class="label">Internal Avg Score</div>
                <div class="value">{avg_mark}</div>
                <div class="delta">Out of 100 max</div>
            </div>
            <div class="stat-card">
                <div class="accent-bar" style="background:#22c55e;"></div>
                <div class="label">Fees Paid</div>
                <div class="value">₹{paid//1000}K</div>
                <div class="delta">₹{pending//1000}K pending</div>
            </div>
            <div class="stat-card">
                <div class="accent-bar" style="background:#8b5cf6;"></div>
                <div class="label">Events Registered</div>
                <div class="value">{len(EVENTS)}</div>
                <div class="delta">Across {len(set(e['type'] for e in EVENTS))} tracks</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown('<div class="section-header">Attendance by Subject</div>', unsafe_allow_html=True)
            att_df = pd.DataFrame({"Subject": list(ATTENDANCE.keys()), "Attendance %": list(ATTENDANCE.values())})

            def att_color(val):
                if val < 75: return "background-color:#fee2e2;color:#b91c1c;font-weight:700"
                if val < 85: return "background-color:#fef3c7;color:#b45309"
                return "background-color:#dcfce7;color:#15803d;font-weight:600"

            st.dataframe(
                att_df.style.map(att_color, subset=["Attendance %"]),
                use_container_width=True, hide_index=True,
            )

            st.markdown('<div class="section-header" style="margin-top: 1.5rem;">Upcoming Events</div>', unsafe_allow_html=True)
            for ev in EVENTS[:3]:
                type_badge = "badge-blue" if ev["type"] == "Technical" else "badge-purple" if ev["type"] == "Cultural" else "badge-green"
                st.markdown(f"""
                <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;
                            padding:0.9rem 1.3rem;margin-bottom:0.6rem;box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-weight:600;color:#0f172a;font-size:0.92rem;">{ev['name']}</div>
                            <div style="font-size:0.78rem;color:#64748b;margin-top:2px;">
                                📅 {ev['date']} &nbsp;·&nbsp; {ev['team']}
                            </div>
                        </div>
                        <span class="badge {type_badge}">{ev['type']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="section-header">Internal Marks Summary</div>', unsafe_allow_html=True)
            marks_df = pd.DataFrame(MARKS)[["subject", "series_1", "series_2", "assignment", "total"]]
            marks_df.columns = ["Subject", "Series I /30", "Series II /30", "Assignment /10", "Total /100"]
            st.dataframe(marks_df, use_container_width=True, hide_index=True)

            st.markdown('<div class="section-header" style="margin-top: 1.5rem;">Recent Fee Invoices</div>', unsafe_allow_html=True)
            for f in FEES[-2:]:
                fc = "badge-green" if f["status"] == "Paid" else "badge-red"
                st.markdown(f"""
                <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;
                            padding:0.9rem 1.3rem;display:flex;justify-content:space-between;
                            align-items:center;margin-bottom:0.6rem;box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                    <div>
                        <div style="font-weight:600;color:#0f172a;font-size:0.92rem;">{f['semester']}</div>
                        <div style="font-size:0.78rem;color:#64748b;margin-top:1px;">Amount: <strong>₹{f['amount']:,}</strong></div>
                    </div>
                    <span class="badge {fc}">{f['status']}</span>
                </div>
                """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    #  PAGE: ATTENDANCE
    # ═══════════════════════════════════════════════════════════════════════════
    elif page == "📅 Attendance":
        st.markdown('<div class="page-title">My Attendance Records</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Subject-wise attendance breakdown, compliance tracking, and shortage warnings</div>', unsafe_allow_html=True)

        overall_avg = round(sum(ATTENDANCE.values()) / len(ATTENDANCE))
        low_ct      = sum(1 for v in ATTENDANCE.values() if v < 75)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Overall Average", f"{overall_avg}%")
        c2.metric("Subjects Below 75%", str(low_ct))
        c3.metric("Highest Subject", max(ATTENDANCE, key=ATTENDANCE.get).split(" - ")[0])
        c4.metric("Needs Attendance", min(ATTENDANCE, key=ATTENDANCE.get).split(" - ")[0])

        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Subject Attendance Chart</div>', unsafe_allow_html=True)

        st.bar_chart(
            pd.DataFrame({"Attendance %": ATTENDANCE}),
            color="#10b981", height=250,
        )

        st.markdown('<div class="section-header" style="margin-top: 1.5rem;">Subject-wise Analysis & Compliance</div>', unsafe_allow_html=True)

        for subj, pct in ATTENDANCE.items():
            conducted = random.randint(40, 60)
            attended  = round(conducted * pct / 100)
            if pct < 75:
                needed = max(0, round((0.75 * conducted - attended) / (1 - 0.75)))
                alert  = f"⚠️ Need to attend {needed} more consecutive classes to achieve 75%"
                badge  = "badge-red"
                bar_c  = "#dc2626"
            elif pct < 85:
                badge = "badge-amber"
                alert = "📌 Attendance is acceptable, maintain above 85% for distinction"
                bar_c = "#d97706"
            else:
                badge = "badge-green"
                alert = "✅ Excellent attendance record"
                bar_c = "#10b981"

            st.markdown(f"""
            <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;
                        padding:1.2rem 1.6rem;margin-bottom:0.8rem;box-shadow:0 2px 6px rgba(0,0,0,0.03);">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">
                    <div>
                        <div style="font-weight:700;color:#0f172a;font-size:0.98rem;">{subj}</div>
                        <div style="font-size:0.8rem;color:#64748b;margin-top:3px;">
                            <strong>{attended}/{conducted}</strong> classes attended &nbsp;·&nbsp; {alert}
                        </div>
                    </div>
                    <div style="display:flex;align-items:center;gap:0.9rem;">
                        <div style="font-family:'Sora',sans-serif;font-size:1.6rem;font-weight:700;
                                    color:{bar_c};">
                            {pct}%
                        </div>
                        <span class="badge {badge}">{'Shortage' if pct < 75 else 'Caution' if pct < 85 else 'Good'}</span>
                    </div>
                </div>
                <div style="background:#f1f5f9;border-radius:99px;height:6px;margin-top:0.8rem;overflow:hidden;">
                    <div style="background:{bar_c};width:{pct}%;height:100%;border-radius:99px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    #  PAGE: EXAM MARKS
    # ═══════════════════════════════════════════════════════════════════════════
    elif page == "📝 Exam Marks":
        st.markdown('<div class="page-title">Exam Marks &amp; Academic Scores</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Continuous internal assessments, assignments, series tests, and performance grades</div>', unsafe_allow_html=True)

        avg_t = round(sum(m["total"] for m in MARKS) / len(MARKS))
        best  = max(MARKS, key=lambda x: x["total"])
        low   = min(MARKS, key=lambda x: x["total"])

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Average Score", f"{avg_t}/100")
        c2.metric("Top Performed", best["subject"].split(" - ")[1])
        c3.metric("Focus Area", low["subject"].split(" - ")[1])
        c4.metric("Subjects Evaluated", str(len(MARKS)))

        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Internal Assessment Scores</div>', unsafe_allow_html=True)

        for m in MARKS:
            pct   = m["total"]
            grade = "O" if pct >= 90 else "A+" if pct >= 85 else "A" if pct >= 75 else "B+" if pct >= 65 else "B" if pct >= 55 else "C"
            gmap  = {
                "O": ("badge-green", "#15803d"),
                "A+": ("badge-blue", "#2563eb"),
                "A": ("badge-cyan", "#0891b2"),
                "B+": ("badge-purple", "#7c3aed"),
                "B": ("badge-amber", "#d97706"),
                "C": ("badge-amber", "#d97706")
            }
            gc, gcolor = gmap[grade]

            st.markdown(f"""
            <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;
                        padding:1.2rem 1.6rem;margin-bottom:0.8rem;box-shadow:0 2px 6px rgba(0,0,0,0.03);">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.7rem;">
                    <div>
                        <div style="font-weight:700;color:#0f172a;font-size:0.98rem;">{m['subject']}</div>
                        <div style="font-size:0.82rem;color:#64748b;margin-top:4px;">
                            Series&nbsp;I: <b>{m['series_1']}/30</b> &nbsp;|&nbsp;
                            Series&nbsp;II: <b>{m['series_2']}/30</b> &nbsp;|&nbsp;
                            Assignment: <b>{m['assignment']}/10</b> &nbsp;|&nbsp;
                            Continuous Eval: <b>30/30</b>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-family:'Sora',sans-serif;font-size:1.8rem;font-weight:700;color:{gcolor};">{m['total']}</div>
                        <div style="font-size:0.74rem;color:#94a3b8;">out of 100 &nbsp;<span class="badge {gc}">Grade {grade}</span></div>
                    </div>
                </div>
                <div style="background:#f1f5f9;border-radius:99px;height:5px;margin-top:0.8rem;overflow:hidden;">
                    <div style="background:{gcolor};width:{m['total']}%;height:100%;border-radius:99px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top: 1.5rem;">Component Score Comparison</div>', unsafe_allow_html=True)
        comp_df = pd.DataFrame(MARKS)[["subject", "series_1", "series_2", "assignment"]].copy()
        comp_df.columns = ["Subject", "Series I", "Series II", "Assignment"]
        comp_df["Subject"] = comp_df["Subject"].apply(lambda x: x.split(" - ")[1])
        st.bar_chart(comp_df.set_index("Subject"), height=230)

    # ═══════════════════════════════════════════════════════════════════════════
    #  PAGE: PROFILE
    # ═══════════════════════════════════════════════════════════════════════════
    elif page == "👤 Profile":
        st.markdown('<div class="page-title">Student Profile &amp; Records</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Personal, academic and contact credentials officially registered with the University</div>', unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["🎓  Academic Info", "📋  Personal Details", "🛡️  Update Contact"])

        with tab1:
            c1, c2, c3 = st.columns(3)
            academic_fields = [
                ("Register No.",      reg_no),
                ("Full Name",         display_name),
                ("Department",        PROFILE["department"]),
                ("Section",           PROFILE["section"]),
                ("Semester",          PROFILE["semester"]),
                ("Academic Year",     PROFILE["academic_year"]),
                ("Faculty Advisor",   PROFILE["advisor"]),
                ("Mentor",            PROFILE["mentor"]),
                ("Scholarship",       PROFILE["scholarship"]),
            ]
            for i, (lbl, val) in enumerate(academic_fields):
                col = [c1, c2, c3][i % 3]
                col.markdown(f"<div class='info-card'><div class='card-label'>{lbl}</div><div class='card-value'>{val}</div></div>", unsafe_allow_html=True)

        with tab2:
            c1, c2, c3 = st.columns(3)
            personal_fields = [
                ("Email",             f"{username}@tve.edu"),
                ("Blood Group",       PROFILE["blood_group"]),
                ("Hostel",            PROFILE["hostel"]),
                ("Bus Route",         PROFILE["bus_route"]),
                ("Address",           PROFILE["address"]),
                ("Guardian",          PROFILE["guardian"]),
                ("Guardian Phone",    PROFILE["guardian_phone"]),
                ("Hometown",          PROFILE["hometown"]),
            ]
            for i, (lbl, val) in enumerate(personal_fields):
                col = [c1, c2, c3][i % 3]
                col.markdown(f"<div class='info-card'><div class='card-label'>{lbl}</div><div class='card-value'>{val}</div></div>", unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="section-header">Update Contact Details</div>', unsafe_allow_html=True)
            st.info("ℹ️ Contact updates are verified against OTP. Academic records must be amended by the academic cell.")
            u1, u2 = st.columns(2)
            new_phone   = u1.text_input("Mobile Number",  value="+91 98765 43210")
            new_email   = u2.text_input("Personal Email", value=f"{username}@gmail.com")
            new_address = st.text_area("Address",         value=PROFILE["address"])
            if st.button("💾  Save Changes", type="primary"):
                st.success("✅ Contact information updated and logged to audit trail.")

    # ═══════════════════════════════════════════════════════════════════════════
    #  PAGE: EVENT REGISTRATION
    # ═══════════════════════════════════════════════════════════════════════════
    elif page == "🎫 Event Registration":
        st.markdown('<div class="page-title">Campus Events &amp; Hackathons</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Register and track participations in technical, cultural and research summits</div>', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📋  My Registrations", "🆕  Register for New Event"])

        with tab1:
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Registered", str(len(EVENTS)))
            c2.metric("Technical Tracks",  str(sum(1 for e in EVENTS if e["type"] == "Technical")))
            c3.metric("Cultural / Other",  str(sum(1 for e in EVENTS if e["type"] != "Technical")))

            st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)

            for ev in EVENTS:
                type_colors = {
                    "Technical": ("badge-blue",   "#2563eb"),
                    "Cultural":  ("badge-purple",  "#7c3aed"),
                    "Research":  ("badge-green",   "#16a34a"),
                }
                tc, _ = type_colors.get(ev["type"], ("badge-slate", "#475569"))
                status_badge = {
                    "Registered":    "badge-blue",
                    "Shortlisted":   "badge-green",
                    "Submitted":     "badge-cyan",
                    "Participating": "badge-purple",
                }.get(ev["status"], "badge-slate")

                st.markdown(f"""
                <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;
                            padding:1.2rem 1.6rem;margin-bottom:0.8rem;box-shadow:0 2px 6px rgba(0,0,0,0.03);">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.6rem;">
                        <div>
                            <div style="font-weight:700;color:#0f172a;font-size:0.98rem;">{ev['name']}</div>
                            <div style="font-size:0.8rem;color:#64748b;margin-top:3px;">
                                📅 {ev['date']} &nbsp;·&nbsp; Team: <strong>{ev['team']}</strong>
                            </div>
                        </div>
                        <div style="display:flex;gap:0.5rem;align-items:center;">
                            <span class="badge {tc}">{ev['type']}</span>
                            <span class="badge {status_badge}">{ev['status']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="section-header">New Event Registration Form</div>', unsafe_allow_html=True)
            with st.form("new_event_form"):
                ef1, ef2 = st.columns(2)
                ev_name  = ef1.text_input("Event Name *", placeholder="e.g. National Smart India Hackathon")
                ev_type  = ef2.selectbox("Event Category", ["Technical", "Cultural", "Research", "Sports", "NSS/NCC"])
                ev_date  = ef1.date_input("Event Date")
                ev_org   = ef2.text_input("Organising Body / Host", placeholder="e.g. IIT Bombay / IEEE")
                ev_team  = ef1.text_input("Team Name / Solo", placeholder="e.g. CodeStorm")
                ev_note  = st.text_area("Event Description / Remarks", placeholder="Any special requirements or team members list", height=90)
                if st.form_submit_button("📤  Submit Registration", use_container_width=True, type="primary"):
                    if ev_name and ev_org:
                        st.success(f"✅ Registration submitted for **{ev_name}** on {ev_date}. Faculty approval workflow initiated.")
                    else:
                        st.error("Please enter the event name and organising body.")

    # ═══════════════════════════════════════════════════════════════════════════
    #  PAGE: FEE PAYMENTS
    # ═══════════════════════════════════════════════════════════════════════════
    elif page == "💳 Fee Payments":
        st.markdown('<div class="page-title">Tuition &amp; Semester Fee Payments</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Financial history, verified digital receipts, and online payment portal</div>', unsafe_allow_html=True)

        total   = sum(f["amount"] for f in FEES)
        paid    = sum(f["amount"] for f in FEES if f["status"] == "Paid")
        pending = total - paid

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Program Fees", f"₹{total:,}")
        c2.metric("Total Paid",         f"₹{paid:,}")
        c3.metric("Outstanding Due",    f"₹{pending:,}", delta_color="inverse")
        c4.metric("Semesters Cleared",  f"{sum(1 for f in FEES if f['status'] == 'Paid')} / {len(FEES)}")

        if pending > 0:
            st.warning(f"🔔 You have an active balance of **₹{pending:,}** for the current semester. Clear dues before exam hall ticket generation.")

        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Fee Payment Ledger</div>', unsafe_allow_html=True)

        for f in FEES:
            fc = "badge-green" if f["status"] == "Paid" else "badge-red"
            bg = "#ffffff"
            brd = "#bbf7d0" if f["status"] == "Paid" else "#fecaca"
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {brd};border-radius:14px;
                        padding:1.2rem 1.6rem;margin-bottom:0.8rem;box-shadow:0 2px 6px rgba(0,0,0,0.02);">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.7rem;">
                    <div>
                        <div style="font-weight:700;color:#0f172a;font-size:0.98rem;">{f['semester']}</div>
                        <div style="font-size:0.8rem;color:#64748b;margin-top:3px;">
                            Payment Mode: <strong>{f['mode']}</strong> &nbsp;·&nbsp; Receipt ID: <code>{f['receipt']}</code> &nbsp;·&nbsp; Date: {f['date']}
                        </div>
                    </div>
                    <div style="display:flex;align-items:center;gap:1rem;">
                        <div style="font-family:'Sora',sans-serif;font-size:1.55rem;font-weight:700;color:#0f172a;">
                            ₹{f['amount']:,}
                        </div>
                        <span class="badge {fc}">{f['status']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if pending > 0:
            st.markdown('<div class="section-header" style="margin-top: 1.5rem;">Online Fee Gateway</div>', unsafe_allow_html=True)
            with st.container(border=True):
                pm1, pm2 = st.columns(2)
                pay_mode    = pm1.radio("Select Payment Mode", ["UPI / QR Code", "Net Banking", "Debit/Credit Card", "Bank Challan"], horizontal=True)
                pay_amount  = pm2.number_input("Amount Payable (₹)", value=pending, step=1000)
                pay_ref     = pm1.text_input("Transaction / UTR Reference ID", placeholder="e.g. UPI-2026-981247")
                pay_remark  = pm2.text_input("Remarks / Notes (Optional)", placeholder="Semester 6 tuition payment")
                if st.button("💳  Submit Payment Confirmation", type="primary", use_container_width=True):
                    if pay_ref:
                        st.success(f"✅ Payment submission for **₹{pay_amount:,}** recorded. Transaction Reference: `{pay_ref}`. Verification receipt will be issued in 24 hours.")
                    else:
                        st.error("Please enter a valid Transaction / UTR Reference ID.")