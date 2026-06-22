import asyncio
import json
import httpx
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field

FORBIDDEN_SEQUENCES = ["4111111111111111", "SECRETKEY"]
PHRASE_MAX_WINDOW = 32
MAX_PADDING = 2
UPSTREAM_LLM_URL = "http://localhost:8001/upstream"  # Change as needed

class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2048)
    class Config:
        extra = "forbid"

async def app_lifespan(app: FastAPI):
    app.state.is_ready = True
    yield
    app.state.is_ready = False

def create_app():
    app = FastAPI(lifespan=app_lifespan)
    app.state.is_ready = False

    @app.middleware("http")
    async def readiness_guard(request: Request, call_next):
        if not getattr(app.state, "is_ready", False):
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"error": "Service not ready."}
            )
        return await call_next(request)

    @app.post("/proxy")
    async def proxy_endpoint(request: Request, body: PromptRequest):
        session_id = str(request.client)
        async def stream_tokens():
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    # Replace 'body.model_dump()' if using Pydantic v1 - use 'body.dict()'
                    async with client.stream("POST", UPSTREAM_LLM_URL, json=body.model_dump()) as upstream:
                        async for line in upstream.aiter_lines():
                            if not line.startswith("data:"):
                                continue
                            try:
                                chunk_json = line.split("data:", 1)[1].strip()
                                chunk_data = json.loads(chunk_json)
                            except Exception:
                                continue
                            chunk_text = chunk_data.get("text")
                            if not chunk_text:
                                continue
                            # Simple forbidden sequence check per chunk
                            t = ''.join([c.lower() for c in chunk_text if c.isalnum()])
                            for seq in FORBIDDEN_SEQUENCES:
                                s = ''.join([c.lower() for c in seq if c.isalnum()])
                                if s in t:
                                    yield "[BLOCKED — SENSITIVE DATA LEAK FLAGGED]"
                                    return
                            yield chunk_text
            except Exception as e:
                yield f"[Proxy Error: {e}]"
        return StreamingResponse(stream_tokens())
    return app

app = create_app()
