"""
Chunk list → texto bruto via gpt‑4o‑transcribe.
"""
from pathlib import Path
from typing import List
from openai import OpenAI
from ..config import OPENAI_KEY
from ..config import TEMPERATURE
# prompts
PROMPT_BASE = (
    "Transcribe en español latino. Mantén signos ¿¡. "
    "Términos técnicos: UiPath, MVP, API, RPA.\n\n"
)
MODEL_TRANS = "gpt-4o-transcribe"

client = OpenAI(api_key=OPENAI_KEY)

def transcribe_chunks(chunks: List[Path]) -> str:
    text = ""
    for ch in chunks:
        with open(ch, "rb") as f:
            rsp = client.audio.transcriptions.create(
                model=MODEL_TRANS,
                file=f,
                language="es",
                temperature=TEMPERATURE,
                prompt=PROMPT_BASE,
                response_format="text"
            )
        text += rsp + "\n\n"
    return text
