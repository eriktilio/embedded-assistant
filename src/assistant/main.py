from .audio.stt import listen
from .audio.tts import speak
from .brain.nlp import detect_intent
from .brain.llm import think
from .core.router import route
from .core.logger import log


NLU_THRESHOLD = 0.55


def main():
    log("INFO", "Assistente embarcado iniciado...")

    while True:
        text = listen()

        if not text:
            continue

        log("USER", text)

        # 1. NLP (sempre primeiro)
        nlp = detect_intent(text)
        log("NLP", f"{nlp['intent']} ({nlp['confidence']:.2f})")

        llm = None

        # 2. decisão de fallback
        if nlp["confidence"] < NLU_THRESHOLD:
            llm = think(text)
            log("LLM", f"{llm['intent']} ({llm['confidence']:.2f})")

        # 3. router final (decisão)
        response = route(nlp, llm)

        # 4. log único de saída
        log("ASSISTANT", response)

        # 5. output seguro
        if response:
            speak(response)
