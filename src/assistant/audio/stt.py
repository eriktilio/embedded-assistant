import json
from pathlib import Path
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from ..core.logger import log

MIC_DEVICE = 1
DEBUG_AUDIO = False


# =================================================
# PATH CORRETO (ROOT = src/assistant)
# =================================================
ASSISTANT_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = ASSISTANT_DIR / "models" / "vosk-pt"


_model = None
_rec = None
_sample_rate = None


def _init_stt():
    global _model, _rec, _sample_rate

    if _model is not None:
        return

    log("STT", f"loading model from {MODEL_PATH}")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Vosk model not found: {MODEL_PATH}")

    _model = Model(str(MODEL_PATH))

    device_info = sd.query_devices(MIC_DEVICE, "input")
    _sample_rate = int(device_info["default_samplerate"])

    log("STT", f"sample_rate={_sample_rate}")

    _rec = KaldiRecognizer(_model, _sample_rate)


def listen():
    global _rec

    _init_stt()

    if DEBUG_AUDIO:
        log("STT", str(sd.query_devices()))

    log("STT", "listening...")

    try:
        with sd.RawInputStream(
            device=MIC_DEVICE,
            samplerate=_sample_rate,
            blocksize=4000,
            dtype="int16",
            channels=1,
        ) as stream:

            while True:
                data, _ = stream.read(2000)
                data_bytes = bytes(data)

                if _rec.AcceptWaveform(data_bytes):
                    result = json.loads(_rec.Result())
                    text = result.get("text", "").strip()

                    if text:
                        log("STT_FINAL", text)
                        return text

                else:
                    partial = json.loads(_rec.PartialResult())
                    partial_text = partial.get("partial", "").strip()

                    if partial_text:
                        log("STT_PARTIAL", partial_text)

    except Exception as e:
        log("STT_ERROR", str(e))
        return ""
