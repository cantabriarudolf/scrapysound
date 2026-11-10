import textwrap
from scrapysound import analyzer

SRT = textwrap.dedent("""\
    1
    00:00:01,000 --> 00:00:02,000
    Hola mundo

    2
    00:00:03,000 --> 00:00:04,000
    Hola mundo

    3
    00:00:05,000 --> 00:00:06,000
    [música]

    4
    00:00:07,000 --> 00:00:09,000
    Hola , mundo

    """)


def test_parse_srt_cleans_by_default(tmp_path):
    p = tmp_path / "a.srt"
    p.write_text(SRT, encoding="utf-8")
    cues = analyzer.parse_srt(str(p))
    # music-only dropped, overlapping dupes merged
    assert all(c["text"] for c in cues)
    assert len(cues) <= 3


def test_parse_srt_raw(tmp_path):
    p = tmp_path / "a.srt"
    p.write_text(SRT, encoding="utf-8")
    cues = analyzer.parse_srt(str(p), use_clean=False)
    assert len(cues) == 3


def test_analyze_and_find(tmp_path):
    p = tmp_path / "a.srt"
    p.write_text(SRT, encoding="utf-8")
    a = analyzer.analyze(str(p))
    assert a["cues"] >= 1
    found = analyzer.find_phrase(str(p), "hola")
    assert len(found) >= 1
