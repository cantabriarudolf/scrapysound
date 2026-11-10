import textwrap
import pytest
from scrapysound import cleaner

SAMPLE = [
    {"start": 1.0, "end": 3.0, "text": "Hola , mundo", "start_ts": "00:00:01,000", "end_ts": "00:00:03,000"},
    {"start": 1.5, "end": 3.5, "text": "hola, mundo", "start_ts": "00:00:01,500", "end_ts": "00:00:03,500"},
    {"start": 5.0, "end": 6.0, "text": "", "start_ts": "00:00:05,000", "end_ts": "00:00:06,000"},
    {"start": 7.0, "end": 8.0, "text": "Bien", "start_ts": "00:00:07,000", "end_ts": "00:00:08,000"},
]


def test_normalize_punctuation():
    assert cleaner.normalize_punctuation("hola , mundo") == "hola, mundo"
    assert cleaner.normalize_punctuation("  hola   mundo  ") == "hola mundo"


def test_clean_cues_dedupes_overlap():
    out = cleaner.clean_cues(SAMPLE)
    texts = [c["text"].lower() for c in out]
    assert texts.count("hola, mundo") == 1
    assert "bien" in texts
    assert "" not in texts


def test_clean_srt_file(tmp_path):
    srt = tmp_path / "a.srt"
    srt.write_text(textwrap.dedent("""\
        1
        00:00:01,000 --> 00:00:03,000
        Hola , mundo

        2
        00:00:05,000 --> 00:00:06,000
        [música]

        """), encoding="utf-8")
    cues = cleaner.clean_srt_file(str(srt))
    assert len(cues) == 1
    assert cues[0]["text"] == "Hola, mundo"
