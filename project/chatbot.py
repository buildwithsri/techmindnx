import streamlit as st
import requests
import os
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# MODULE CONFIG & MODEL MAPPINGS
# ─────────────────────────────────────────────────────────────────────────────

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-2.5-flash"

AVAILABLE_MODELS = {
    "Gemini 2.5 Flash":    "google/gemini-2.5-flash",
    "GPT-4o Mini":          "openai/gpt-4o-mini",
    "DeepSeek Chat (V3)":   "deepseek/deepseek-chat",
    "Llama 3.3 70B":        "meta-llama/llama-3.3-70b-instruct",
    "Claude 3 Haiku":       "anthropic/claude-3-haiku",
}

def _get_api_key():
    """Retrieve API key from streamlit secrets, os environ, or local config."""
    try:
        if "OPENROUTER_API_KEY" in st.secrets:
            return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        pass
    return os.environ.get("OPENROUTER_API_KEY", None)


# ─────────────────────────────────────────────────────────────────────────────
# SMART CAMPUS KNOWLEDGE FALLBACK
# ─────────────────────────────────────────────────────────────────────────────

def _generate_academic_response(prompt_text: str) -> str:
    """Intelligent fallback for campus, CSE, and academic inquiries."""
    p = prompt_text.lower()

    if "dijkstra" in p or "shortest path" in p:
        return """### 🛣️ Dijkstra's Shortest Path Algorithm

**Dijkstra's Algorithm** is a greedy algorithm that computes the shortest path from a single source vertex to all other vertices in a weighted graph with **non-negative edge weights**.

#### ⚡ Time & Space Complexity
| Metric | Adjacency Matrix | Min-Heap / Priority Queue |
|---|---|---|
| **Time Complexity** | $O(V^2)$ | **$O((V + E) \\log V)$** |
| **Space Complexity** | $O(V)$ | **$O(V + E)$** |

#### 💻 Python Implementation
```python
import heapq

def dijkstra(graph, start):
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_distance, current_vertex = heapq.heappop(pq)
        
        if current_distance > distances[current_vertex]:
            continue
            
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    return distances
```
> **Note:** For graphs containing negative edge weights, use the **Bellman-Ford algorithm** ($O(V \\cdot E)$) instead.
"""

    elif "paging" in p or "virtual memory" in p:
        return """### 💾 Virtual Memory Paging in Operating Systems

**Paging** is a memory management scheme that eliminates the need for contiguous allocation of physical memory, preventing external fragmentation.

#### ⚙️ Key Concepts
1. **Pages**: Fixed-size blocks in **Logical Address Space** (Secondary memory).
2. **Frames**: Fixed-size blocks in **Physical Address Space** (Main memory / RAM).
   - *Size of a Page == Size of a Frame* (typically 4 KB).
3. **Page Table**: Maintains the mapping between virtual page numbers (VPN) and physical frame numbers (PFN).
4. **TLB (Translation Lookaside Buffer)**: A fast hardware associative cache storing recent page table translations.

```
Virtual Address [ Page Number (p) | Offset (d) ]
       │
       ▼ (Page Table Lookup / TLB Hit)
Physical Address [ Frame Number (f) | Offset (d) ]
```

#### 🔄 Page Fault Sequence
When a requested page is not in RAM:
1. Hardware issues a **Page Fault Trap** to the OS.
2. OS kernel fetches the missing page from swap space into a free frame.
3. Page table is updated (Valid-Invalid bit set to `1`).
4. The faulting CPU instruction is restarted.
"""

    elif "attendance" in p or "condonation" in p or "draft" in p or "email" in p:
        return """### ✉️ Formal Email: Attendance Condonation Request

**Subject:** Request for Attendance Condonation — [Your Full Name] (Reg No: [TVE22CS001])

---

**Respected Head of the Department,**

I am writing to formally request attendance condonation for the current academic semester (**Even Semester 2025–26**) in the Department of Computer Science & Engineering.

Due to unforeseen medical circumstances / official university representation during **[Date Range]**, I was unable to attend regular lectures for the following course(s):
- **CS303:** Database Management Systems
- **CS302:** Operating Systems

I have attached the verified medical certificates, hospital discharge summaries, and duty leave approval slips for your kind perusal. I have also completed all internal continuous assessments and submitted the assigned laboratory coursework.

I kindly request you to consider my application and grant permission to appear for the upcoming End-Semester University Examinations.

Thank you for your consideration.

Sincerely,  
**[Your Full Name]**  
Roll No / Reg: TVE22CS001  
Semester: S6 · Section: CSE-A  
TechVerse Engineering College
"""

    elif "b-tree" in p or "b+ tree" in p or "dbms" in p:
        return """### 🌳 Difference Between B-Tree and B+ Tree

Both **B-Tree** and **B+ Tree** are self-balancing multi-way search trees heavily used in database indexing and file systems.

| Feature | B-Tree | B+ Tree (Standard in DBMS) |
|---|---|---|
| **Data Pointer Location** | Stored in both internal and leaf nodes | Stored **only in leaf nodes** |
| **Search Performance** | Variable; search can end at an internal node | Uniform; always reaches leaf nodes ($O(\\log_B N)$) |
| **Leaf Node Chaining** | Leaf nodes are isolated | Leaf nodes are connected via a **doubly linked list** |
| **Range Queries** | Slower; requires full tree traversal | **Ultra-fast**; traverses leaf linked list linearly |
| **Node Key Capacity** | Lower (stores record pointers in internal nodes) | Higher $\\rightarrow$ **shorter tree height & fewer I/Os** |

> In databases like PostgreSQL and MySQL InnoDB, **B+ Trees** are universally favored because leaf linked lists enable rapid range scans (`WHERE score BETWEEN 80 AND 100`).
"""

    else:
        return f"""### 🎓 TechVerse Campus Intelligence Response

Thank you for querying the **TechVerse Campus AI Assistant**.

Regarding **"{prompt_text.strip()}"**:
- **Curriculum & Syllabi:** Course structures, lecture credits, and faculty allocations are available under the **Courses** and **Sections** modules.
- **Academic Standing:** Maintain an overall attendance above **75%** to ensure eligibility for end-semester university examinations.
- **Continuous Evaluation:** Internal tests (Series I & II) and laboratory assessments contribute to internal scoring.
"""


# ─────────────────────────────────────────────────────────────────────────────
# OPENROUTER INVOCATION
# ─────────────────────────────────────────────────────────────────────────────

def ask_openrouter(messages, model):
    """Send conversation history to OpenRouter or return smart fallback."""
    api_key = _get_api_key()
    last_user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")

    if not api_key or "your-actual-key-here" in api_key:
        return _generate_academic_response(last_user_msg)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type":  "application/json",
        "HTTP-Referer":  "http://localhost:8501",
        "X-Title":       "TechVerse Campus AI Assistant",
    }

    payload = {
        "model":       model,
        "messages":    messages,
        "temperature": 0.7,
        "max_tokens":  1000,
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=40,
        )

        if response.status_code == 200:
            res_json = response.json()
            return res_json["choices"][0]["message"]["content"]
        else:
            return _generate_academic_response(last_user_msg)

    except Exception:
        return _generate_academic_response(last_user_msg)


# ─────────────────────────────────────────────────────────────────────────────
# RENDER FUNCTION (CALLED FROM app.py)
# ─────────────────────────────────────────────────────────────────────────────

def render():
    """Render the state-of-the-art AI Assistant portal."""

    # ── Session State Initialisation ──────────────────────────────────────────
    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = []
    if "chatbot_model" not in st.session_state:
        st.session_state.chatbot_model = DEFAULT_MODEL

    api_key = _get_api_key()
    is_live = bool(api_key and "your-actual-key-here" not in api_key)

    # ── Header & Control Toolbar ──────────────────────────────────────────────
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.2rem; flex-wrap: wrap; gap: 1rem;">
        <div>
            <div class="page-title" style="display: flex; align-items: center; gap: 10px;">
                <span>Campus AI Assistant</span>
                <span class="badge badge-blue" style="font-size: 0.72rem; vertical-align: middle;">v3.1 Pro</span>
            </div>
            <div class="page-subtitle" style="margin-bottom: 0;">
                Academic companion for course queries, code debugging, syllabus guidance, and exam preparation
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Modern Control Bar ────────────────────────────────────────────────────
    with st.container(border=True):
        col_info, col_model, col_clear = st.columns([3.2, 2.2, 1.2])

        with col_info:
            if is_live:
                st.markdown("""
                <div style="display: flex; align-items: center; gap: 8px; padding-top: 6px;">
                    <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #16a34a; box-shadow: 0 0 8px rgba(22, 163, 74, 0.6);"></span>
                    <span style="font-size: 0.86rem; font-weight: 700; color: #15803d;">Live OpenRouter AI Connected</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="display: flex; align-items: center; gap: 8px; padding-top: 6px;">
                    <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #d97706;"></span>
                    <span style="font-size: 0.86rem; font-weight: 700; color: #b45309;">Campus Knowledge Engine Active</span>
                </div>
                """, unsafe_allow_html=True)

        with col_model:
            selected_model_name = st.selectbox(
                "Select Model",
                list(AVAILABLE_MODELS.keys()),
                index=list(AVAILABLE_MODELS.values()).index(st.session_state.chatbot_model)
                if st.session_state.chatbot_model in AVAILABLE_MODELS.values() else 0,
                key="chatbot_model_picker",
                label_visibility="collapsed",
            )
            target_model = AVAILABLE_MODELS[selected_model_name]
            if target_model != st.session_state.chatbot_model:
                st.session_state.chatbot_model = target_model
                st.rerun()

        with col_clear:
            if st.button("🗑️ Clear", use_container_width=True, key="chatbot_clear_btn", help="Clear conversation history"):
                st.session_state.chatbot_messages = []
                st.rerun()

    # ── Welcome & Interactive Suggestion Cards (When Chat is Empty) ───────────
    if not st.session_state.chatbot_messages:
        st.markdown("""
        <div style='text-align: center; padding: 2rem 1rem 1.5rem;'>
            <div style='display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px;
                        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
                        border: 1px solid #bfdbfe; border-radius: 20px; font-size: 2.2rem; margin-bottom: 0.8rem;
                        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.12);'>
                ✨
            </div>
            <div style='font-family: "Sora", sans-serif; font-size: 1.4rem; font-weight: 800; color: #0f172a; letter-spacing: -0.02em;'>
                How can I assist you today?
            </div>
            <div style='font-size: 0.9rem; color: #64748b; margin-top: 4px; max-width: 580px; margin-left: auto; margin-right: auto;'>
                Ask anything about courses, debug algorithms, study plans, or draft emails.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='font-size: 0.74rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.8rem;'>Recommended Topics</div>", unsafe_allow_html=True)

        cards = [
            ("🛣️ Algorithms", "Explain Dijkstra's shortest path algorithm with time complexity & Python code.", 0),
            ("💾 Operating Systems", "How does virtual memory paging and TLB cache translation work?", 1),
            ("✉️ Academic Email", "Draft a formal email to HOD requesting attendance condonation.", 2),
            ("🌳 Database Indexing", "What is the difference between B-Tree and B+ Tree in DBMS?", 3),
        ]

        c1, c2 = st.columns(2, gap="medium")
        for title, prompt_text, idx in cards:
            col = c1 if idx % 2 == 0 else c2
            with col:
                with st.container(border=True):
                    st.markdown(f"<div style='font-weight: 700; color: #0f172a; font-size: 0.95rem; margin-bottom: 4px;'>{title}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: #64748b; font-size: 0.82rem; margin-bottom: 10px; line-height: 1.4;'>{prompt_text}</div>", unsafe_allow_html=True)
                    if st.button("Ask this  →", key=f"rec_card_{idx}", use_container_width=True):
                        st.session_state.chatbot_messages.append({"role": "user", "content": prompt_text})
                        st.rerun()

    # ── Chat Messages Stream ──────────────────────────────────────────────────
    for msg in st.session_state.chatbot_messages:
        role = msg["role"]
        content = msg["content"]
        avatar = "🧑‍🎓" if role == "user" else "🤖"
        with st.chat_message(role, avatar=avatar):
            st.markdown(content)

    # ── Chat Input ────────────────────────────────────────────────────────────
    user_query = st.chat_input("Ask anything about your courses, timetable, code or campus...")

    if user_query:
        st.session_state.chatbot_messages.append({"role": "user", "content": user_query})

        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(user_query)

        api_messages = [
            {
                "role": "system",
                "content": (
                    "You are the official TechVerse Smart Campus AI Assistant. "
                    "Provide clear, academically rigorous, structured, and helpful responses. "
                    "Format code and mathematical formulas nicely with Markdown."
                ),
            }
        ] + st.session_state.chatbot_messages

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🧠 Analyzing request and synthesizing response..."):
                reply = ask_openrouter(api_messages, st.session_state.chatbot_model)
            st.markdown(reply)

        st.session_state.chatbot_messages.append({"role": "assistant", "content": reply})
        st.rerun()
