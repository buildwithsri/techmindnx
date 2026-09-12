import streamlit as st
import sqlite3
import os
import re
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Student Registration",
    page_icon="🎓",
    layout="wide"
)

# =========================================================
# DATABASE SETUP
# =========================================================

DB_NAME = "students.db"
PHOTO_FOLDER = "student_photos"

os.makedirs(PHOTO_FOLDER, exist_ok=True)


def create_database():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            emergency_contact TEXT NOT NULL,
            department TEXT NOT NULL,
            photo TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


create_database()


# =========================================================
# GENERATE STUDENT ID
# =========================================================

def generate_student_id():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id
        FROM students
        WHERE student_id LIKE 'FIT26DL%'
        ORDER BY student_id DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    conn.close()

    if result is None:
        number = 100
    else:
        last_id = result[0]
        number = int(last_id.replace("FIT26DL", "")) + 1

    return f"FIT26DL{number}"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

.main-title {
    font-size: 32px;
    font-weight: 700;
    color: #111827;
}

.subtitle {
    color: #6b7280;
    font-size: 16px;
    margin-bottom: 25px;
}

.form-card {
    background-color: white;
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
}

.id-box {
    background-color: #eff6ff;
    border: 1px solid #bfdbfe;
    padding: 15px;
    border-radius: 10px;
    color: #1d4ed8;
    font-size: 20px;
    font-weight: 700;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🎓 Student Registration</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Register a new student in the Academic Management Platform.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# GENERATE ID
# =========================================================

student_id = generate_student_id()

st.markdown(
    f"""
    <div class="id-box">
        Student ID: {student_id}
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# =========================================================
# STUDENT FORM
# =========================================================

with st.form("student_registration_form"):

    st.subheader("👤 Personal Information")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Student Name *",
            placeholder="Enter full name"
        )

        phone = st.text_input(
            "Phone Number *",
            placeholder="+91 98765 43210"
        )

        email = st.text_input(
            "Email Address *",
            placeholder="student@example.com"
        )

    with col2:

        department = st.selectbox(
            "Department *",
            [
                "Computer Science & Engineering",
                "Artificial Intelligence & Data Science",
                "Information Technology",
                "Electronics & Communication Engineering",
                "Electrical & Electronics Engineering",
                "Mechanical Engineering",
                "Civil Engineering",
                "Other"
            ]
        )

        emergency_contact = st.text_input(
            "Emergency Contact *",
            placeholder="+91 98765 43210"
        )

    address = st.text_area(
        "Address *",
        placeholder="Enter student's complete address",
        height=100
    )

    st.subheader("📷 Student Photo")

    photo = st.file_uploader(
        "Upload Student Photo",
        type=["jpg", "jpeg", "png"],
        help="Upload a JPG or PNG image."
    )

    st.write("")

    submitted = st.form_submit_button(
        "➕ Register Student",
        use_container_width=True,
        type="primary"
    )


# =========================================================
# FORM VALIDATION & SAVE
# =========================================================

if submitted:

    # ---------------------------------------------
    # Required field validation
    # ---------------------------------------------

    if not name.strip():
        st.error("❌ Please enter the student's name.")

    elif not phone.strip():
        st.error("❌ Please enter the phone number.")

    elif not email.strip():
        st.error("❌ Please enter the email address.")

    elif not address.strip():
        st.error("❌ Please enter the address.")

    elif not emergency_contact.strip():
        st.error("❌ Please enter the emergency contact.")

    elif not photo:
        st.error("❌ Please upload a student photo.")

    # ---------------------------------------------
    # Phone validation
    # ---------------------------------------------

    elif not re.fullmatch(r"[0-9+\-\s()]{7,20}", phone):
        st.error("❌ Please enter a valid phone number.")

    # ---------------------------------------------
    # Email validation
    # ---------------------------------------------

    elif not re.fullmatch(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        email
    ):
        st.error("❌ Please enter a valid email address.")

    else:

        # -----------------------------------------
        # Save photo
        # -----------------------------------------

        file_extension = os.path.splitext(photo.name)[1]

        photo_filename = f"{student_id}{file_extension}"

        photo_path = os.path.join(
            PHOTO_FOLDER,
            photo_filename
        )

        with open(photo_path, "wb") as file:
            file.write(photo.getbuffer())

        # -----------------------------------------
        # Save student to database
        # -----------------------------------------

        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students (
                student_id,
                name,
                phone,
                email,
                address,
                emergency_contact,
                department,
                photo,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            name.strip(),
            phone.strip(),
            email.strip(),
            address.strip(),
            emergency_contact.strip(),
            department,
            photo_path,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        # -----------------------------------------
        # Success message
        # -----------------------------------------

        st.success(
            f"✅ Student registered successfully! "
            f"Student ID: {student_id}"
        )

        # -----------------------------------------
        # Display registered information
        # -----------------------------------------

        st.subheader("📋 Student Details")

        col1, col2 = st.columns([1, 2])

        with col1:

            st.image(
                photo_path,
                caption=name,
                width=180
            )

        with col2:

            st.write(f"**Student ID:** {student_id}")
            st.write(f"**Name:** {name}")
            st.write(f"**Phone:** {phone}")
            st.write(f"**Email:** {email}")
            st.write(f"**Department:** {department}")
            st.write(f"**Emergency Contact:** {emergency_contact}")
            st.write(f"**Address:** {address}")

