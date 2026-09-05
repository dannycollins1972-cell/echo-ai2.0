import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel

from .conversation import build_context
from .memory import (
    add_saved_memory,
    clear_memory,
    forget_memory,
    get_history,
    get_saved_memories,
)
from .personality import get_personality

load_dotenv()

app = FastAPI(
    title="ECHO AI",
    version="0.4.0",
)


class ChatRequest(BaseModel):
    message: str


class MemoryRequest(BaseModel):
    content: str


@app.get("/")
def home():
    return {
        "status": "online",
        "assistant": "ECHO AI",
        "version": "0.4.0",
    }


@app.get("/memory")
def memory():
    return {
        "messages": get_history(),
    }


@app.get("/memory/saved")
def saved_memories():
    return {
        "memories": get_saved_memories(),
    }


@app.post("/memory/save")
def save_memory(request: MemoryRequest):
    content = request.content.strip()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Memory content cannot be empty.",
        )

    add_saved_memory(content)

    return {
        "saved": True,
        "memory": content,
    }


@app.delete("/memory/saved")
def forget_saved_memory(request: MemoryRequest):
    content = request.content.strip()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Memory content cannot be empty.",
        )

    removed = forget_memory(content)

    return {
        "forgotten": removed,
    }


@app.delete("/memory")
def delete_all_memory():
    clear_memory()

    return {
        "cleared": True,
    }


@app.post("/chat")
def chat(request: ChatRequest):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not configured.",
        )

    history = build_context(request.message)
    personality = get_personality()

    instructions = (
        f"You are {personality['name']}, a personal AI assistant. "
        f"Use a {personality['tone']} tone and a "
        f"{personality['style']} style. "
        "Be natural, conversational, friendly, and helpful. "
        "Do not claim to be human. "
        "Use conversation history when appropriate."
    )

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="gpt-5-mini",
            instructions=instructions,
            input=history,
        )

        reply = response.output_text

        from .memory import add_message

        add_message("assistant", reply)

        return {
            "response": reply,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )
