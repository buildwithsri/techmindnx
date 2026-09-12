import streamlit as st
import pandas as pd
import re
from datetime import datetime

# =========================================================
# IN-MEMORY DATA (session state — no SQLite, no disk I/O)
# =========================================================

def _init_form_state():
    if "registered_students" not in st.session_state:
        st.session_state.registered_students = [
            {
                "Student ID":        "FIT26DL100",
                "Name":              "Roshni Menon",
                "Phone":             "+91 98765 43210",
                "Email":             "roshni@tve.edu",
                "Department":        "Computer Science & Engineering",
                "Emergency Contact": "+91 91234 56789",
                "Address":           "12 MG Road, Kochi, Kerala",
                "Registered At":     "2026-09-01 09:00:00",
            },
            {
                "Student ID":        "FIT26DL101",
                "Name":              "Arjun Das",
                "Phone":             "+91 99887 76655",
                "Email":             "arjun@tve.edu",
                "Department":        "Artificial Intelligence & Data Science",
                "Emergency Contact": "+91 98001 12345",
                "Address":           "34 NH47, Thrissur, Kerala",
                "Registered At":     "2026-09-02 10:30:00",
            },
        ]
    if "next_form_id" not in st.session_state:
        st.session_state.next_form_id = 102


def _generate_student_id() -> str:
    sid = f"FIT26DL{st.session_state.next_form_id}"
    st.session_state.next_form_id += 1
    return sid


# =========================================================
# RENDER — called from app.py
# =========================================================

def render():
    """Render the student registration form (in-memory, pandas/CSV)."""

    _init_form_state()

    # ── Tabs: Register | View All ─────────────────────────────────────────────
    tab_register, tab_view = st.tabs(["➕  Register New Student", "📋  View All Registrations"])

    # ═══════════════════════════════════════════════════════
    #  TAB 1 — Registration form
    # ═══════════════════════════════════════════════════════
    with tab_register:
        st.markdown('<div class="page-title">Student Registration Portal</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="page-subtitle">Onboard and enroll new campus students with institutional credentials and department allotment</div>',
            unsafe_allow_html=True,
        )

        preview_id = f"FIT26DL{st.session_state.next_form_id}"
        st.markdown(f"""
        <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px;
                    padding: 0.9rem 1.4rem; color: #1d4ed8; font-weight: 700; font-size: 1.1rem;
                    display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem;">
            <span>🎓 Generated Next Registration ID:</span>
            <span style="font-family: monospace; font-size: 1.25rem; background: #ffffff; padding: 3px 12px; border-radius: 8px; border: 1px solid #bfdbfe;">
                {preview_id}
            </span>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            with st.form("student_registration_form", clear_on_submit=True):
                st.markdown('<div class="section-header">1. Personal & Contact Information</div>', unsafe_allow_html=True)

                col1, col2 = st.columns(2)

                with col1:
                    name = st.text_input("Full Legal Name *", placeholder="Firstname Lastname")
                    phone = st.text_input("Primary Contact Phone *", placeholder="+91 98765 43210")
                    email = st.text_input("Official / Personal Email *", placeholder="student@tve.edu")

                with col2:
                    department = st.selectbox(
                        "Allotted Department *",
                        [
                            "Computer Science & Engineering",
                            "Artificial Intelligence & Data Science",
                            "Information Technology",
                            "Electronics & Communication Engineering",
                            "Electrical & Electronics Engineering",
                            "Mechanical Engineering",
                            "Civil Engineering",
                            "Other",
                        ],
                    )
                    emergency_contact = st.text_input(
                        "Emergency Guardian Phone *", placeholder="+91 98765 00000"
                    )

                address = st.text_area(
                    "Permanent Residential Address *",
                    placeholder="Street, City, District, State, Postal PIN",
                    height=85,
                )

                st.markdown('<div class="section-header" style="margin-top: 1rem;">2. Identification Photo (Optional)</div>', unsafe_allow_html=True)
                photo = st.file_uploader(
                    "Upload Student Passport Photograph",
                    type=["jpg", "jpeg", "png"],
                    help="Upload a standard passport JPG/PNG photo.",
                )

                st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button(
                    "➕  Submit & Complete Student Enrollment",
                    use_container_width=True,
                    type="primary",
                )

        # ── Validation & in-memory save ───────────────────────────────────────
        if submitted:
            errors = []

            if not name.strip():
                errors.append("Please provide the student's legal name.")
            if not phone.strip():
                errors.append("Please provide a contact phone number.")
            elif not re.fullmatch(r"[0-9+\-\s()]{7,20}", phone):
                errors.append("Please enter a valid phone number format.")
            if not email.strip():
                errors.append("Please provide an email address.")
            elif not re.fullmatch(
                r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email
            ):
                errors.append("Please enter a valid email address.")
            if not address.strip():
                errors.append("Please provide the permanent address.")
            if not emergency_contact.strip():
                errors.append("Please provide the emergency contact number.")

            if errors:
                for err in errors:
                    st.error(f"❌ {err}")
            else:
                student_id = _generate_student_id()

                record = {
                    "Student ID":        student_id,
                    "Name":              name.strip(),
                    "Phone":             phone.strip(),
                    "Email":             email.strip(),
                    "Department":        department,
                    "Emergency Contact": emergency_contact.strip(),
                    "Address":           address.strip(),
                    "Registered At":     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                st.session_state.registered_students.append(record)

                st.success(f"🎉 Student enrolled successfully! Assigned Student ID: **{student_id}**")

                # Confirmation Card
                with st.container(border=True):
                    st.markdown('<div class="section-header">Registration Confirmation Card</div>', unsafe_allow_html=True)
                    d1, d2 = st.columns([1, 2.5])
                    with d1:
                        if photo:
                            st.image(photo, caption=name.strip(), width=160)
                        else:
                            st.markdown("""
                            <div style='width:130px;height:130px;border-radius:14px;
                                        background:#eff6ff;border:1px solid #bfdbfe;
                                        display:flex;align-items:center;justify-content:center;
                                        font-size:2.8rem;'>
                                🧑‍🎓
                            </div>
                            """, unsafe_allow_html=True)
                    with d2:
                        st.markdown(f"""
                        <div style='font-size:0.92rem;line-height:1.8;'>
                            <div><strong>Student ID:</strong> <span style='font-family:monospace;color:#2563eb;font-weight:700;'>{student_id}</span></div>
                            <div><strong>Full Name:</strong> {name.strip()}</div>
                            <div><strong>Department:</strong> {department}</div>
                            <div><strong>Email:</strong> {email.strip()}</div>
                            <div><strong>Phone:</strong> {phone.strip()}</div>
                        </div>
                        """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════
    #  TAB 2 — View all registered students
    # ═══════════════════════════════════════════════════════
    with tab_view:
        st.markdown('<div class="page-title">Registered Students Roster</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="page-subtitle">'
            f'{len(st.session_state.registered_students)} student(s) currently registered in memory'
            f'</div>',
            unsafe_allow_html=True,
        )

        if not st.session_state.registered_students:
            st.info("No students registered yet. Use the Register tab to add a student.")
            return

        df = pd.DataFrame(st.session_state.registered_students)

        # Search filter
        search = st.text_input(
            "Search", placeholder="Search by name, ID, or department…",
            label_visibility="collapsed", key="form_search"
        )
        if search:
            mask = (
                df["Name"].str.contains(search, case=False, na=False)
                | df["Student ID"].str.contains(search, case=False, na=False)
                | df["Department"].str.contains(search, case=False, na=False)
            )
            df = df[mask]

        st.dataframe(df, use_container_width=True, hide_index=True)

        # Summary metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Enrolled", len(st.session_state.registered_students))
        if not df.empty:
            top_dept = (
                pd.DataFrame(st.session_state.registered_students)["Department"]
                .value_counts()
                .idxmax()
            )
            m2.metric("Primary Department", top_dept.split("&")[0].strip())
        m3.metric("Matching Filters", len(df))

        # CSV export
        csv_data = pd.DataFrame(st.session_state.registered_students).to_csv(index=False)
        st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
        st.download_button(
            label="⬇️  Download Registration List (CSV)",
            data=csv_data,
            file_name="registered_students.csv",
            mime="text/csv",
            use_container_width=True,
        )
