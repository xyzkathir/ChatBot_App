from pathlib import Path
import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Mashreq Banking Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_api_key() -> str:
    env_key = os.getenv("GROK_API_KEY")
    if env_key:
        return env_key.strip()
    return ""


GROK_API_KEY = get_api_key()
GROK_MODEL = os.getenv("GROK_MODEL", "openai/gpt-oss-20b")
GROK_URL = os.getenv("GROK_URL", "https://api.groq.com/openai/v1/chat/completions")

if not GROK_URL.endswith("/chat/completions"):
    if GROK_URL.endswith("/v1"):
        GROK_URL = f"{GROK_URL}/chat/completions"
    elif GROK_URL.endswith("/openai"):
        GROK_URL = f"{GROK_URL}/v1/chat/completions"


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "banking-chatbot"}


@app.get("/")
def serve_index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/style.css")
def serve_css():
    return FileResponse(STATIC_DIR / "style.css")


@app.get("/app.js")
def serve_js():
    return FileResponse(STATIC_DIR / "app.js")


@app.post("/api/chat")
def chat_with_agent(payload: ChatRequest):
    user_message = payload.message.strip()

    if not user_message:
        return {"reply": "Please type your question so I can help you."}

    if not GROK_API_KEY:
        return {
            "reply": "The Grok API key is missing. Add it to the environment or api_key.txt before running the chatbot."
        }

    system_prompt = """
You are a helpful banking customer service assistant for a modern digital bank.

Your job:
- Answer customer banking questions clearly and professionally.
- Explain account services, debit cards, loans, payments, transfers, security, and support processes in simple language.
- Keep responses brief, friendly, and actionable.
- Never invent account balances, transaction details, or personal facts.
- If the customer asks for sensitive actions like resetting PINs, changing account details, or making transfers, recommend secure steps such as contacting the bank or using verified app channels.
- Use a calm, trustworthy tone.
"""

    request_body = {
        "model": GROK_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.4,
        "max_tokens": 350,
    }

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            GROK_URL,
            json=request_body,
            headers=headers,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()

        content = data.get("choices", [{}])[0].get("message", {}).get("content")
        if content:
            return {"reply": content.strip()}

        return {"reply": "I couldn't generate a response from the model. Please try again."}

    except requests.exceptions.RequestException as exc:
        return {
            "reply": "The banking assistant is temporarily unavailable. Please retry in a moment.",
            "error": str(exc),
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
