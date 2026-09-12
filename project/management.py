
import random
import string

import streamlit as st

st.set_page_config(page_title="Management Portal", page_icon="🎓", layout="wide")

# ---------------------------------------------------------------------------
# Dummy "database" (prototype only)
# ---------------------------------------------------------------------------

COLLECTIONS = {"staff": "Staff", "students": "Students"}


def seed_staff():
    return [
        {"id": 1, "login": "prof.rao", "password": "Faculty#101"},
        {"id": 2, "login": "dr.menon", "password": "Faculty#102"},
        {"id": 3, "login": "admin.jose", "password": "Faculty#103"},
        {"id": 4, "login": "lib.anu", "password": "Faculty#104"},
    ]


def seed_students():
    return [
        {"id": 1, "login": "stu.arjun21", "password": "Student#201"},
        {"id": 2, "login": "stu.divya22", "password": "Student#202"},
        {"id": 3, "login": "stu.farhan23", "password": "Student#203"},
        {"id": 4, "login": "stu.leah24", "password": "Student#204"},
        {"id": 5, "login": "stu.nihal25", "password": "Student#205"},
    ]


def init_state():
    if "staff" not in st.session_state:
        st.session_state.staff = seed_staff()
    if "students" not in st.session_state:
        st.session_state.students = seed_students()
    if "next_id" not in st.session_state:
        st.session_state.next_id = {"staff": 5, "students": 6}
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if "reset_result" not in st.session_state:
        st.session_state.reset_result = None


init_state()


def hash_password_for_real_system(plaintext_password):
    """Placeholder only — a real system would hash this, never store it as-is."""
    return plaintext_password


def generate_temp_password(length=10):
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def find_account(collection, account_id):
    for account in st.session_state[collection]:
        if account["id"] == account_id:
            return account
    return None


def mask_password(pw):
    return "•" * min(max(len(pw), 6), 10)


def create_account(collection, login, password):
    if any(a["login"].lower() == login.lower() for a in st.session_state[collection]):
        return False, "That login already exists."
    new_id = st.session_state.next_id[collection]
    st.session_state.next_id[collection] += 1
    st.session_state[collection].append(
        {"id": new_id, "login": login, "password": hash_password_for_real_system(password)}
    )
    return True, "Account created."


def update_account(collection, account_id, login, password):
    duplicate = any(
        a["login"].lower() == login.lower() and a["id"] != account_id
        for a in st.session_state[collection]
    )
    if duplicate:
        return False, "That login is already in use."
    account = find_account(collection, account_id)
    account["login"] = login
    account["password"] = hash_password_for_real_system(password)
    return True, "Account updated."


def delete_account(collection, account_id):
    st.session_state[collection] = [
        a for a in st.session_state[collection] if a["id"] != account_id
    ]


def reset_password(collection, account_id):
    account = find_account(collection, account_id)
    temp = generate_temp_password()
    account["password"] = hash_password_for_real_system(temp)
    return temp


# ---------------------------------------------------------------------------
# Dialogs (modals)
# ---------------------------------------------------------------------------

@st.dialog("Add Account")
def add_dialog(collection):
    label = COLLECTIONS[collection].rstrip("s")
    st.caption(f"Create a new {label.lower()} account.")
    login = st.text_input("Login ID / Username", key=f"add_login_{collection}")
    password = st.text_input("Password", key=f"add_password_{collection}")

    col_cancel, col_confirm = st.columns(2)
    with col_cancel:
        if st.button("Cancel", key=f"add_cancel_{collection}", use_container_width=True):
            st.rerun()
    with col_confirm:
        if st.button("Create Account", key=f"add_confirm_{collection}", type="primary", use_container_width=True):
            if not login.strip() or not password.strip():
                st.error("Login and password are required.")
            else:
                ok, message = create_account(collection, login.strip(), password.strip())
                if ok:
                    st.toast(message, icon="✅")
                    st.rerun()
                else:
                    st.error(message)


@st.dialog("Edit Account")
def edit_dialog(collection, account_id):
    account = find_account(collection, account_id)
    if account is None:
        st.error("Account not found.")
        return

    st.caption("Update the login and password for this account.")
    login = st.text_input("Login ID / Username", value=account["login"], key=f"edit_login_{collection}_{account_id}")
    password = st.text_input("Password", value=account["password"], key=f"edit_password_{collection}_{account_id}")

    col_cancel, col_confirm = st.columns(2)
    with col_cancel:
        if st.button("Cancel", key=f"edit_cancel_{collection}_{account_id}", use_container_width=True):
            st.rerun()
    with col_confirm:
        if st.button("Save Changes", key=f"edit_confirm_{collection}_{account_id}", type="primary", use_container_width=True):
            if not login.strip() or not password.strip():
                st.error("Login and password are required.")
            else:
                ok, message = update_account(collection, account_id, login.strip(), password.strip())
                if ok:
                    st.toast(message, icon="✅")
                    st.rerun()
                else:
                    st.error(message)


@st.dialog("Reset Password?")
def reset_dialog(collection, account_id):
    account = find_account(collection, account_id)
    if account is None:
        st.error("Account not found.")
        return

    st.write("Are you sure you want to reset this account's password?")
    st.caption(f"Account: **{account['login']}**")

    col_cancel, col_confirm = st.columns(2)
    with col_cancel:
        if st.button("Cancel", key=f"reset_cancel_{collection}_{account_id}", use_container_width=True):
            st.rerun()
    with col_confirm:
        if st.button("Confirm Reset", key=f"reset_confirm_{collection}_{account_id}", type="primary", use_container_width=True):
            temp = reset_password(collection, account_id)
            st.session_state.reset_result = {
                "collection": collection,
                "login": account["login"],
                "temp_password": temp,
            }
            st.toast("Password reset.", icon="✅")
            st.rerun()


@st.dialog("Delete Account?")
def delete_dialog(collection, account_id):
    account = find_account(collection, account_id)
    if account is None:
        st.error("Account not found.")
        return

    st.write("This action cannot be undone.")
    st.caption(f"Account: **{account['login']}**")

    col_cancel, col_confirm = st.columns(2)
    with col_cancel:
        if st.button("Cancel", key=f"delete_cancel_{collection}_{account_id}", use_container_width=True):
            st.rerun()
    with col_confirm:
        if st.button("Delete", key=f"delete_confirm_{collection}_{account_id}", type="primary", use_container_width=True):
            delete_account(collection, account_id)
            st.toast("Account deleted.", icon="✅")
            st.rerun()


# ---------------------------------------------------------------------------
# Page renderers
# ---------------------------------------------------------------------------

def render_header():
    left, right = st.columns([5, 1])
    with left:
        crumb = "Dashboard" if st.session_state.page == "dashboard" else COLLECTIONS[st.session_state.page]
        st.markdown(f"### Management Portal")
        st.caption(f"Manage Staff and Student Accounts &nbsp;·&nbsp; **{crumb}**", unsafe_allow_html=True)
    with right:
        if st.session_state.page != "dashboard":
            st.write("")
            if st.button("← Back to Dashboard", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()
    st.divider()


def render_dashboard():
    st.subheader("Management Portal")
    st.caption("Manage Staff and Student Accounts")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("#### 🧑‍🏫 Staff Management")
            st.write("View and manage staff accounts")
            st.caption(f"{len(st.session_state.staff)} accounts")
            if st.button("Open Staff Management", key="goto_staff", use_container_width=True):
                st.session_state.page = "staff"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("#### 🎓 Student Management")
            st.write("View and manage student accounts")
            st.caption(f"{len(st.session_state.students)} accounts")
            if st.button("Open Student Management", key="goto_students", use_container_width=True):
                st.session_state.page = "students"
                st.rerun()


def render_management_page(collection):
    label = COLLECTIONS[collection]
    st.subheader(f"{label} Account Management")
    st.caption(f"Edit logins, reset passwords, or remove {label.lower()} accounts.")

    # show a one-time banner with a freshly reset temp password, if any
    result = st.session_state.reset_result
    if result and result["collection"] == collection:
        with st.container(border=True):
            st.success(
                f"Temporary password for **{result['login']}**: `{result['temp_password']}`  "
                "\n\nShare this with the account holder — it won't be shown again."
            )
            if st.button("Dismiss", key=f"dismiss_reset_{collection}"):
                st.session_state.reset_result = None
                st.rerun()

    toolbar_left, toolbar_right = st.columns([3, 1])
    with toolbar_left:
        search = st.text_input(
            "Search", placeholder=f"Search {label.lower()} logins…",
            key=f"search_{collection}", label_visibility="collapsed",
        )
    with toolbar_right:
        if st.button(f"Add {label.rstrip('s')} Account", key=f"add_btn_{collection}", use_container_width=True):
            add_dialog(collection)

    st.write("")

    query = (search or "").strip().lower()
    accounts = [a for a in st.session_state[collection] if query in a["login"].lower()]

    if not accounts:
        st.info("No matching accounts.")
        return

    header = st.columns([1, 3, 3, 1.3, 1.6, 1.1])
    for col, text in zip(header, ["ID", "Account Login", "Password", "", "", ""]):
        col.markdown(f"**{text}**")

    for account in accounts:
        c_id, c_login, c_pw, c_edit, c_reset, c_delete = st.columns([1, 3, 3, 1.3, 1.6, 1.1])
        c_id.write(account["id"])
        c_login.write(account["login"])
        c_pw.code(mask_password(account["password"]), language=None)

        if c_edit.button("Edit", key=f"edit_{collection}_{account['id']}", use_container_width=True):
            edit_dialog(collection, account["id"])
        if c_reset.button("Reset Password", key=f"reset_{collection}_{account['id']}", use_container_width=True):
            reset_dialog(collection, account["id"])
        if c_delete.button("Delete", key=f"delete_{collection}_{account['id']}", use_container_width=True):
            delete_dialog(collection, account["id"])


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

render_header()

if st.session_state.page == "dashboard":
    render_dashboard()
elif st.session_state.page in ("staff", "students"):
    render_management_page(st.session_state.page)
