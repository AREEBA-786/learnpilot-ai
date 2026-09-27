import json
import os
import uuid
from datetime import datetime

CHATS_FILE = "chats.json"


def load_all_chats():
    if not os.path.exists(CHATS_FILE):
        return {}
    try:
        with open(CHATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_all_chats(chats: dict):
    with open(CHATS_FILE, "w", encoding="utf-8") as f:
        json.dump(chats, f, indent=2, ensure_ascii=False)


def create_new_session():
    session_id = str(uuid.uuid4())
    chats = load_all_chats()
    chats[session_id] = {
        "title": "New Chat",
        "created_at": datetime.now().isoformat(),
        "messages": []
    }
    save_all_chats(chats)
    return session_id


def update_session_messages(session_id, messages):
    chats = load_all_chats()
    if session_id not in chats:
        chats[session_id] = {
            "title": "New Chat",
            "created_at": datetime.now().isoformat(),
            "messages": []
        }
    chats[session_id]["messages"] = messages

    if chats[session_id]["title"] == "New Chat":
        first_user_msg = next((m["content"] for m in messages if m["role"] == "user"), None)
        if first_user_msg:
            title = first_user_msg.strip()
            chats[session_id]["title"] = title[:40] + ("..." if len(title) > 40 else "")

    save_all_chats(chats)


def delete_session(session_id):
    chats = load_all_chats()
    if session_id in chats:
        del chats[session_id]
        save_all_chats(chats)


def get_sorted_sessions():
    chats = load_all_chats()
    items = sorted(chats.items(), key=lambda x: x[1].get("created_at", ""), reverse=True)
    return items