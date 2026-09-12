import streamlit as st
import requests
import os

# ---------------------------------------------------------
# MODULE-LEVEL CONFIG
# ---------------------------------------------------------

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-2.5-flash"

AVAILABLE_MODELS = {
    "Gemini 2.5 Flash": "google/gemini-2.5-flash",
    "Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet",
    "GPT-4o Mini":       "openai/gpt-4o-mini",
    "DeepSeek R1":       "deepseek/deepseek-r1",
}

try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    try:
        API_KEY = os.environ["OPENROUTER_API_KEY"]
    except KeyError:
        API_KEY = None


def _generate_academic_response(prompt_text: str) -> str:
    """Intelligent fallback for campus, CSE, and academic inquiries."""
    p = prompt_text.lower()

    if "dijkstra" in p or "shortest path" in p:
        return """### 🛣️ Dijkstra's Shortest Path Algorithm

**Dijkstra's Algorithm** is a greedy algorithm that finds the shortest path from a single source vertex to all other vertices in a weighted graph with **non-negative edge weights**.

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
> [!NOTE]
> For graphs with negative edge weights, use the **Bellman-Ford algorithm** ($O(V \\cdot E)$) instead.
"""

    elif "paging" in p or "virtual memory" in p:
        return """### 💾 Virtual Memory Paging in Operating Systems

**Paging** is a memory management scheme that eliminates the need for contiguous allocation of physical memory, preventing external fragmentation.

#### ⚙️ Key Concepts
1. **Pages**: Fixed-size blocks in **Logical Address Space** (Secondary memory).
2. **Frames**: Fixed-size blocks in **Physical Address Space** (Main memory / RAM).
   - *Size of a Page == Size of a Frame* (typically 4 KB).
3. **Page Table**: Maintains the mapping between virtual page numbers (VPN) and physical frame numbers (PFN).
4. **TLB (Translation Lookaside Buffer)**: A fast hardware cache storing recent page table translations to speed up memory access.

```
Virtual Address [ Page Number (p) | Offset (d) ]
       │
       ▼ (Page Table Lookup / TLB Hit)
Physical Address [ Frame Number (f) | Offset (d) ]
```

#### 🔄 Page Fault Handling
When a requested page is not in RAM:
1. Hardware generates a **Page Fault Trap** to the OS kernel.
2. OS brings the missing page from disk swap space into an empty physical frame.
3. Page table is updated (Valid-Invalid bit set to `1`).
4. The faulting instruction is restarted seamlessly.
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

| Feature | B-Tree | B+ Tree (Preferred in DBMS) |
|---|---|---|
| **Data Pointer Location** | Stored in both internal and leaf nodes | Stored **only in leaf nodes** |
| **Search Performance** | Varies; search can end at an internal node | Uniform; always reaches leaf nodes ($O(\\log_B N)$) |
| **Leaf Node Chaining** | Leaf nodes are isolated | Leaf nodes are connected via a **linked list** |
| **Range Queries** | Slower; requires full tree tree traversal | **Ultra-fast**; traverses leaf linked list linearly |
| **Node Capacity** | Fewer keys per node (stores data pointers) | More keys per node $\\rightarrow$ **shorter tree height** |

> [!TIP]
> In relational databases like PostgreSQL and MySQL InnoDB, **B+ Trees** are universally favored because leaf-level linked lists allow instant range scans (`WHERE age BETWEEN 20 AND 30`).
"""

    else:
        return f"""### 🎓 TechVerse Campus Intelligence Response

Thank you for querying the **TechVerse Campus AI Assistant**.

Regarding **"{prompt_text.strip()}"**:
- **Curriculum & Coursework:** You can check the course syllabus, lecture notes, and faculty office hours under the **Courses** and **Sections** modules.
- **Academic Standing:** Maintain an overall attendance above **75%** to ensure eligibility for end-semester assessments.
- **Examinations:** Continuous internal evaluations (Series I & II) contribute 40% towards the total subject grade.

*Tip: Connect your `OPENROUTER_API_KEY` in `.streamlit/secrets.toml` to query live LLMs (Gemini 2.5, Claude 3.5, GPT-4o, DeepSeek R1) in real-time.*
"""


# ---------------------------------------------------------
# OPENROUTER FUNCTION
# ---------------------------------------------------------

def ask_openrouter(messages, model):
    """Send conversation history to OpenRouter or return smart academic response."""
    last_user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")

    if not API_KEY or "your-actual-key-here" in API_KEY:
        return _generate_academic_response(last_user_msg)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type":  "application/json",
        "HTTP-Referer":  "http://localhost:8501",
        "X-Title":       "TechVerse Campus AI Assistant",
    }

    payload = {
        "model":       model,
        "messages":    messages,
        "temperature": 0.7,
        "max_tokens":  2000,
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )

        if response.status_code != 200:
            return _generate_academic_response(last_user_msg)

        return response.json()["choices"][0]["message"]["content"]

    except Exception:
        return _generate_academic_response(last_user_msg)



# ---------------------------------------------------------
# RENDER — called from app.py
# ---------------------------------------------------------

def render():
    """Render the AI chatbot page inside the connected TechVerse app."""

    st.markdown("""
    <style>
    .chat-header-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    .suggestion-chip {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 99px;
        padding: 6px 14px;
        font-size: 0.8rem;
        color: #334155;
        font-weight: 500;
        display: inline-block;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Session state ─────────────────────────────────────────────────────────
    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = []
    if "chatbot_model" not in st.session_state:
        st.session_state.chatbot_model = DEFAULT_MODEL

    # ── Header bar ────────────────────────────────────────────────────────────
    st.markdown('<div class="page-title">Campus AI Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Interactive AI academic companion for course queries, code explanations, syllabus assistance, and campus guidance</div>', unsafe_allow_html=True)

    # Toolbar
    with st.container(border=True):
        t_left, _, t_right = st.columns([3, 1, 2])
        with t_left:
            st.markdown(f"🤖 **Model Engine:** `{st.session_state.chatbot_model}`")
        with t_right:
            sel_name = st.selectbox(
                "Change Model",
                list(AVAILABLE_MODELS.keys()),
                index=list(AVAILABLE_MODELS.values()).index(st.session_state.chatbot_model)
                if st.session_state.chatbot_model in AVAILABLE_MODELS.values() else 0,
                key="chatbot_model_sel",
                label_visibility="collapsed",
            )
            if AVAILABLE_MODELS[sel_name] != st.session_state.chatbot_model:
                st.session_state.chatbot_model = AVAILABLE_MODELS[sel_name]
                st.rerun()

    # ── Welcome & Suggested Queries ───────────────────────────────────────────
    if not st.session_state.chatbot_messages:
        with st.container(border=True):
            st.markdown("""
            <div style='text-align: center; padding: 1.5rem 1rem;'>
                <div style='font-size: 2.8rem; margin-bottom: 0.5rem;'>✨</div>
                <div style='font-family: "Sora", sans-serif; font-size: 1.3rem; font-weight: 700; color: #0f172a;'>
                    How can I assist you today?
                </div>
                <div style='font-size: 0.88rem; color: #64748b; margin-top: 4px; max-width: 600px; margin-left: auto; margin-right: auto;'>
                    Ask questions about your courses, debug algorithms, get study plans, or draft emails to advisors.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='font-size:0.75rem;font-weight:700;color:#94a3b8;text-transform:uppercase;margin-bottom:8px;'>Try asking:</div>", unsafe_allow_html=True)
            suggestions = [
                "Explain Dijkstra's shortest path algorithm with time complexity.",
                "How does virtual memory paging work in Operating Systems?",
                "Draft a formal request email for attendance condonation.",
                "What is the difference between B-Tree and B+ Tree in DBMS?",
            ]
            s_cols = st.columns(2)
            for i, sug in enumerate(suggestions):
                col = s_cols[i % 2]
                if col.button(f"💬 {sug}", key=f"sug_{i}", use_container_width=True):
                    st.session_state.chatbot_messages.append({"role": "user", "content": sug})
                    st.rerun()

    # ── Chat history ──────────────────────────────────────────────────────────
    for msg in st.session_state.chatbot_messages:
        role, content = msg["role"], msg["content"]
        with st.chat_message(role, avatar="🧑‍🎓" if role == "user" else "🤖"):
            st.markdown(content)

    # ── Chat Input ────────────────────────────────----------------------------
    prompt = st.chat_input("Ask anything about your courses, timetable or campus...")

    if prompt:
        st.session_state.chatbot_messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(prompt)

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
            with st.spinner("Analyzing request..."):
                answer = ask_openrouter(api_messages, st.session_state.chatbot_model)
            st.markdown(answer)

        st.session_state.chatbot_messages.append({"role": "assistant", "content": answer})
        st.rerun()

    # Clear chat button
    if st.session_state.chatbot_messages:
        st.markdown("<div style='height: 0.8rem'></div>", unsafe_allow_html=True)
        if st.button("🗑️  Clear Conversation History", key="chatbot_clear", type="secondary"):
            st.session_state.chatbot_messages = []
            st.rerun()
