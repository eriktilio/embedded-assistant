from ..actions.system import get_time, open_spotify
from ..actions.gpio import led_on
from ..core.logger import log


HANDLERS = {
    "hora": get_time,
    "spotify": open_spotify,
    "ligar_led": led_on,
}


def route(nlp_result: dict = None, llm_result: dict = None):
    candidates = []

    if nlp_result:
        candidates.append(nlp_result)

    if llm_result:
        candidates.append(llm_result)

    log("ROUTER", f"candidates={candidates}")

    best = max(candidates, key=lambda x: x.get("confidence", 0.0))

    log("ROUTER", f"best={best}")

    intent = best.get("intent")

    if not intent or intent in ("unknown", "fallback"):
        log("ROUTER", "intent=fallback")
        return "Não entendi"

    handler = HANDLERS.get(intent)

    if handler:
        log("ROUTER", f"handler={intent}")
        return handler()

    log("ROUTER", f"handler_not_found={intent}")
    return "Não entendi"