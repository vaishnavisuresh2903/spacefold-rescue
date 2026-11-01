import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="SpaceFold Rescue — Meta Model API Backend Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

META_API_URL = os.getenv("META_MODEL_API_URL", "https://api.llama.com/v1/chat/completions")
META_API_KEY = os.getenv("META_MODEL_API_KEY", "")
META_MODEL_NAME = os.getenv("META_MODEL_NAME", "muse-spark-1.3")

SYSTEM_PROMPT = """
You are the kinematic fault-recovery reasoning assistant for SpaceFold Rescue (Team ORIGENIX).
You receive the current joint angles, locked hinge states, joint limits, and movement dependencies of a 3D folding structure.
Rules:
1. Never propose moving a hinge marked as locked=true.
2. Only propose movements using remaining independently movable hinges within their [min_deg, max_deg] limits.
3. The deterministic simulator will verify your proposed sequence against joint limits and 3D panel collisions before execution.
4. Return strict JSON with keys:
   - fault_summary (string)
   - recovery_possible (boolean)
   - proposed_sequence (list of objects with keys: hinge_id (string), target_deg (float), reason (string))
   - operator_explanation (string)
"""

class HingeState(BaseModel):
    hinge_id: str
    current_deg: float
    min_deg: float
    max_deg: float
    locked: bool
    dependencies: List[str] = []

class TelemetryPayload(BaseModel):
    structure_id: str
    hinges: List[HingeState]
    simulator_feedback: str = ""

@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {
        "status": "ok",
        "configured_model": META_MODEL_NAME,
        "api_key_configured": str(bool(META_API_KEY))
    }

@app.post("/api/recover")
async def analyze_fault(payload: TelemetryPayload) -> Dict[str, Any]:
    if not META_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="META_MODEL_API_KEY is not set. Configure META_MODEL_API_KEY to enable live Meta Model API analysis."
        )

    headers = {
        "Authorization": f"Bearer {META_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": META_MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": payload.model_dump_json()}
        ],
        "temperature": 0.1,
        "response_format": {"type": "json_object"}
    }

    async with httpx.AsyncClient(timeout=25.0) as client:
        response = await client.post(META_API_URL, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        parsed["model_used"] = META_MODEL_NAME
        parsed["mode"] = "LIVE_META_MODEL_API"
        return parsed