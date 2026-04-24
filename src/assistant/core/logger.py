from datetime import datetime


def _ts():
    return datetime.now().strftime("%H:%M:%S")


def log(level: str, msg: str):
    print(f"[{_ts()}] [{level.upper()}] {msg}")
