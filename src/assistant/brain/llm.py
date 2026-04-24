import json

from llama_cpp import Llama

from .intents import INTENTS
from .prompts import intent_prompt
from ..core.logger import log

VALID_INTENTS = set(INTENTS.keys())

# Carregamento do modelo (UMA vez só)
llm = Llama(
    model_path="./models/qwen2.5-0.5b-instruct-q4_k_m.gguf",
    n_ctx=256,  # importante pra 1GB RAM
    n_threads=4,  # ajuste conforme CPU do dispositivo
    n_gpu_layers=0,  # embarcado geralmente CPU only
    verbose=False,
)


# Parser de JSON da saída
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


# Inferência do SLM
def think(text: str) -> dict:
    prompt = intent_prompt(text)

    try:
        output = llm(
            prompt,
            max_tokens=50,  # reduz latência e RAM
            temperature=0.1,
            top_p=0.9,
            repeat_penalty=1.1,
            stop=["```", "\n\n"],
        )["choices"][0]["text"].strip()

    except Exception as e:
        log("LLM_ERROR", str(e))
        return {
            "intent": "unknown",
            "confidence": 0.0,
            "source": "llm_local",
        }

        # 📦 Log bruto (debug essencial)
        log("LLM_RAW", output)

    parsed = extract_json(output)

    if not parsed:
        log("LLM_FAIL_PARSE", output)
        return {
            "intent": "unknown",
            "confidence": 0.0,
            "source": "llm_local",
        }

    intent = parsed.get("intent", "").lower().strip()

    # Validação de intent
    if intent not in VALID_INTENTS:
        log("LLM_INVALID_INTENT", intent)
        intent = "unknown"
        confidence = 0.0
    else:
        confidence = 0.7  # baseline fixo do SLM

    result = {
        "intent": intent,
        "confidence": confidence,
        "source": "slm_local",
        "raw": output,
    }

    log("LLM", f"{intent} ({confidence:.2f})")

    return result
