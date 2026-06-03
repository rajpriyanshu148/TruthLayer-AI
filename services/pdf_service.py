import fitz
from typing import Optional
from utils.config import MAX_TEXT_CHARS
from utils.helpers import truncate_text


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        pages_text = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            if text.strip():
                pages_text.append(f"[Page {page_num + 1}]\n{text.strip()}")
        doc.close()
        full_text = "\n\n".join(pages_text)
        return truncate_text(full_text, MAX_TEXT_CHARS)
    except Exception as e:
        raise RuntimeError(f"PDF extraction failed: {e}") from e


def get_pdf_metadata(file_bytes: bytes) -> dict:
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        meta = doc.metadata or {}
        page_count = len(doc)
        doc.close()
        return {
            "title": meta.get("title", "Unknown"),
            "author": meta.get("author", "Unknown"),
            "pages": page_count,
            "subject": meta.get("subject", ""),
        }
    except Exception:
        return {"title": "Unknown", "author": "Unknown", "pages": 0, "subject": ""}
