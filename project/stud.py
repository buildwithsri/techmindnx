import streamlit as st

# -------------------------------------------------
# PAGE CONFIGcd
# -------------------------------------------------

st.set_page_config(
    page_title="Student Management Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main background */
.stApp {
    background-color: #f5f7fb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Title */
.main-title {
    font-size: 32px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 5px;
}

.subtitle {
    color: #6b7280;
    font-size: 15px;
    margin-bottom: 25px;
}

/* Welcome card */
.welcome-card {
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    padding: 28px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.welcome-card h2 {
    color: white;
    margin-bottom: 5px;
}

.welcome-card p {
    color: #dbeafe;
}

/* Cards */
.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}

.card-title {
    color: #6b7280;
    font-size: 14px;
}

.card-value {
    color: #111827;
    font-size: 28px;
    font-weight: 700;
    margin-top: 8px;
}

/* Profile */
.profile-item {
    display: flex;
    justify-content: space-between;
    padding: 15px 0;
    border-bottom: 1px solid #eeeeee;
}

.profile-label {
    color: #6b7280;
}

.profile-value {
    color: #111827;
    font-weight: 600;
}

/* Sidebar logo */
.logo {
    text-align: center;
    padding: 20px 0 30px 0;
}

.logo-icon {
    font-size: 42px;
}

.logo-title {
    font-size: 20px;
    font-weight: bold;
}

.logo-subtitle {
    font-size: 12px;
    color: #9ca3af !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SAMPLE STUDENT DATA
# -------------------------------------------------

student = {
    "id": "STU2026001",
    "name": "Roshni",
    "department": "Computer Science & Engineering",
    "semester": "5",
    "email": "roshni@example.com",
    "phone": "+91 98765 43210"
}

attendance = {
    "overall": 87,
    "required": 75,
    "subjects": [
        ["Python Programming", 40, 36, "90%"],
        ["Database Management", 38, 31, "81.6%"],
        ["Computer Networks", 42, 36, "85.7%"],
        ["Software Engineering", 35, 32, "91.4%"]
    ]
}

marks = [
    ["Python Programming", 27, 62, 89],
    ["Database Management", 25, 55, 80],
    ["Computer Networks", 26, 57, 83],
    ["Software Engineering", 28, 59, 87]
]

events = [
    ["EVT001", "Tech Fest 2026", "20 Sep 2026", "Main Auditorium"],
    ["EVT002", "Sports Meet", "28 Sep 2026", "College Ground"],
    ["EVT003", "Cultural Fest", "05 Oct 2026", "Open Stage"]
]

fee = {
    "total": 50000,
    "paid": 50000,
    "balance": 0
}

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div class="logo">
        <div class="logo-icon">🎓</div>
        <div class="logo-title">Student Portal</div>
        <div class="logo-subtitle">Management System</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📅 Attendance",
            "📝 Exam Marks",
            "👤 Profile",
            "🎫 Event Registration",
            "💳 Fee Payments"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.write("Logged in as")
    st.markdown(f"**{student['name']}**")
    st.caption(student["id"])

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown(
    '<div class="main-title">Student Management Portal</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Student academic and campus services</div>',
    unsafe_allow_html=True
)

# =================================================
# DASHBOARD
# =================================================

if page == "🏠 Dashboard":

    st.markdown(f"""
    <div class="welcome-card">
        <h2>Welcome, {student["name"]} 👋</h2>
        <p>
            {student["department"]} &nbsp; | &nbsp;
            Semester {student["semester"]} &nbsp; | &nbsp;
            {student["id"]}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">Attendance</div>
            <div class="card-value">87%</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Average Marks</div>
            <div class="card-value">84%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <div class="card-title">Exam Eligibility</div>
            <div class="card-value">Eligible</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="card">
            <div class="card-title">Fee Status</div>
            <div class="card-value">Paid</div>
        </div>
        """, unsafe_allow_html=True)

    # Overview
    left, right = st.columns(2)

    with left:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📅 Attendance")

        st.progress(attendance["overall"] / 100)

        st.write(
            f"Overall Attendance: **{attendance['overall']}%**"
        )

        st.write(
            f"Minimum Required: **{attendance['required']}%**"
        )

        if attendance["overall"] >= attendance["required"]:
            st.success("Attendance requirement satisfied")
        else:
            st.warning("Attendance requirement not satisfied")

        st.markdown('</div>', unsafe_allow_html=True)

    with right:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📝 Recent Exam Marks")

        for subject in marks:
            st.write(
                f"**{subject[0]}** — {subject[3]}/100"
            )

        st.markdown('</div>', unsafe_allow_html=True)


# =================================================
# ATTENDANCE
# =================================================

elif page == "📅 Attendance":

    st.header("📅 Attendance")

    st.write(
        "View your subject-wise attendance details."
    )

    st.metric(
        "Overall Attendance",
        f"{attendance['overall']}%"
    )

    st.progress(attendance["overall"] / 100)

    st.subheader("Subject-wise Attendance")

    table_data = []

    for subject in attendance["subjects"]:

        table_data.append({
            "Subject": subject[0],
            "Classes Held": subject[1],
            "Classes Attended": subject[2],
            "Attendance": subject[3]
        })

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True
    )


# =================================================
# EXAM MARKS
# =================================================

elif page == "📝 Exam Marks":

    st.header("📝 Exam Marks")

    st.write(
        "View internal, external and total examination marks."
    )

    table_data = []

    for item in marks:

        table_data.append({
            "Subject": item[0],
            "Internal": item[1],
            "External": item[2],
            "Total": item[3]
        })

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True
    )

    average = sum(x[3] for x in marks) / len(marks)

    st.metric(
        "Average Marks",
        f"{average:.1f}%"
    )


# =================================================
# PROFILE
# =================================================

elif page == "👤 Profile":

    st.header("👤 Student Profile")

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    profile = {
        "Student ID": student["id"],
        "Name": student["name"],
        "Department": student["department"],
        "Semester": student["semester"],
        "Email": student["email"],
        "Phone": student["phone"]
    }

    for label, value in profile.items():

        st.markdown(
            f"""
            <div class="profile-item">
                <span class="profile-label">{label}</span>
                <span class="profile-value">{value}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


# =================================================
# EVENT REGISTRATION
# =================================================

elif page == "🎫 Event Registration":

    st.header("🎫 Event Registration")

    st.write(
        "Register for upcoming college events."
    )

    for event in events:

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.subheader(event[1])

                st.write(
                    f"📅 {event[2]}"
                )

                st.write(
                    f"📍 {event[3]}"
                )

            with col2:

                if st.button(
                    "Register",
                    key=event[0],
                    use_container_width=True
                ):
                    st.success(
                        f"Registered for {event[1]}"
                    )


# =================================================
# FEE PAYMENTS
# =================================================

elif page == "💳 Fee Payments":

    st.header("💳 Fee Payments")

    st.write(
        "View your college fee payment information."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Fee",
            f"₹{fee['total']:,}"
        )

    with col2:
        st.metric(
            "Paid",
            f"₹{fee['paid']:,}"
        )

    with col3:
        st.metric(
            "Balance",
            f"₹{fee['balance']:,}"
        )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    if fee["balance"] == 0:

        st.success(
            "Your fee payment is completely paid."
        )

    else:

        st.warning(
            f"Outstanding balance: ₹{fee['balance']:,}"
        )

        if st.button(
            "Pay Remaining Fee",
            type="primary"
        ):
            st.info(
                "Demo only. No payment backend is connected."
            )

    st.markdown('</div>', unsafe_allow_html=True)