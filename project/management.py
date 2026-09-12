import streamlit as st
import pandas as pd
import random
import string

# ─── Seed Data (module-level) ────────────────────────────────────────────────

SEED_STAFF = [
    {"id": "TVE-STF-001", "name": "Dr. Arjun Nair",   "username": "prof.rao",  "role": "Faculty",    "dept": "CSE", "email": "arjun@tve.edu",   "phone": "+91 94460 12345", "status": "Active",   "password": "Faculty#101"},
    {"id": "TVE-STF-002", "name": "Dr. Meera Pillai",  "username": "dr.menon",  "role": "Faculty",    "dept": "ECE", "email": "meera@tve.edu",   "phone": "+91 94460 67890", "status": "Active",   "password": "Faculty#102"},
    {"id": "TVE-STF-003", "name": "Admin Jose",        "username": "admin.jose","role": "Admin",      "dept": "Admin","email": "jose@tve.edu",   "phone": "+91 98001 11223", "status": "Active",   "password": "Faculty#103"},
    {"id": "TVE-STF-004", "name": "Lib. Anu",          "username": "lib.anu",   "role": "Librarian",  "dept": "LIB", "email": "anu@tve.edu",     "phone": "+91 96330 55678", "status": "On Leave", "password": "Faculty#104"},
]

SEED_STUDENTS = [
    {"id": "TVE-STU-001", "name": "Aditya Sharma",  "username": "stu.arjun21", "dept": "CSE", "sem": "S6", "email": "aditya@tve.edu",  "phone": "+91 98765 43210", "status": "Active",    "password": "Student#201"},
    {"id": "TVE-STU-002", "name": "Bhavana Nair",   "username": "stu.divya22", "dept": "CSE", "sem": "S6", "email": "bhavana@tve.edu", "phone": "+91 98765 43211", "status": "Active",    "password": "Student#202"},
    {"id": "TVE-STU-003", "name": "Chetan Pillai",  "username": "stu.farhan23","dept": "CSE", "sem": "S6", "email": "chetan@tve.edu",  "phone": "+91 98765 43212", "status": "Active",    "password": "Student#203"},
    {"id": "TVE-STU-004", "name": "Deepthi Menon",  "username": "stu.leah24",  "dept": "CSE", "sem": "S6", "email": "deepthi@tve.edu", "phone": "+91 98765 43213", "status": "Suspended", "password": "Student#204"},
    {"id": "TVE-STU-005", "name": "Edwin Jose",     "username": "stu.nihal25", "dept": "CSE", "sem": "S6", "email": "edwin@tve.edu",   "phone": "+91 98765 43214", "status": "Active",    "password": "Student#205"},
]

DEPARTMENTS = ["CSE", "ECE", "ME", "CE", "EEE", "Admin", "LIB"]
ROLES       = ["Faculty", "HOD", "Admin", "Librarian", "Lab Staff"]


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _init_mgmt_state():
    if "mgmt_staff" not in st.session_state:
        st.session_state.mgmt_staff    = list(SEED_STAFF)
    if "mgmt_students" not in st.session_state:
        st.session_state.mgmt_students = list(SEED_STUDENTS)
    if "mgmt_next_id" not in st.session_state:
        st.session_state.mgmt_next_id  = 5
    if "mgmt_page" not in st.session_state:
        st.session_state.mgmt_page     = "dashboard"
    if "mgmt_reset_result" not in st.session_state:
        st.session_state.mgmt_reset_result = None


def _rand_password(length=10):
    chars = string.ascii_letters + string.digits + "!@#"
    return "".join(random.choices(chars, k=length))


def _find(collection, uid):
    for item in st.session_state[collection]:
        if item["id"] == uid:
            return item
    return None


def _delete(collection, uid):
    st.session_state[collection] = [
        x for x in st.session_state[collection] if x["id"] != uid
    ]


# ─── Dialogs ─────────────────────────────────────────────────────────────────

@st.dialog("Add New Staff Account")
def _add_staff_dialog():
    c1, c2 = st.columns(2)
    name     = c1.text_input("Full Name *", placeholder="Dr. Firstname Lastname")
    username = c2.text_input("Username *", placeholder="e.g. prof.rao")
    dept     = c1.selectbox("Department", DEPARTMENTS)
    role     = c2.selectbox("Role", ROLES)
    email    = c1.text_input("Email *", placeholder="staff@tve.edu")
    phone    = c2.text_input("Phone", placeholder="+91 94460 00000")
    pwd      = _rand_password()
    st.info(f"🔑 **Generated Temporary Password:** `{pwd}`")
    if st.button("Create Account", type="primary", use_container_width=True):
        if not (name and username and email):
            st.error("Name, username and email are required.")
        elif any(x["username"] == username for x in st.session_state.mgmt_staff):
            st.error("Username already exists in the system.")
        else:
            nid = f"TVE-STF-{st.session_state.mgmt_next_id:03d}"
            st.session_state.mgmt_next_id += 1
            st.session_state.mgmt_staff.append({
                "id": nid, "name": name, "username": username,
                "role": role, "dept": dept, "email": email,
                "phone": phone, "status": "Active", "password": pwd,
            })
            st.rerun()


@st.dialog("Edit Staff Account")
def _edit_staff_dialog(uid):
    rec = _find("mgmt_staff", uid)
    if not rec:
        st.error("Record not found.")
        return
    c1, c2 = st.columns(2)
    rec["name"]   = c1.text_input("Full Name",   value=rec["name"])
    rec["dept"]   = c1.selectbox("Department",   DEPARTMENTS, index=DEPARTMENTS.index(rec["dept"]) if rec["dept"] in DEPARTMENTS else 0)
    rec["role"]   = c2.selectbox("Role",         ROLES, index=ROLES.index(rec["role"]) if rec["role"] in ROLES else 0)
    rec["email"]  = c2.text_input("Email",       value=rec["email"])
    rec["phone"]  = c1.text_input("Phone",       value=rec["phone"])
    rec["status"] = c2.selectbox("Status",       ["Active", "On Leave", "Inactive"], index=["Active", "On Leave", "Inactive"].index(rec["status"]))
    if st.button("Save Changes", type="primary", use_container_width=True):
        st.rerun()


@st.dialog("Reset Staff Password")
def _reset_staff_dialog(uid):
    rec = _find("mgmt_staff", uid)
    if not rec:
        st.error("Record not found.")
        return
    st.write(f"Reset credentials for **{rec['name']}** (`{rec['username']}`)")
    mode = st.radio("Mode", ["Auto-generate secure password", "Set custom password"], horizontal=True)
    if mode == "Auto-generate secure password":
        new_pwd = _rand_password()
        st.info(f"🔑 **Generated Password:** `{new_pwd}`")
    else:
        new_pwd = st.text_input("New Password", type="password")
        conf    = st.text_input("Confirm Password", type="password")
        if new_pwd != conf:
            st.warning("Passwords do not match.")
            new_pwd = None
    if st.button("Confirm Password Reset", type="primary", use_container_width=True) and new_pwd:
        rec["password"] = new_pwd
        st.session_state.mgmt_reset_result = {"collection": "mgmt_staff", "uid": uid, "password": new_pwd}
        st.rerun()


@st.dialog("Add New Student Account")
def _add_student_dialog():
    c1, c2 = st.columns(2)
    name     = c1.text_input("Full Name *", placeholder="Student Name")
    username = c2.text_input("Username *", placeholder="e.g. stu.arjun21")
    dept     = c1.selectbox("Department", ["CSE", "ECE", "ME", "CE", "EEE"])
    sem      = c2.selectbox("Semester", ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"])
    email    = c1.text_input("Email *", placeholder="student@tve.edu")
    phone    = c2.text_input("Phone", placeholder="+91 98765 43210")
    pwd      = _rand_password()
    st.info(f"🔑 **Generated Temporary Password:** `{pwd}`")
    if st.button("Create Student Account", type="primary", use_container_width=True):
        if not (name and username and email):
            st.error("Name, username and email are required.")
        elif any(x["username"] == username for x in st.session_state.mgmt_students):
            st.error("Username already exists in the system.")
        else:
            nid = f"TVE-STU-{st.session_state.mgmt_next_id:03d}"
            st.session_state.mgmt_next_id += 1
            st.session_state.mgmt_students.append({
                "id": nid, "name": name, "username": username,
                "dept": dept, "sem": sem, "email": email,
                "phone": phone, "status": "Active", "password": pwd,
            })
            st.rerun()


@st.dialog("Edit Student Account")
def _edit_student_dialog(uid):
    rec = _find("mgmt_students", uid)
    if not rec:
        st.error("Record not found.")
        return
    c1, c2 = st.columns(2)
    rec["name"]   = c1.text_input("Full Name",   value=rec["name"])
    rec["dept"]   = c1.selectbox("Department",   ["CSE", "ECE", "ME", "CE", "EEE"], index=["CSE","ECE","ME","CE","EEE"].index(rec["dept"]) if rec["dept"] in ["CSE","ECE","ME","CE","EEE"] else 0)
    rec["sem"]    = c2.selectbox("Semester",     ["S1","S2","S3","S4","S5","S6","S7","S8"], index=["S1","S2","S3","S4","S5","S6","S7","S8"].index(rec["sem"]) if rec["sem"] in ["S1","S2","S3","S4","S5","S6","S7","S8"] else 0)
    rec["email"]  = c2.text_input("Email",       value=rec["email"])
    rec["phone"]  = c1.text_input("Phone",       value=rec["phone"])
    rec["status"] = c2.selectbox("Status",       ["Active", "Suspended", "Alumni"], index=["Active", "Suspended", "Alumni"].index(rec["status"]) if rec["status"] in ["Active", "Suspended", "Alumni"] else 0)
    if st.button("Save Changes", type="primary", use_container_width=True):
        st.rerun()


@st.dialog("Reset Student Password")
def _reset_student_dialog(uid):
    rec = _find("mgmt_students", uid)
    if not rec:
        st.error("Record not found.")
        return
    st.write(f"Reset credentials for **{rec['name']}** (`{rec['username']}`)")
    mode = st.radio("Mode", ["Auto-generate secure password", "Set custom password"], horizontal=True)
    if mode == "Auto-generate secure password":
        new_pwd = _rand_password()
        st.info(f"🔑 **Generated Password:** `{new_pwd}`")
    else:
        new_pwd = st.text_input("New Password", type="password")
        conf    = st.text_input("Confirm Password", type="password")
        if new_pwd != conf:
            st.warning("Passwords do not match.")
            new_pwd = None
    if st.button("Confirm Password Reset", type="primary", use_container_width=True) and new_pwd:
        rec["password"] = new_pwd
        st.session_state.mgmt_reset_result = {"collection": "mgmt_students", "uid": uid, "password": new_pwd}
        st.rerun()


# ─── Sub-renders ─────────────────────────────────────────────────────────────

def _render_mgmt_header():
    col_t, col_nav = st.columns([4, 1])
    with col_t:
        crumb = (
            "Dashboard"
            if st.session_state.mgmt_page == "dashboard"
            else ("Staff Accounts" if st.session_state.mgmt_page == "mgmt_staff" else "Student Accounts")
        )
        st.markdown(f"<div style='font-size:0.84rem;color:#64748b;font-weight:600;margin-bottom:0.5rem;'>Account Management &nbsp;›&nbsp; <strong style='color:#0f172a;'>{crumb}</strong></div>", unsafe_allow_html=True)
    with col_nav:
        if st.session_state.mgmt_page != "dashboard":
            if st.button("← Back to Hub", key="mgmt_back", use_container_width=True):
                st.session_state.mgmt_page = "dashboard"
                st.rerun()


def _render_mgmt_dashboard():
    st.markdown('<div class="page-title">Account Management</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Configure, provision and govern staff and student credentials across the campus</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2, gap="large")

    with c1:
        active_staff = sum(1 for x in st.session_state.mgmt_staff if x["status"] == "Active")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 50%, #2563eb 100%);
                    border-radius: 16px; padding: 2rem 2.2rem; color: white; margin-bottom: 1.2rem;
                    box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.25);">
            <div style="font-size: 0.82rem; color: rgba(255,255,255,0.8); font-weight: 700;
                        text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.4rem;">
                Faculty &amp; Staff Accounts
            </div>
            <div style="font-family: 'Sora', sans-serif; font-size: 3.2rem; font-weight: 700; line-height: 1;">
                {len(st.session_state.mgmt_staff)}
            </div>
            <div style="font-size: 0.85rem; color: rgba(255,255,255,0.85); margin-top: 0.6rem;">
                <strong>{active_staff}</strong> active users &nbsp;·&nbsp; {len(st.session_state.mgmt_staff)-active_staff} on leave / offboarded
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Manage Faculty & Staff Accounts →", key="goto_staff",
                     use_container_width=True, type="primary"):
            st.session_state.mgmt_page = "mgmt_staff"
            st.rerun()

    with c2:
        active_stu = sum(1 for x in st.session_state.mgmt_students if x["status"] == "Active")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #065f46 0%, #047857 50%, #059669 100%);
                    border-radius: 16px; padding: 2rem 2.2rem; color: white; margin-bottom: 1.2rem;
                    box-shadow: 0 10px 25px -5px rgba(5, 150, 105, 0.25);">
            <div style="font-size: 0.82rem; color: rgba(255,255,255,0.8); font-weight: 700;
                        text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.4rem;">
                Student Accounts
            </div>
            <div style="font-family: 'Sora', sans-serif; font-size: 3.2rem; font-weight: 700; line-height: 1;">
                {len(st.session_state.mgmt_students)}
            </div>
            <div style="font-size: 0.85rem; color: rgba(255,255,255,0.85); margin-top: 0.6rem;">
                <strong>{active_stu}</strong> active enrolled &nbsp;·&nbsp; {len(st.session_state.mgmt_students)-active_stu} suspended / alumni
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Manage Student Accounts →", key="goto_students",
                     use_container_width=True, type="primary"):
            st.session_state.mgmt_page = "mgmt_students"
            st.rerun()


def _render_management_page(collection: str):
    """Shared CRUD table for both 'mgmt_staff' and 'mgmt_students'."""
    is_staff = collection == "mgmt_staff"
    label    = "Faculty / Staff" if is_staff else "Student"

    # ── Password reset notification ───────────────────────────────────────────
    result = st.session_state.mgmt_reset_result
    if result and result.get("collection") == collection:
        st.success(
            f"✅ Password for **{result['uid']}** reset to: `{result['password']}`  "
            f"— please deliver securely to user."
        )
        st.session_state.mgmt_reset_result = None

    # ── Header + add button ───────────────────────────────────────────────────
    head_l, head_r = st.columns([3.5, 1.5])
    head_l.markdown(f'<div class="page-title">{label} Accounts Directory</div>', unsafe_allow_html=True)
    with head_r:
        if st.button(f"➕  Add New {label}", type="primary", use_container_width=True):
            if is_staff:
                _add_staff_dialog()
            else:
                _add_student_dialog()

    # ── Search + filter ───────────────────────────────────────────────────────
    sf1, sf2 = st.columns([3, 1])
    search = sf1.text_input("Search", placeholder=f"Search by name, username or email…",
                             label_visibility="collapsed", key=f"{collection}_search")
    status_filter = sf2.selectbox(
        "Status",
        ["All", "Active", "On Leave", "Inactive", "Suspended"],
        label_visibility="collapsed",
        key=f"{collection}_status",
    )

    records = st.session_state[collection]
    if search:
        records = [
            r for r in records
            if search.lower() in r["name"].lower()
            or search.lower() in r["username"].lower()
            or search.lower() in r["email"].lower()
        ]
    if status_filter != "All":
        records = [r for r in records if r["status"] == status_filter]

    st.markdown(f"<div style='font-size:0.82rem;color:#64748b;margin-bottom:1rem;'>Showing <strong>{len(records)}</strong> registered account(s)</div>",
                unsafe_allow_html=True)

    # ── Table header ──────────────────────────────────────────────────────────
    cols_def = [2, 3, 2, 2, 3, 1.5, 2.5]
    if is_staff:
        headers = ["ID", "Name / Username", "Role", "Dept", "Email", "Status", "Actions"]
    else:
        headers = ["ID", "Name / Username", "Semester", "Dept", "Email", "Status", "Actions"]

    with st.container(border=True):
        h_cols = st.columns(cols_def)
        for h, c in zip(headers, h_cols):
            c.markdown(f"<div style='font-size:0.75rem;font-weight:700;color:#64748b;text-transform:uppercase;padding-bottom:6px;'>{h}</div>",
                       unsafe_allow_html=True)

        st.markdown("<hr style='border:none;border-top:1px solid #e2e8f0;margin:4px 0 10px 0;'>", unsafe_allow_html=True)

        # ── Rows ──────────────────────────────────────────────────────────────────
        status_badge = {
            "Active":    "badge-green",
            "On Leave":  "badge-amber",
            "Inactive":  "badge-slate",
            "Suspended": "badge-red",
            "Alumni":    "badge-blue",
        }

        for rec in records:
            row = st.columns(cols_def)
            row[0].markdown(f"<div style='font-size:0.82rem;color:#64748b;padding-top:6px;font-family:monospace;'>{rec['id']}</div>",
                            unsafe_allow_html=True)
            row[1].markdown(f"""
                <div style='padding-top:2px;'>
                    <div style='font-weight:600;color:#0f172a;font-size:0.9rem;'>{rec['name']}</div>
                    <div style='font-size:0.75rem;color:#64748b;'>@{rec['username']}</div>
                </div>""", unsafe_allow_html=True)
            row[2].markdown(f"<div style='padding-top:6px;font-size:0.86rem;color:#334155;'>{rec.get('role', rec.get('sem',''))}</div>",
                            unsafe_allow_html=True)
            row[3].markdown(f"<div style='padding-top:6px;font-size:0.86rem;color:#334155;font-weight:600;'>{rec.get('dept','')}</div>",
                            unsafe_allow_html=True)
            row[4].markdown(f"<div style='padding-top:6px;font-size:0.84rem;color:#475569;word-break:break-all;'>{rec['email']}</div>",
                            unsafe_allow_html=True)
            sb = status_badge.get(rec["status"], "badge-slate")
            row[5].markdown(f"<div style='padding-top:6px;'><span class='badge {sb}'>{rec['status']}</span></div>",
                            unsafe_allow_html=True)

            act1, act2, act3, act4 = row[6].columns(4)
            if act1.button("✏️", key=f"edit_{rec['id']}", help="Edit account details"):
                if is_staff: _edit_staff_dialog(rec["id"])
                else:        _edit_student_dialog(rec["id"])
            if act2.button("🔑", key=f"rst_{rec['id']}", help="Reset password"):
                if is_staff: _reset_staff_dialog(rec["id"])
                else:        _reset_student_dialog(rec["id"])
            if act3.button("🚫", key=f"sus_{rec['id']}", help="Suspend account"):
                rec["status"] = "Suspended"
                st.rerun()
            if act4.button("🗑️", key=f"del_{rec['id']}", help="Delete account"):
                _delete(collection, rec["id"])
                st.rerun()

            st.markdown("<hr style='border:none;border-top:1px solid #f1f5f9;margin:6px 0;'>", unsafe_allow_html=True)

    # ── Export ────────────────────────────────────────────────────────────────
    if records:
        csv = pd.DataFrame(records).drop(columns=["password"], errors="ignore").to_csv(index=False)
        st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
        st.download_button(
            f"⬇️  Export {label} Accounts (CSV)",
            data=csv,
            file_name=f"{label.lower().replace(' / ', '_')}_accounts.csv",
            mime="text/csv",
        )


# ─── RENDER — called from app.py ────────────────────────────────────────────

def render():
    """Render the account management page inside the connected TechVerse app."""

    _init_mgmt_state()
    _render_mgmt_header()

    if st.session_state.mgmt_page == "dashboard":
        _render_mgmt_dashboard()
    elif st.session_state.mgmt_page in ("mgmt_staff", "mgmt_students"):
        _render_management_page(st.session_state.mgmt_page)
