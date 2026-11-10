import textwrap
from scrapysound import rich_analysis


def _cues():
    return [
        {"start": 1.0, "end": 2.0, "text": "Bien", "start_ts": "00:00:01,000", "end_ts": "00:00:02,000"},
        {"start": 3.0, "end": 4.0, "text": "bien", "start_ts": "00:00:03,000", "end_ts": "00:00:04,000"},
        {"start": 5.0, "end": 6.0, "text": "Bien!", "start_ts": "00:00:05,000", "end_ts": "00:00:06,000"},
        {"start": 7.0, "end": 8.0, "text": "Otra cosa", "start_ts": "00:00:07,000", "end_ts": "00:00:08,000"},
    ]


def test_detect_catchphrases():
    out = rich_analysis.detect_catchphrases(_cues(), min_repeats=3)
    assert out[0][0] == "bien"
    assert out[0][1] == 3


def test_phrase_timeline():
    tl = rich_analysis.phrase_timeline(_cues(), "bien")
    assert len(tl) == 3
    assert tl[0]["start"] == 1.0


def test_wordcloud(tmp_path):
    p = tmp_path / "wc.json"
    data = rich_analysis.write_wordcloud_data(_cues(), str(p))
    assert data["words"][0]["text"] == "bien"
    assert p.exists()
