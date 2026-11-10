import argparse, os, sys, glob

def cmd_download(args):
    from .downloader import download_subtitles, download_audio, download_all
    outdir = args.outdir or "."
    if args.audio_only:
        download_audio(args.url, outdir)
    elif args.subs_only:
        download_subtitles(args.url, outdir)
    else:
        download_all(args.url, outdir)
    print("Download complete.")

def cmd_analyze(args):
    from .analyzer import write_report, find_phrase
    srt = args.srt
    if args.search:
        cues = find_phrase(srt, args.search)
        for c in cues:
            print(f"{c['start_ts']} --> {c['end_ts']} | {c['text']}")
        return
    out = args.out or "phrase_analysis.md"
    a = write_report(srt, out)
    print(f"Analyzed {a['cues']} cues, duration {a['duration']:.2f}s -> {out}")

def cmd_extract(args):
    from .extractor import extract_segment, extract_all_occurrences, to_seconds
    if args.search:
        results = extract_all_occurrences(args.srt, args.audio, args.search, args.outdir or "clips", args.context)
        print(f"Extracted {len(results)} clips -> {args.outdir or 'clips'}")
    else:
        s = to_seconds(args.start); e = to_seconds(args.end)
        out = args.out or os.path.join(args.outdir or ".", "clip.mp3")
        extract_segment(args.audio, s, e, out)
        print(f"OK -> {out}")

def cmd_all(args):
    from .downloader import download_all
    from .analyzer import write_report
    from .extractor import extract_all_occurrences
    outdir = args.outdir or "scrapysound_out"
    os.makedirs(outdir, exist_ok=True)
    print("Downloading...")
    download_all(args.url, outdir)
    srts = glob.glob(os.path.join(outdir, "*.srt"))
    if not srts:
        print("No SRT found", file=sys.stderr); return
    srt = srts[0]
    audio = os.path.join(outdir, "audio.mp3")
    print("Analyzing...")
    write_report(srt, os.path.join(outdir, "phrase_analysis.md"))
    if args.phrase:
        print(f"Extracting '{args.phrase}'...")
        extract_all_occurrences(srt, audio, args.phrase, os.path.join(outdir, "clips"), args.context)
    print("Done.")

def main():
    p = argparse.ArgumentParser(prog="scrapysound", description="YouTube subtitle & audio toolkit (powered by Gentle Shell)")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("download", help="Download subtitles and/or audio")
    d.add_argument("url")
    d.add_argument("-o", "--outdir", default=".")
    d.add_argument("--subs-only", action="store_true")
    d.add_argument("--audio-only", action="store_true")
    d.set_defaults(func=cmd_download)

    a = sub.add_parser("analyze", help="Analyze phrases in an SRT")
    a.add_argument("srt")
    a.add_argument("-o", "--out")
    a.add_argument("--search")
    a.set_defaults(func=cmd_analyze)

    e = sub.add_parser("extract", help="Extract audio clips")
    e.add_argument("--audio", required=True)
    e.add_argument("--srt")
    e.add_argument("--search")
    e.add_argument("start", nargs="?")
    e.add_argument("end", nargs="?")
    e.add_argument("-o", "--out")
    e.add_argument("--outdir", default=".")
    e.add_argument("--context", type=float, default=0.3)
    e.set_defaults(func=cmd_extract)

    al = sub.add_parser("all", help="Full pipeline: download + analyze + extract")
    al.add_argument("url")
    al.add_argument("-o", "--outdir", default="scrapysound_out")
    al.add_argument("--phrase")
    al.add_argument("--context", type=float, default=0.3)
    al.set_defaults(func=cmd_all)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
