import io
from pathlib import Path
from typing import Optional

from gtts import gTTS


# Map internal classifier labels to audio asset keys.
SOUND_FILE_MAP = {
    "ak_47": "M16.mp3",
    "insas_rifle": "M16.mp3",
    "rifle_22": "sniper-rifle.mp3",
    "m16": "M16.mp3",
    "m4_carbine": "M16.mp3",
    "mp5_smg": "M16.mp3",
    "uzi_smg": "M16.mp3",
    "glock_pistol": None,
    "revolver": None,
    "shotgun": None,
    "sniper_rifle": "sniper-rifle.mp3",
    "grenade": "grenade.mp3",
    "rpg": "grenade.mp3",
    "knife": None,
    "sword": None,
    "crossbow": None,
    "no_weapon": None,
}


def _project_root() -> Path:
    """
    Resolve the project root assuming this file is at rakshakai/utils/audio.py.
    """
    return Path(__file__).resolve().parents[1]


def _sounds_dir() -> Path:
    return _project_root() / "sound"


def load_weapon_sound_bytes(internal_label: str) -> Optional[bytes]:
    """
    Load a pre-recorded .wav sound corresponding to the given internal label.
    Returns None if no asset is configured or file is missing.
    """
    filename = SOUND_FILE_MAP.get(internal_label)
    if not filename:
        return None

    path = _sounds_dir() / filename
    if not path.exists():
        return None

    return path.read_bytes()


def generate_tts_audio_bytes(text: str, lang: str = "en") -> Optional[bytes]:
    """
    Generate text-to-speech audio bytes for the given text using gTTS.
    Returns None if generation fails (e.g., network connectivity issues).
    """
    try:
        buf = io.BytesIO()
        tts = gTTS(text=text, lang=lang)
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except Exception:
        # In production, consider logging the exception.
        return None

