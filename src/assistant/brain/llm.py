import json
import requests

from .intents import INTENTS
from .prompts import intent_prompt
from ..core.logger import log

VALID_INTENTS = set(INTENTS.keys())


def extract_json(text: str) -> dict | None:
    text = text.strip()
    text = text.replace("```json", "").replace("```", "")

    try:
        return json.loads(text)
    except:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start : end + 1])
            except:
                return None
    return None


def think(text: str) -> dict:
    prompt = intent_prompt(text)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:0.5b",
                "prompt": prompt,
                "stream": False,
                "temperature": 0.1,
                "top_p": 0.9,
                "repeat_penalty": 1.1,
            },
            timeout=20,
        )
    except Exception as e:
        log("LLM_ERROR", str(e))
        return {
            "intent": "unknown",
            "confidence": 0.0,
            "source": "llm",
        }

    output = response.json().get("response", "").strip()

    parsed = extract_json(output)

    # log bruto (importantíssimo pra debug futuro)
    log("LLM_RAW", output)

    if not parsed:
        log("LLM_FAIL_PARSE", output)
        return {
            "intent": "unknown",
            "confidence": 0.0,
            "source": "llm",
        }

    intent = parsed.get("intent", "").lower().strip()

    if intent not in VALID_INTENTS:
        log("LLM_INVALID_INTENT", intent)
        intent = "unknown"
        confidence = 0.0
    else:
        confidence = 0.7  # baseline do LLM

    result = {
        "intent": intent,
        "confidence": confidence,
        "source": "llm",
        "raw": output,
    }

    log("LLM", f"{intent} ({confidence:.2f})")

    return result