import pyttsx3
from ..core.logger import log

# cria engine UMA vez (import-time singleton)
_engine = pyttsx3.init()
_engine.setProperty("rate", 180)


def speak(text: str):
    if not text:
        log("TTS_SKIP", "empty text")
        return

    log("TTS", text)

    try:
        _engine.say(text)
        _engine.runAndWait()
    except Exception as e:
        log("TTS_ERROR", str(e))
    finally:
        # garante que não acumula estado interno estranho
        _engine.stop()
