from .audio.stt import listen
from .audio.tts import speak
from .brain.nlp import detect_intent
from .brain.llm import think
from .core.router import route
from .core.logger import log


def main():
    log("INFO", "Assistente embarcado iniciado...")

    while True:
        text = listen()

        if not text:
            continue

        log("USER", text)

        # 1. NLP first
        nlp = detect_intent(text)
        log("NLP", f"{nlp['intent']} ({nlp['confidence']:.2f})")

        llm = None

        # 2. fallback para LLM se NLP fraco
        if nlp["confidence"] < 0.55:
            llm = think(text)
            log("LLM", llm)

        # 3. decisão final
        response = route(nlp, llm)

        # 4. log de saída única (IMPORTANTE)
        log("ASSISTANT", response)

        # 5. output único garantido
        if response:
            speak(response)