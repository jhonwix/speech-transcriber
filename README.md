# Speech Transcriber 📝📼

Convierte videos MP4 a transcripciones en PDF limpias (ES‑LatAM).

## Instalación

```bash
git clone https://github.com/tu‑usuario/speech‑transcriber.git
cd speech‑transcriber
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # añade tu OPENAI_API_KEY

## Uso CLI
python -m speech_transcriber.cli  path/al/video.mp4

## Uso WEB
flask --app speech_transcriber.webapp.routes run

## Pruebas
pytest
