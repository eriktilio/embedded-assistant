import json
from pathlib import Path

import sounddevice as sd
from vosk import Model, KaldiRecognizer
from ..core.logger import log

# =========================
# Configuração
# =========================
MIC_DEVICE = 1
DEBUG_AUDIO = False


# =========================
# Caminho do modelo
# =========================
BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "models" / "vosk-pt"

log("STT", f"loading model from {MODEL_PATH}")


# =========================
# Modelo STT
# =========================
model = Model(str(MODEL_PATH))

device_info = sd.query_devices(MIC_DEVICE, "input")
SAMPLE_RATE = int(device_info["default_samplerate"])

log("STT", f"sample_rate={SAMPLE_RATE}")

rec = KaldiRecognizer(model, SAMPLE_RATE)


# =========================
# Captura de áudio
# =========================
def listen():
    if DEBUG_AUDIO:
        log("STT", str(sd.query_devices()))

    log("STT", "listening...")

    try:
        with sd.RawInputStream(
            device=MIC_DEVICE,
            samplerate=SAMPLE_RATE,
            blocksize=4000,
            dtype="int16",
            channels=1,
        ) as stream:

            while True:
                data, _ = stream.read(2000)
                data_bytes = bytes(data)

                # final result
                if rec.AcceptWaveform(data_bytes):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").strip()

                    if text:
                        log("STT_FINAL", text)
                        return text

                # partial result (live feedback)
                else:
                    partial = json.loads(rec.PartialResult())
                    partial_text = partial.get("partial", "").strip()

                    if partial_text:
                        # evita spam de log pesado (só loga mudanças)
                        log("STT_PARTIAL", partial_text)

    except Exception as e:
        log("STT_ERROR", str(e))
        return ""
