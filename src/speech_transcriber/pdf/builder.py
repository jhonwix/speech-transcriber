from pathlib import Path
import datetime, textwrap
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

def build_pdf(text: str, path: Path, title: str):
    styles = getSampleStyleSheet()
    body   = styles["BodyText"]; body.spaceAfter, body.leading = 6, 14

    doc = SimpleDocTemplate(str(path), pagesize=LETTER,
                            leftMargin=25*mm, rightMargin=25*mm,
                            topMargin=25*mm,  bottomMargin=25*mm,
                            title=title)
    story = [
        Paragraph(f"<b>{title}</b>", styles["Title"]),
        Paragraph(datetime.date.today().isoformat(), styles["Normal"]),
        Spacer(1, 12)
    ]
    for para in text.split("\n\n"):
        story.append(Paragraph(textwrap.fill(para, 100), body))
        story.append(Spacer(1, 8))
    doc.build(story)
    return path
