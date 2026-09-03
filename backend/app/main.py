import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel

from .memory import add_message, get_history, clear_memory

load_dotenv()

app = FastAPI(
    title="ECHO AI",
    version="0.2.0"
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "status": "online",
        "assistant": "ECHO AI",
        "version": "0.2.0"
    }


@app.get("/memory")
def memory():
    return {
        "messages": get_history()
    }


@app.delete("/memory")
def delete_memory():
    clear_memory()
    return {
        "cleared": True
    }


@app.post("/chat")
def chat(request: ChatRequest):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not configured."
        )

    add_message("user", request.message)

    history = get_history()

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="gpt-5-mini",
            instructions=(
                "You are ECHO, a personal AI assistant. "
                "Be natural, friendly, conversational, and helpful. "
                "Use the conversation history when appropriate."
            ),
            input=history
        )

        reply = response.output_text

        add_message("assistant", reply)

        return {
            "response": reply
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
