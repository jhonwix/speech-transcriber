"""
CLI entry – uso:
    python -m speech_transcriber.cli  ruta/al/video.mp4

Opciones:
  --contains "cadena"  → muestra si la cadena aparece en la transcripción.
"""
from pathlib import Path

import click

from .audio import extract_wav, split_audio
from .stt    import transcribe_chunks, clean_text
from .pdf    import build_pdf


def transcribe_file(video_path: Path, contains: str | None = None) -> tuple[Path, Path]:
    """Pipeline completo para un solo archivo MP4.

    Devuelve (pdf_path, txt_path).
    """
    video_path = video_path.resolve()
    wav        = extract_wav(video_path)
    raw_text   = transcribe_chunks(split_audio(wav))
    txt        = clean_text(raw_text)

    if contains:
        found = contains.lower() in txt.lower()
        click.echo(f'[contains] {"✅" if found else "❌"} {contains}')

    pdf_path = video_path.with_name(f"{video_path.stem}_transcripcion.pdf")
    build_pdf(txt, pdf_path, "Transcripción")

    txt_path = video_path.with_suffix(".txt")
    txt_path.write_text(txt, encoding="utf-8")

    return pdf_path, txt_path


@click.command()
@click.argument("video", type=click.Path(exists=True))
@click.option("--contains", help="Cadena a buscar en la transcripción")
def main(video: str, contains: str | None):
    pdf, txt = transcribe_file(Path(video), contains)
    click.echo(f"PDF: {pdf.name}\nTXT: {txt.name}")


if __name__ == "__main__":
    main()
