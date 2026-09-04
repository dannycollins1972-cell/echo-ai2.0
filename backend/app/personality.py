DEFAULT_PERSONALITY = {
    "name": "ECHO",
    "tone": "friendly",
    "style": "natural",
    "verbosity": "adaptive",
    "be_conversational": True,
    "ask_before_memory": True,
}


def get_personality():
    return DEFAULT_PERSONALITY.copy()
