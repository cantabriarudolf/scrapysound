import subprocess, os, shutil

def _yt_dlp():
    return shutil.which("yt-dlp") or "yt-dlp"

def download_subtitles(url, outdir, langs=("es-orig", "es"), fmt="srt"):
    os.makedirs(outdir, exist_ok=True)
    cmd = [_yt_dlp(), "--write-subs", "--write-auto-subs",
           "--sub-langs", ",".join(langs), "--sub-format", fmt,
           "--skip-download", "-o", os.path.join(outdir, "%(title)s.%(ext)s"), url]
    subprocess.run(cmd, check=True)

def download_audio(url, outdir, fmt="mp3", quality="5"):
    os.makedirs(outdir, exist_ok=True)
    cmd = [_yt_dlp(), "-x", f"--audio-format={fmt}", f"--audio-quality={quality}",
           "-o", os.path.join(outdir, "audio.%(ext)s"), url]
    subprocess.run(cmd, check=True)

def download_all(url, outdir):
    download_subtitles(url, outdir)
    download_audio(url, outdir)
