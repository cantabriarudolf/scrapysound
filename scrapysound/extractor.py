import json
import os, re, subprocess, shutil

FFMPEG = shutil.which("ffmpeg") or "/home/sh1r0l0x/Descargas/jd2/tools/linux/ffmpeg/x64/ffmpeg"

def to_seconds(ts):
    ts = ts.strip()
    if ":" in ts:
        parts = ts.split(":")
        if len(parts) == 3:
            h, m, rest = parts
            if "," in rest:
                sec, ms = rest.split(",")
                ms = int(ms.ljust(3, "0")[:3])
            else:
                sec, ms = rest, 0
            return int(h)*3600 + int(m)*60 + int(sec) + ms/1000.0
        elif len(parts) == 2:
            m, rest = parts
            if "," in rest:
                sec, ms = rest.split(",")
                ms = int(ms.ljust(3, "0")[:3])
            else:
                sec, ms = rest, 0
            return int(m)*60 + int(sec) + ms/1000.0
    return float(ts)

def fmt(s):
    h = int(s//3600); m = int((s%3600)//60); sec = int(s%60)
    ms = int(round((s-int(s))*1000))
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

def extract_segment(audio_path, start, end, out_path):
    os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else ".", exist_ok=True)
    dur = end - start
    cmd = [FFMPEG, "-y", "-ss", str(start), "-i", audio_path, "-t", str(dur),
           "-acodec", "libmp3lame", "-q:a", "4", out_path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-500:])
    return out_path

def extract_all_occurrences(srt_path, audio_path, phrase, outdir, context=0.3, write_manifest=True):
    from .analyzer import parse_srt
    cues = parse_srt(srt_path)
    q = phrase.lower()
    matches = [c for c in cues if q in c["text"].lower()]
    os.makedirs(outdir, exist_ok=True)
    results = []
    for i, c in enumerate(matches, 1):
        s = max(0, c["start"] - context)
        e = c["end"] + context
        safe = re.sub(r"[^a-zA-Z0-9]+", "_", c["text"])[:40]
        out = os.path.join(outdir, f"{i:03d}_{safe}.mp3")
        extract_segment(audio_path, s, e, out)
        results.append((c, out))
    manifest_path = None
    if write_manifest:
        manifest_path = write_manifest_json(results, outdir)
    return results, manifest_path


def write_manifest_json(results, outdir):
    """Write manifest.json: timestamp + text + clip file for programmatic use."""
    os.makedirs(outdir, exist_ok=True)
    items = []
    for i, (c, path) in enumerate(results, 1):
        items.append({
            "index": i,
            "file": os.path.basename(path),
            "path": path,
            "start": c["start"],
            "end": c["end"],
            "start_ts": c["start_ts"],
            "end_ts": c["end_ts"],
            "text": c["text"],
        })
    manifest_path = os.path.join(outdir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    return manifest_path


def manifest_from_existing_clips(srt_path, phrase, outdir):
    """Build manifest.json from already-extracted mp3s (matched by index prefix)."""
    from .analyzer import parse_srt
    import glob
    cues = parse_srt(srt_path)
    q = phrase.lower()
    matches = [c for c in cues if q in c["text"].lower()]
    mp3s = sorted(glob.glob(os.path.join(outdir, "*.mp3")))
    results = []
    for i, c in enumerate(matches, 1):
        path = mp3s[i - 1] if i - 1 < len(mp3s) else None
        if path is None:
            break
        results.append((c, path))
    return results, write_manifest_json(results, outdir)
