"""Rich phrase analysis: catchphrases, timelines, wordcloud data. Powered by Gentle Shell."""
import collections
import json
import os

from .analyzer import norm, parse_srt


def word_frequencies(cues, top=50):
    words = collections.Counter()
    for c in cues:
        for w in norm(c["text"]).split():
            words[w] += 1
    return words.most_common(top)


def detect_catchphrases(cues, min_repeats=3):
    """Full normalized cue texts repeated >= min_repeats, sorted by count desc."""
    full = collections.Counter(norm(c["text"]) for c in cues)
    return sorted(
        [(t, n) for t, n in full.items() if n >= min_repeats],
        key=lambda x: -x[1],
    )


def phrase_timeline(cues, phrase):
    """All cues containing phrase (case-insensitive) in timeline order."""
    q = phrase.lower()
    out = []
    for c in sorted(cues, key=lambda x: x["start"]):
        if q in c["text"].lower():
            out.append({"start": c["start"], "end": c["end"],
                        "start_ts": c["start_ts"], "end_ts": c["end_ts"],
                        "text": c["text"]})
    return out


def write_wordcloud_data(cues, out_path, top=100):
    freqs = word_frequencies(cues, top=top)
    data = {"words": [{"text": w, "value": n} for w, n in freqs]}
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data


def write_rich_report(srt_path, outdir, top_catchphrases=10):
    """Write phrase_analysis.md + wordcloud.json + timeline JSONs for top catchphrases."""
    from .analyzer import write_report
    os.makedirs(outdir, exist_ok=True)
    cues = parse_srt(srt_path)
    a = write_report(srt_path, os.path.join(outdir, "phrase_analysis.md"))
    write_wordcloud_data(cues, os.path.join(outdir, "wordcloud.json"))
    catchphrases = detect_catchphrases(cues)[:top_catchphrases]
    timelines = {}
    for phrase, count in catchphrases:
        tl = phrase_timeline(cues, phrase)
        timelines[phrase] = tl
    with open(os.path.join(outdir, "timelines.json"), "w", encoding="utf-8") as f:
        json.dump(timelines, f, ensure_ascii=False, indent=2)
    return {"analysis": a, "catchphrases": catchphrases, "outdir": outdir}
