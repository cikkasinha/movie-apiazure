# routes_chat.py

import os
import time
import json
import requests
from flask import request, jsonify

# 🌐 Ollama model config
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")
MAX_TURNS = 8
SESSIONS = {}

# 🧠 System prompt to guide chat behavior
SYSTEM_PROMPT = """You are a helpful movie assistant for an API that serves:
- /genres
- /movies-by-genre?genre_id=...
- /recommend-ai?title=...
Remember previous user messages and respond naturally."""

# 🗂 Session management
def _get_session(session_id):
    history = SESSIONS.get(session_id, [])
    if not history or history[0].get("role") != "system":
        history = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    return history

def _save_session(session_id, history):
    trimmed = [history[0]]  # keep system prompt
    tail = history[1:][-2 * MAX_TURNS:]  # recent turns only
    trimmed.extend(tail)
    SESSIONS[session_id] = trimmed

# 🔌 Call Ollama API with conversation
def _ollama_chat(messages):
    url = f"{OLLAMA_HOST}/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    }
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    # ✅ Support both new-style and legacy response formats
    return data.get("message", {}).get("content", "") or data.get("response", "")

# 🎯 Register chatbot route
def register_chat_routes(app):

    @app.route("/chat", methods=["POST"])
    def chat():
        body = request.get_json(force=True, silent=True) or {}
        session_id = body.get("session_id") or request.remote_addr or str(int(time.time()))

        # 🔄 Accept multiple keys: message, prompt, or input
        user_msg = (body.get("message") or body.get("prompt") or body.get("input") or "").strip()
        if not user_msg:
            return jsonify({"error": "message (or prompt) is required"}), 400

        history = _get_session(session_id)
        history.append({ "role": "user", "content": user_msg })

        try:
            reply = _ollama_chat(history).strip()
            history.append({ "role": "assistant", "content": reply })
            _save_session(session_id, history)

            # 🧼 Return both keys for frontend compatibility
            return jsonify({
                "session_id": session_id,
                "response": reply,
                "reply": reply
            })

        except Exception as e:
            return jsonify({ "error": str(e) }), 500
