"""
Divide WAV por silencios (>800 ms) en trozos ≥1 s y ≤24 MB.
"""
import math, tempfile
from pathlib import Path
from typing import List
from pydub import AudioSegment, silence
from ..config import MIN_MS, CHUNK_LIMIT

def split_audio(wav_path: Path) -> List[Path]:
    audio = AudioSegment.from_wav(wav_path)
    bytes_per_ms = (audio.frame_rate * audio.sample_width) / 8
    max_ms = math.floor(CHUNK_LIMIT / bytes_per_ms)

    segs = []
    for s in silence.split_on_silence(audio, min_silence_len=800, silence_thresh=-40):
        if len(s) < MIN_MS:
            continue
        if len(s) > max_ms:
            for i in range(0, len(s), max_ms):
                sub = s[i:i+max_ms]
                if len(sub) >= MIN_MS:
                    segs.append(sub)
        else:
            segs.append(s)

    tmp = Path(tempfile.mkdtemp())
    out_files = []
    for i, s in enumerate(segs):
        p = tmp / f"chunk_{i:03d}.wav"
        s.export(p, format="wav")
        out_files.append(p)
    return out_files
