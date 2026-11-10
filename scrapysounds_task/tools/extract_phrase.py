#!/usr/bin/env python3
"""Extract an audio segment from the downloaded video audio by timestamp.

Usage:
  python extract_phrase.py 00:02:41,919 00:02:44,000 -o abuela.mp3
  python extract_phrase.py 161.92 169.05 -o abuela.mp3
  python extract_phrase.py --search "abuela"            # prints cues + suggested cuts
  python extract_phrase.py --search "abuela" --extract  # extracts every matching cue

Timestamps accept HH:MM:SS,mmm / HH:MM:SS / seconds (float).
"""
import argparse, os, re, subprocess, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(BASE, "work", "video", "audio.mp3")
SRT = os.path.join(BASE, "work", "video", "Te muestro la EVOLUCIÓN de Gentle Shell ! y... anuncio IMPORTANTE !.es-orig.srt")
FFMPEG = "/home/sh1r0l0x/Descargas/jd2/tools/linux/ffmpeg/x64/ffmpeg"
OUTDIR = os.path.join(BASE, "work", "video", "clips")


def to_seconds(ts):
    ts = ts.strip()
    if ":" in ts:
        parts = ts.split(":")
        # HH:MM:SS,mmm or MM:SS
        if len(parts) == 3:
            h, m, rest = parts
            if "," in rest:
                sec, ms = rest.split(",")
                ms = int(ms.ljust(3, "0")[:3])
            else:
                sec, ms = rest, 0
            return int(h) * 3600 + int(m) * 60 + int(sec) + ms / 1000.0
        elif len(parts) == 2:
            m, rest = parts
            if "," in rest:
                sec, ms = rest.split(",")
                ms = int(ms.ljust(3, "0")[:3])
            else:
                sec, ms = rest, 0
            return int(m) * 60 + int(sec) + ms / 1000.0
    return float(ts)


def fmt(s):
    h = int(s // 3600); m = int((s % 3600) // 60); sec = int(s % 60)
    ms = int(round((s - int(s)) * 1000))
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"


def parse_srt(path):
    text = open(path, encoding="utf-8").read()
    blocks = re.split(r"\n\s*\n", text)
    cues = []
    for b in blocks:
        lines = b.strip().splitlines()
        if len(lines) < 3:
            continue
        mm = re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", lines[1])
        if not mm:
            continue
        start = to_seconds(mm.group(1)); end = to_seconds(mm.group(2))
        body = " ".join(lines[2:]).strip()
        body = re.sub(r"<[^>]+>", "", body)
        cues.append((start, end, body, mm.group(1), mm.group(2)))
    return cues


def extract(start, end, out):
    os.makedirs(os.path.dirname(out) if os.path.dirname(out) else ".", exist_ok=True)
    dur = end - start
    cmd = [FFMPEG, "-y", "-ss", str(start), "-i", AUDIO, "-t", str(dur),
           "-acodec", "libmp3lame", "-q:a", "4", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("ffmpeg error:", r.stderr[-500:], file=sys.stderr)
        return False
    print(f"OK -> {out}  ({fmt(start)} -> {fmt(end)}, {dur:.2f}s)")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("start", nargs="?")
    ap.add_argument("end", nargs="?")
    ap.add_argument("-o", "--out")
    ap.add_argument("--search", help="phrase to search in subtitles")
    ap.add_argument("--extract", action="store_true", help="extract every matching cue (with --search)")
    ap.add_argument("--context", type=float, default=0.3, help="extra seconds before/after cue")
    ap.add_argument("--outdir", help="output directory for --extract (default work/video/clips)")
    args = ap.parse_args()

    if args.search:
        cues = parse_srt(SRT)
        q = args.search.lower()
        matches = [c for c in cues if q in c[2].lower()]
        print(f"Found {len(matches)} cues containing '{args.search}':")
        for c in matches:
            print(f"  {fmt(c[0])} --> {fmt(c[1])} | {c[2]}")
        if args.extract:
            od = args.outdir or OUTDIR
            os.makedirs(od, exist_ok=True)
            for i, c in enumerate(matches, 1):
                s = max(0, c[0] - args.context)
                e = c[1] + args.context
                safe = re.sub(r"[^a-zA-Z0-9]+", "_", c[2])[:40]
                out = os.path.join(od, f"{i:03d}_{safe}.mp3")
                extract(s, e, out)
        return

    if not args.start or not args.end:
        ap.error("need start and end (or --search)")
    s = to_seconds(args.start); e = to_seconds(args.end)
    if e <= s:
        ap.error("end must be > start")
    out = args.out or os.path.join(OUTDIR, f"clip_{fmt(s).replace(',','_').replace(':','')}.mp3")
    os.makedirs(os.path.dirname(out) if os.path.dirname(out) else ".", exist_ok=True)
    extract(s, e, out)


if __name__ == "__main__":
    main()
