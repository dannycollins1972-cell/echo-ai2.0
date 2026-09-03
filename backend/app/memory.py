import json
from pathlib import Path

MEMORY_FILE = Path("memory.json")


def load_memory():
    if not MEMORY_FILE.exists():
        return []

    try:
        return json.loads(MEMORY_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return []


def save_memory(memory):
    MEMORY_FILE.write_text(json.dumps(memory, indent=2))


def add_message(role, content):
    memory = load_memory()

    memory.append({
        "role": role,
        "content": content
    })

    save_memory(memory)


def get_history():
    return load_memory()


def clear_memory():
    save_memory([])
