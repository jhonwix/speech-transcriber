"""
Central config read once and reused.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
ROOT_DIR   = Path(__file__).resolve().parents[1]
UPLOAD_DIR = ROOT_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# External
FFMPEG_PATH = os.getenv("FFMPEG_PATH", r"C:\ffmpeg\bin\ffmpeg.exe")
OPENAI_KEY  = os.getenv("OPENAI_API_KEY", "")

# Audio split params
CHUNK_LIMIT = 24 * 1024 * 1024     # 24 MB
MIN_MS      = 1000                 # 1 s
TEMPERATURE = 0
