import requests
import streamlit as st
from datetime import datetime


import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")


st.set_page_config(
    page_title="Agentic AI Platform",
    page_icon="🤖",
    layout="wide"
)


st.markdown("""
<style>
.main-title {
    font-size: 38px;
    font-weight: 800;
}

.sub-title {
    color: #777;
    font-size: 16px;
}

.trace-box {
    padding: 10px;
    border-radius: 8px;
    background-color: #111827;
    color: #e5e7eb;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# SESSION STATE
# =========================

if "session_id" not in st.session_state:
    st.session_state.session_id = "default"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_sources" not in st.session_state:
    st.session_state.last_sources = []

if "last_trace" not in st.session_state:
    st.session_state.last_trace = []


# =========================
# BACKEND STATUS
# =========================

def backend_status():
    try:
        response = requests.get(
            f"{BACKEND_URL}/status",
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        return None

    except Exception:
        return None


# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown("## ⚙️ Control Panel")

    status = backend_status()

    if status:
        st.success("Backend Online")
        st.caption(f"Model: `{status.get('model')}`")
    else:
        st.error("Backend Offline")

    st.divider()

    st.session_state.session_id = st.text_input(
        "Session ID",
        value=st.session_state.session_id
    )

    st.caption("Use different session IDs for different conversations.")

    st.divider()

    st.markdown("### 📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Upload PDF document",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.info(f"Selected: {uploaded_file.name}")

        if st.button("Upload PDF", use_container_width=True):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            with st.spinner("Uploading PDF..."):

                response = requests.post(
                    f"{BACKEND_URL}/upload-pdf",
                    files=files
                )

            if response.status_code == 200:

                st.success("PDF uploaded successfully")

                st.json(response.json())

            else:

                st.error("Upload failed")

                st.text(response.text)

    st.divider()

    st.markdown("### 🧹 Actions")

    if st.button("Clear Chat UI", use_container_width=True):

        st.session_state.messages = []
        st.session_state.last_sources = []
        st.session_state.last_trace = []

        st.rerun()

    if st.button("Clear Session Memory", use_container_width=True):

        response = requests.post(
            f"{BACKEND_URL}/clear-memory/{st.session_state.session_id}"
        )

        if response.status_code == 200:
            st.success("Session memory cleared")
        else:
            st.error("Could not clear memory")

    if st.button("Clear Uploaded Documents", use_container_width=True):

        response = requests.delete(
            f"{BACKEND_URL}/clear-documents"
        )

        if response.status_code == 200:
            st.success("Documents cleared")
        else:
            st.error("Could not clear documents")


# =========================
# HEADER
# =========================

st.markdown(
    '<div class="main-title">🤖 Agentic AI Platform</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Multi-agent AI with RAG, tools, SQL, memory, and web search.</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================
# METRICS
# =========================

status = backend_status()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Backend",
        "Online" if status else "Offline"
    )

with col2:
    st.metric(
        "Model",
        status.get("model", "N/A") if status else "N/A"
    )

with col3:
    st.metric(
        "Messages",
        len(st.session_state.messages)
    )

with col4:
    st.metric(
        "Session",
        st.session_state.session_id
    )


# =========================
# TABS
# =========================

tab_chat, tab_sources, tab_trace, tab_tools = st.tabs([
    "💬 Chat",
    "📚 Sources",
    "🧠 Agent Trace",
    "🛠 Tools"
])


# =========================
# CHAT TAB
# =========================

with tab_chat:

    st.markdown("### Chat with your Agent")

    chat_container = st.container()

    with chat_container:

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):

                st.write(message["content"])

    user_input = st.chat_input(
        "Ask about PDFs, search the web, run SQL, calculate, or execute Python..."
    )

    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "time": datetime.now().strftime("%H:%M:%S")
        })

        payload = {
            "question": user_input,
            "session_id": st.session_state.session_id
        }

        with st.spinner("Agent is thinking..."):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json=payload,
                    timeout=300
                )

                if response.status_code == 200:

                    data = response.json()

                    answer = data.get("response", "")
                    sources = data.get("sources", [])
                    trace = data.get("trace", [])

                    st.session_state.last_sources = sources
                    st.session_state.last_trace = trace

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                        "trace": trace,
                        "time": datetime.now().strftime("%H:%M:%S")
                    })

                    st.rerun()

                else:

                    st.error("Backend returned an error")

                    st.text(response.text)

            except Exception as e:

                st.error(f"Request failed: {e}")


# =========================
# SOURCES TAB
# =========================

with tab_sources:

    st.markdown("### Retrieved Sources")

    if not st.session_state.last_sources:

        st.info("No sources available yet.")

    else:

        for idx, source in enumerate(
            st.session_state.last_sources,
            start=1
        ):

            st.markdown(f"#### Source {idx}")

            title = source.get("source", "Unknown source")

            url = source.get("url")

            preview = source.get("preview", "")

            if url:
                st.markdown(f"**[{title}]({url})**")
            else:
                st.markdown(f"**{title}**")

            st.write(preview)

            st.divider()


# =========================
# TRACE TAB
# =========================

with tab_trace:

    st.markdown("### Agent Execution Trace")

    if not st.session_state.last_trace:

        st.info("No trace available yet.")

    else:

        for step in st.session_state.last_trace:

            st.markdown(
                f"<div class='trace-box'>✅ {step}</div>",
                unsafe_allow_html=True
            )


# =========================
# TOOLS TAB
# =========================

with tab_tools:

    st.markdown("### Available Tools")

    tools = [
        ("🧮 Calculator", "Handles arithmetic calculations."),
        ("🐍 Python Tool", "Executes Python snippets."),
        ("🌐 Web Search", "Searches the internet."),
        ("🗄 SQL Tool", "Queries SQLite database."),
        ("📄 PDF RAG", "Answers questions from uploaded PDFs."),
        ("🧠 Session Memory", "Remembers conversations."),
        ("📌 Source Tracking", "Shows retrieval sources."),
        ("🧭 Agent Trace", "Shows agent workflow.")
    ]

    for name, desc in tools:

        st.markdown(f"**{name}**")

        st.caption(desc)

        st.divider()


# =========================
# FOOTER
# =========================

st.caption(
    "Built with FastAPI, LangGraph, Ollama, FAISS, Streamlit, and multi-agent tooling."
)
