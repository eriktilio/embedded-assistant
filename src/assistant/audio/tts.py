import pyttsx3
import threading
from ..core.logger import log

_engine = None
_lock = threading.Lock()


def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()

        # configuração base
        _engine.setProperty("rate", 180)
        _engine.setProperty("volume", 1.0)

    return _engine


def _speak_worker(text: str):
    try:
        with _lock:
            engine = _get_engine()

            # limpa qualquer fala pendente
            engine.stop()

            engine.say(text)
            engine.runAndWait()

    except Exception as e:
        log("TTS_ERROR", str(e))


def speak(text: str):
    if not text or not isinstance(text, str):
        log("TTS_SKIP", "empty or invalid text")
        return

    log("TTS", text)

    # roda em thread para não travar STT loop
    thread = threading.Thread(target=_speak_worker, args=(text,), daemon=True)

    thread.start()
