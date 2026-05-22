import json
import os

from app.core.config import MEMORY_FILE


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_memory(memory):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)


def add_to_memory(session_id: str, role: str, content: str):
    memory = load_memory()

    if session_id not in memory:
        memory[session_id] = []

    memory[session_id].append({
        "role": role,
        "content": content
    })

    if len(memory[session_id]) > 10:
        memory[session_id] = memory[session_id][-10:]

    save_memory(memory)


def get_memory(session_id: str):
    memory = load_memory()
    return memory.get(session_id, [])


def format_memory(session_id: str):
    messages = get_memory(session_id)

    if not messages:
        return ""

    return "\n".join([
        f"{item['role']}: {item['content']}"
        for item in messages
    ])


def clear_memory(session_id: str):
    memory = load_memory()
    memory[session_id] = []
    save_memory(memory)
