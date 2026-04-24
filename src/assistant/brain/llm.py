import json
import requests
from pathlib import Path

from .intents import INTENTS
from .prompts import intent_prompt
from ..core.logger import log

VALID_INTENTS = set(INTENTS.keys())

# paths
BASE_DIR = Path(__file__).resolve().parents[1]

# API do llama-server (rodando local)
LLM_URL = "http://127.0.0.1:8080/completion"


# -------------------------
# JSON parser seguro
# -------------------------
def extract_json(text: str):
    if not text:
        return None

    text = text.replace("```json", "").replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        try:
            return json.loads(text[start : end + 1])
        except:
            return None

    return None


# -------------------------
# LLM via llama-server (HTTP)
# -------------------------
def think(text: str) -> dict:
    prompt = intent_prompt(text)

    log("LLM_CMD", "executando llama-server")

    try:
        response = requests.post(
            LLM_URL,
            json={
                "prompt": prompt,
                "n_predict": 20,
                "temperature": 0.1,
                "top_p": 0.9,
                # MUITO IMPORTANTE: força saída curta e evita texto extra
                "stop": ["\n\n", "```"],
            },
            timeout=3,
        )

        data = response.json()
        output = (data.get("content") or "").strip()

        log("LLM_RAW", output)

        parsed = extract_json(output)

        if not parsed:
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "source": "llama-server",
                "raw": output,
            }

        intent = parsed.get("intent", "").lower().strip()

        if intent not in VALID_INTENTS:
            intent = "unknown"
            confidence = 0.0
        else:
            confidence = 0.85  # mais confiável que heurística NLP

        return {
            "intent": intent,
            "confidence": confidence,
            "source": "llama-server",
            "raw": output,
        }

    except Exception as e:
        log("LLM_ERROR", str(e))

        return {
            "intent": "unknown",
            "confidence": 0.0,
            "source": "llama-server",
        }
