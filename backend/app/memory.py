import json
from pathlib import Path

MEMORY_FILE = Path(__file__).resolve().parent.parent / "memory.json"


def load_memory() -> list[dict]:
    if not MEMORY_FILE.exists():
        return []

    try:
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_memory(memory: list[dict]) -> None:
    MEMORY_FILE.write_text(
        json.dumps(memory, indent=2),
        encoding="utf-8",
    )


def add_message(role: str, content: str) -> None:
    memory = load_memory()

    memory.append({
        "type": "conversation",
        "role": role,
        "content": content,
    })

    save_memory(memory)


def add_saved_memory(content: str) -> None:
    memory = load_memory()

    memory.append({
        "type": "saved_memory",
        "content": content,
    })

    save_memory(memory)


def get_history() -> list[dict]:
    return [
        item for item in load_memory()
        if item.get("type") == "conversation"
    ]


def get_saved_memories() -> list[dict]:
    return [
        item for item in load_memory()
        if item.get("type") == "saved_memory"
    ]


def forget_memory(content: str) -> bool:
    memory = load_memory()
    target = content.strip().lower()

    filtered = [
        item for item in memory
        if not (
            item.get("type") == "saved_memory"
            and item.get("content", "").strip().lower() == target
        )
    ]

    changed = len(filtered) != len(memory)

    if changed:
        save_memory(filtered)

    return changed


def clear_memory() -> None:
    save_memory([])
