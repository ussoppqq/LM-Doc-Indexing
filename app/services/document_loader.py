import re
from pathlib import Path
from pypdf import PdfReader

PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")

    text = re.sub(r"\n\d+\n", "\n", text)

    lines = [l.strip() for l in text.splitlines() if len(l.strip()) > 0]
    text = " ".join(lines)

    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"-\s+", "", text)

    return text.strip()

def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    raw_text = ""

    for page in reader.pages:
        if page.extract_text():
            raw_text += page.extract_text() + "\n"

    cleaned_text = clean_text(raw_text)

    output_path = PROCESSED_DIR / (Path(path).stem + ".txt")
    output_path.write_text(cleaned_text, encoding="utf-8")

    return cleaned_text
