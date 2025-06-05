"""
Flask blueprint – web interface with background jobs & live progress.
"""
from pathlib import Path
from threading import Thread, Lock
from uuid import uuid4

from flask import (
    Blueprint, render_template, request, send_from_directory,
    flash, jsonify
)

from ..config import UPLOAD_DIR
from ..audio.extractor import extract_wav, AudioMissingError
from ..audio           import split_audio
from ..stt             import transcribe_chunks, clean_text
from ..pdf             import build_pdf

bp = Blueprint("web", __name__,
               static_folder="static",
               template_folder="templates")

# --------------------------------- state ---------------------------------
_PROGRESS: dict[str, int]            = {}  # job_id -> % (0‑100)
_RESULTS:  dict[str, list[dict]]     = {}  # job_id -> [{"video":name,"pdf":name}]
_LOCK = Lock()

# --------------------------------- routes --------------------------------
@bp.get("/")
def index():
    return render_template("index.html")

@bp.post("/upload")
def upload():
    """Save files, create background job, return job_id immediately."""
    files = request.files.getlist("videos")
    if not files:
        return jsonify({"error": "no files"}), 400

    saved: list[Path] = []
    for f in files:
        dst = UPLOAD_DIR / f.filename
        f.save(dst)
        saved.append(dst)

    job_id = uuid4().hex
    with _LOCK:
        _PROGRESS[job_id] = 0
        _RESULTS[job_id]  = []

    Thread(target=_worker, args=(job_id, saved), daemon=True).start()
    return jsonify({"job_id": job_id})

@bp.get("/progress/<job_id>")
def progress(job_id: str):
    with _LOCK:
        pct  = _PROGRESS.get(job_id, 100)
        outs = _RESULTS.get(job_id, []) if pct == 100 else []
    return jsonify({"progress": pct, "outputs": outs})

@bp.get("/uploads/<path:filename>")
def download(filename):
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)

# ----------------------------- background job ----------------------------
def _worker(job_id: str, paths: list[Path]):
    try:
        for path in paths:
            try:
                wav = extract_wav(path)
            except AudioMissingError as err:
                flash(str(err), "warning")
                continue

            chunks = split_audio(wav)
            total  = len(chunks)
            raw    = ""

            for ix, ch in enumerate(chunks, 1):
                raw += transcribe_chunks([ch])
                _set(job_id, int(ix / total * 90))   # hasta 90 %

            clean = clean_text(raw)
            pdf   = build_pdf(
                        clean,
                        path.with_name(f"{path.stem}_transcripcion.pdf"),
                        "Transcripción")
            with _LOCK:
                _RESULTS[job_id].append({"video": path.name, "pdf": pdf.name})

        _set(job_id, 100)
    except Exception as exc:
        flash(f"Error: {exc}", "warning")
        _set(job_id, 100)

def _set(job_id: str, value: int):
    with _LOCK:
        _PROGRESS[job_id] = value
