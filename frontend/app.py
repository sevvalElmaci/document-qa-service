from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import streamlit as st
from PIL import Image

# Config
# Config
DEFAULT_API_BASE = "http://localhost:8000/api/v1"

try:
    API_BASE = st.secrets["API_BASE"]
except Exception:
    API_BASE = DEFAULT_API_BASE

API_BASE = st.sidebar.text_input("API Base URL", value=API_BASE)  # debug override

UPLOAD_URL = f"{API_BASE}/upload"
ASK_URL = f"{API_BASE}/ask"
REQUEST_TIMEOUT_SEC = 180


APP_TITLE = "Document QA Service (Local RAG)"
APP_SUBTITLE = "Study case implementation • FastAPI + FAISS + SentenceTransformer + Ollama (llama3)"

LOGO_PATH = Path(__file__).parent / "assets" / "company_logo.jpg"
st.set_page_config(
    page_title="Document QA (Local RAG)",
    page_icon="🧠",
    layout="wide",
)



def load_logo(path: Path) -> Optional[Image.Image]:
    try:
        if path.exists():
            return Image.open(path)
    except Exception:
        return None
    return None


def request_json(
    method: str,
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    json_body: Optional[Dict[str, Any]] = None,
    files: Optional[Dict[str, Any]] = None,
    timeout: int = REQUEST_TIMEOUT_SEC,
) -> Dict[str, Any]:

    try:
        resp = requests.request(
            method=method,
            url=url,
            params=params,
            json=json_body,
            files=files,
            timeout=timeout,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        # Streamlit-friendly error
        raise RuntimeError(f"Request failed: {e}") from e
    except ValueError as e:
        raise RuntimeError("Response is not valid JSON.") from e


def post_upload(file_bytes: bytes, filename: str, mode: str) -> Dict[str, Any]:
    files = {"file": (filename, file_bytes, "text/plain")}
    params = {"mode": mode}
    return request_json("POST", UPLOAD_URL, params=params, files=files)


def post_ask(doc_id: str, question: str, top_k: int) -> Dict[str, Any]:
    payload = {"doc_id": doc_id, "question": question, "top_k": top_k}
    return request_json("POST", ASK_URL, json_body=payload)


def render_sources(sources: List[Dict[str, Any]]) -> None:
    st.subheader("📌 Sources (retrieved chunks)")

    if not sources:
        st.info("No sources found.")
        return

    sources_sorted = sorted(sources, key=lambda x: x.get("relevance", 0.0), reverse=True)

    for i, src in enumerate(sources_sorted, start=1):
        file_ = src.get("file", "unknown")
        relevance = float(src.get("relevance", 0.0))
        chunk = src.get("chunk", "")

        with st.expander(f"Source #{i} | relevance={relevance:.3f} | file={file_}"):
            st.code(chunk, language="markdown")


def init_state() -> None:
    st.session_state.setdefault("doc_id", None)
    st.session_state.setdefault("mode", "fast")
    st.session_state.setdefault("upload_info", None)
    st.session_state.setdefault("history", [])  # list[dict]



init_state()


logo = load_logo(LOGO_PATH)

hcol1, hcol2 = st.columns([1, 8], vertical_alignment="center")
with hcol1:
    if logo:
        st.image(logo, width=56)
    else:
        st.write("")
with hcol2:
    st.markdown(
        f"""
        <div style="display:flex; flex-direction:column; gap:2px;">
            <div style="font-size:40px; font-weight:800; line-height:1.1;">{APP_TITLE}</div>
            <div style="opacity:0.7; font-size:14px;">{APP_SUBTITLE}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

left, right = st.columns([1, 2], gap="large")

# Left Side
with left:
    st.header("1) Upload Document")

    mode = st.radio(
        "Mode",
        ["fast", "long"],
        index=0 if st.session_state.mode == "fast" else 1,
        horizontal=False,
    )
    st.session_state.mode = mode

    uploaded = st.file_uploader("Select a TXT file", type=["txt"])

    upload_clicked = st.button(
        "📤 Upload & Index",
        use_container_width=True,
        disabled=(uploaded is None),
    )

    if upload_clicked and uploaded is not None:
        try:
            resp = post_upload(
                file_bytes=uploaded.getvalue(),
                filename=uploaded.name,
                mode=mode,
            )
            st.session_state.doc_id = resp.get("doc_id")
            st.session_state.upload_info = resp
            st.success("✅ Uploaded & indexed successfully!")
        except Exception as e:
            st.error(f"❌ Upload failed: {e}")

    st.divider()

    st.header("2) Settings")
    top_k = st.slider("Top-K (how many chunks to retrieve?)", 1, 8, 3)

    if st.session_state.upload_info:
        st.subheader("📄 Upload Info")
        st.json(st.session_state.upload_info)

    st.divider()

    st.header("3) Quick Check")
    st.write("Doc ID:")
    st.code(st.session_state.doc_id or "(not uploaded yet)")

    if st.button("🧹 Clear chat", use_container_width=True):
        st.session_state.history = []
        st.toast("Chat cleared.")

# Right Side
with right:
    st.header("Question & Answer")

    if not st.session_state.doc_id:
        st.info("Please upload a TXT file on the left to start asking questions.")
    else:
        question = st.text_input("Ask a question", placeholder="e.g., What is git version control?")
        ask_clicked = st.button(
            "🤖 Ask",
            type="primary",
            use_container_width=True,
            disabled=(not question.strip()),
        )

        if ask_clicked:
            try:
                with st.spinner("Thinking..."):
                    resp = post_ask(
                        doc_id=st.session_state.doc_id,
                        question=question.strip(),
                        top_k=top_k,
                    )

                st.session_state.history.append(
                    {
                        "q": resp.get("question", question),
                        "a": resp.get("answer", ""),
                        "sources": resp.get("sources", []),
                        "confidence": resp.get("confidence", "unknown"),
                    }
                )
                st.toast("✅ Answer received!")
            except Exception as e:
                st.error(f"❌ Ask failed: {e}")

        if st.session_state.history:
            for n, item in enumerate(reversed(st.session_state.history), start=1):
                st.markdown(f"### 🗨️ Question #{len(st.session_state.history) - n + 1}")
                st.write(item["q"])

                st.markdown("### ✅ Answer")
                st.success(item["a"] or "(empty answer)")

                st.caption(f"Confidence: **{item.get('confidence', 'unknown')}**")
                render_sources(item.get("sources", []))
                st.divider()
        else:
            st.write("No questions asked yet.")
