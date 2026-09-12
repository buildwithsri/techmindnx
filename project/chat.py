


import streamlit as st

st.set_page_config(
    page_title="Academic Chatbot",
    page_icon="🤖"
)

st.title("🤖 Academic Assistant")
st.write("Ask me anything about the Academic Portal!")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def get_response(question):

    question = question.lower()

    if "hello" in question or "hi" in question:
        return "Hello! 👋 How can I help you?"

    elif "attendance" in question:
        return "You can check your attendance in the Attendance section of the Student Portal."

    elif "marks" in question or "result" in question:
        return "You can view your marks and examination results in the Results section."

    elif "timetable" in question or "time table" in question:
        return "Your class timetable is available in the Timetable section."

    elif "course" in question or "subject" in question:
        return "You can view your registered courses and subjects in the Courses section."

    elif "fee" in question or "fees" in question:
        return "You can check your fee details and payment status in the Fees section."

    elif "profile" in question:
        return "You can view your personal information in the Profile section."

    elif "password" in question:
        return "If you forgot your password, please contact the administrator."

    elif "staff" in question:
        return "Staff-related information is available in the Staff Portal."

    elif "admin" in question or "management" in question:
        return "Management users can access administrative reports and portal management features."

    elif "help" in question:
        return """
I can help you with:

- Attendance
- Marks and results
- Timetable
- Courses and subjects
- Fees
- Profile
- Password
- Staff Portal
- Management Portal
"""

    else:
        return "Sorry, I don't understand your question. Please try asking about attendance, marks, timetable, courses, fees, or profile."


# Chat input
prompt = st.chat_input("Type your question here...")

if prompt:

    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # Generate response
    response = get_response(prompt)

    # Show chatbot response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })