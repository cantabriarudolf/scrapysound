import textwrap
import json
from scrapysound import extractor

SRT = textwrap.dedent("""\
    1
    00:00:01,000 --> 00:00:02,000
    Abuela salió video

    2
    00:00:05,000 --> 00:00:06,000
    Otra cosa

    3
    00:00:07,000 --> 00:00:08,000
    abuela otra vez

    """)


def test_extract_all_writes_manifest(tmp_path, monkeypatch):
    srt = tmp_path / "a.srt"
    srt.write_text(SRT, encoding="utf-8")
    audio = tmp_path / "audio.mp3"
    audio.write_text("fake", encoding="utf-8")
    outdir = tmp_path / "clips"

    calls = []

    def fake_segment(a, s, e, out):
        calls.append((s, e, out))
        with open(out, "w", encoding="utf-8") as f:
            f.write("clip")
        return out

    monkeypatch.setattr(extractor, "extract_segment", fake_segment)
    results, manifest = extractor.extract_all_occurrences(
        str(srt), str(audio), "abuela", str(outdir))
    assert len(results) == 2
    assert len(calls) == 2
    with open(manifest, encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 2
    assert data[0]["text"].lower().startswith("abuela")
    assert data[0]["file"].endswith(".mp3")


def test_manifest_from_existing(tmp_path):
    srt = tmp_path / "a.srt"
    srt.write_text(SRT, encoding="utf-8")
    outdir = tmp_path / "clips"
    outdir.mkdir()
    (outdir / "001_x.mp3").write_text("x", encoding="utf-8")
    (outdir / "002_y.mp3").write_text("y", encoding="utf-8")
    results, manifest = extractor.manifest_from_existing_clips(
        str(srt), "abuela", str(outdir))
    assert len(results) == 2
    with open(manifest, encoding="utf-8") as f:
        data = json.load(f)
    assert data[0]["file"] == "001_x.mp3"
