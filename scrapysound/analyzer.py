import re, collections, os, glob

def parse_srt(path):
    text = open(path, encoding="utf-8").read()
    blocks = re.split(r"\n\s*\n", text)
    cues = []
    for b in blocks:
        lines = b.strip().splitlines()
        if len(lines) < 3:
            continue
        m = re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", lines[1])
        if not m:
            continue
        def tosec(s):
            h, mn, rest = s.split(":")
            sec, ms = rest.split(",")
            return int(h)*3600 + int(mn)*60 + int(sec) + int(ms)/1000.0
        body = " ".join(lines[2:]).strip()
        body = re.sub(r"<[^>]+>", "", body)
        body = re.sub(r"\[[^\]]*\]", "", body).strip()
        if not body:
            continue
        cues.append({"start": tosec(m.group(1)), "end": tosec(m.group(2)),
                     "text": body, "start_ts": m.group(1), "end_ts": m.group(2)})
    return cues

def norm(s):
    s = s.lower()
    s = re.sub(r"[¿¡!?.,;:()\"']", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def analyze(srt_path, top=20):
    cues = parse_srt(srt_path)
    words = collections.Counter()
    bigrams = collections.Counter()
    trigrams = collections.Counter()
    full = collections.Counter()
    for c in cues:
        t = norm(c["text"])
        ws = t.split()
        for w in ws:
            words[w] += 1
        for i in range(len(ws)-1):
            bigrams[" ".join(ws[i:i+2])] += 1
        for i in range(len(ws)-2):
            trigrams[" ".join(ws[i:i+3])] += 1
        full[t] += 1
    return {
        "cues": len(cues),
        "duration": cues[-1]["end"] if cues else 0,
        "words": words.most_common(top),
        "bigrams": [(p, n) for p, n in bigrams.most_common(top) if n >= 3],
        "trigrams": [(p, n) for p, n in trigrams.most_common(top) if n >= 3],
        "full_repeats": [(p, n) for p, n in full.most_common(top) if n >= 3],
    }

def find_phrase(srt_path, phrase):
    cues = parse_srt(srt_path)
    q = phrase.lower()
    return [c for c in cues if q in c["text"].lower()]

def write_report(srt_path, out_path):
    a = analyze(srt_path)
    lines = []
    lines.append("# Phrase analysis\n")
    lines.append(f"- Cues: {a['cues']}")
    lines.append(f"- Duration: {a['duration']:.2f}s\n")
    lines.append("## Top words")
    for w, n in a["words"]:
        lines.append(f"- {w}: {n}")
    lines.append("\n## Top bigrams (>=3)")
    for p, n in a["bigrams"]:
        lines.append(f"- {p}: {n}")
    lines.append("\n## Top trigrams (>=3)")
    for p, n in a["trigrams"]:
        lines.append(f"- {p}: {n}")
    lines.append("\n## Full cues repeated (>=3)")
    for p, n in a["full_repeats"]:
        lines.append(f"- {p}: {n}")
    open(out_path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return a
