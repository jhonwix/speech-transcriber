"""Namespace package to allow `python -m speech_transcriber.cli`."""
from importlib import metadata
__version__ = metadata.version("speech_transcriber") if "speech_transcriber" in metadata.packages_distributions() else "0.0.0"
