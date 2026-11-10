"""SRT cleaning for auto-generated subtitles. Powered by Gentle Shell."""
import re


def normalize_punctuation(text):
    """Collapse whitespace, fix spacing before punctuation."""
    text = re.sub(r"\s+", " ", text).strip()
    # remove space before punctuation: "hola , mundo" -> "hola, mundo"
    text = re.sub(r"\s+([,.;:!?\)\]])", r"\1", text)
    # ensure space after punctuation when followed by letter: "hola,mundo" -> "hola, mundo"
    text = re.sub(r"([,.;:!?])([A-Za-zÁÉÍÓÚáéíóúÑñ])", r"\1 \2", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _norm_key(text):
    s = text.lower()
    s = re.sub(r"[¿¡!?.,;:()\"']", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def clean_cues(cues):
    """Drop music-only/empty cues, dedupe overlaps, normalize punctuation.

    cues: list of dicts with keys start, end, text, start_ts, end_ts.
    Returns a new cleaned list.
    """
    cleaned = []
    seen_exact = set()
    for c in cues:
        text = normalize_punctuation(c.get("text", ""))
        if not text:
            continue
        key = (round(c["start"], 3), round(c["end"], 3), text)
        if key in seen_exact:
            continue
        seen_exact.add(key)
        cleaned.append({**c, "text": text})

    # dedupe overlapping cues with identical normalized text: keep earliest
    result = []
    for c in sorted(cleaned, key=lambda x: x["start"]):
        dup = False
        for kept in result:
            if _norm_key(kept["text"]) == _norm_key(c["text"]):
                # overlap in time?
                if c["start"] < kept["end"] and kept["start"] < c["end"]:
                    dup = True
                    break
        if not dup:
            result.append(c)
    return result


def clean_srt_file(path):
    """Parse an SRT file and return cleaned cues."""
    from .analyzer import parse_srt as _parse_raw
    cues = _parse_raw(path, use_clean=False)
    return clean_cues(cues)
