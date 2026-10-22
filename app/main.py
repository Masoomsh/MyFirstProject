import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI, OpenAIError
from pydantic import BaseModel

# override=True so values in .env win over stale variables already set in the shell
load_dotenv(override=True)

LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL", "http://localhost:4000")
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY", "sk-anything")
LITELLM_MODEL = os.getenv("LITELLM_MODEL", "ollama-llama3.2")

# The LiteLLM proxy exposes an OpenAI-compatible API, so the OpenAI SDK talks to it directly.
client = OpenAI(base_url=LITELLM_BASE_URL, api_key=LITELLM_API_KEY, timeout=120)

app = FastAPI(title="My FastAPI Application")


class ChatRequest(BaseModel):
    prompt: str
    model: str | None = None


def ask_llm(prompt: str, model: str | None = None) -> str:
    try:
        completion = client.chat.completions.create(
            model=model or LITELLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
    except OpenAIError as e:
        raise HTTPException(status_code=502, detail=f"LiteLLM request failed: {e}")
    return completion.choices[0].message.content


@app.get("/")
def home():
    return {"message": "Welcome to My FastAPI Application!"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/response")
def response():
    return {"message": ask_llm("How is the weather today ")}


@app.post("/chat")
def chat(request: ChatRequest):
    model = request.model or LITELLM_MODEL
    return {"model": model, "message": ask_llm(request.prompt, model)}
