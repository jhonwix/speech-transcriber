"""
GPT‑4o‑mini para ortografía y párrafos coherentes.
"""
from openai import OpenAI
from ..config import OPENAI_KEY

MODEL_CLEAN  = "gpt-4o-mini"
PROMPT_CLEAN = (
    "Corrige ortografía y puntuación en español latino. "
    "Agrupa en párrafos de 2 a 4 oraciones."
)

client = OpenAI(api_key=OPENAI_KEY)

def clean_text(raw: str) -> str:
    rsp = client.chat.completions.create(
        model=MODEL_CLEAN,
        temperature=0.2,
        messages=[
            {"role":"system","content": PROMPT_CLEAN},
            {"role":"user",  "content": raw},
        ],
    )
    return rsp.choices[0].message.content.strip()
