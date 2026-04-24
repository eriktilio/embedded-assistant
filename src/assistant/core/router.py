from ..actions.system import get_time, open_spotify
from ..actions.gpio import led_on
from ..core.logger import log

WEIGHTS = {
    "nlp": 1.0,
    "llm": 0.85
}

HANDLERS = {
    "hora": get_time,
    "spotify": open_spotify,
    "ligar_led": led_on,
}


def route(nlp_result=None, llm_result=None):
    candidates = []

    if nlp_result:
        nlp_result = {
            **nlp_result,
            "confidence": nlp_result["confidence"] * WEIGHTS["nlp"]
        }
        candidates.append(nlp_result)

    if llm_result:
        llm_result = {
            **llm_result,
            "confidence": llm_result["confidence"] * WEIGHTS["llm"]
        }
        candidates.append(llm_result)

    log("ROUTER", f"candidates={candidates}")

    best = max(candidates, key=lambda x: x.get("confidence", 0.0))

    log("ROUTER", f"best={best}")

    intent = best.get("intent")

    if not intent or intent in ("unknown", "fallback"):
        log("ROUTER", "fallback_triggered")
        return "Não entendi"

    handler = HANDLERS.get(intent)

    if handler:
        log("ROUTER", f"handler={intent}")
        return handler()

    log("ROUTER", f"handler_not_found={intent}")
    return "Não entendi"