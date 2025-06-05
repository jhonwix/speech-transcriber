"""
Video → WAV mono 16 kHz 16‑bit PCM.
Si FFmpeg no encuentra audio, lanza AudioMissingError.
"""
import subprocess
from pathlib import Path
from ..config import FFMPEG_PATH

class AudioMissingError(RuntimeError):
    """Se dispara cuando el video no contiene pista de audio o FFmpeg falla."""

def extract_wav(video: Path) -> Path:
    wav_out = video.with_suffix(".wav")

    cmd = [
        FFMPEG_PATH, "-i", str(video),
        "-vn", "-ar", "16000", "-ac", "1",
        "-c:a", "pcm_s16le",
        str(wav_out)
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.returncode != 0:
        # Busca indicio de ausencia de audio
        if "does not contain any stream" in proc.stderr.lower() or \
           "stream mapping" in proc.stderr.lower() and "Audio" not in proc.stderr:
            raise AudioMissingError(f"El archivo «{video.name}» no contiene pista de audio.")
        # Otros errores
        raise AudioMissingError(f"FFmpeg falló: {proc.stderr.splitlines()[-1]}")

    return wav_out
