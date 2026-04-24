from datetime import datetime
import os


def get_time():
    return f"Agora são {datetime.now().strftime('%H:%M')}"


def open_spotify():
    os.system("spotify")
    return "Abrindo Spotify"
