import streamlit as st

st.set_page_config(
    page_title="Academic Platform",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Academic Platform")
st.write("Please login to access your academic dashboard.")

st.divider()

st.subheader("Student Login")

student_id = st.text_input(
    "Student ID",
    placeholder="Enter your Student ID"
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter your password"
)

if st.button("🔐 Login", use_container_width=True):

    if student_id == "FIT26DL100" and password == "A@123":
        st.success("✅ Login successful!")
        st.write(f"Welcome, {student_id}!")

    else:
        st.error("❌ Invalid Student ID or password.")
