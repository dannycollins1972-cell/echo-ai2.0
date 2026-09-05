from .memory import add_message, get_history


def build_context(user_message: str) -> list[dict]:
    """
    Add the user's message to local conversation history
    and return the current conversation context.
    """
    add_message("user", user_message)
    return get_history()
