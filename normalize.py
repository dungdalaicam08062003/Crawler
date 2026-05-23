import re


def clean_text(text: str) -> str:

    if not text:
        return ""

    return " ".join(text.split())


def normalize_article(raw: dict) -> dict:

    return {

        "title": clean_text(
            raw.get("title", "")
        ),

        "content": clean_text(
            raw.get("content", "")
        )[:500],

        "url": raw.get("url", "")
    }