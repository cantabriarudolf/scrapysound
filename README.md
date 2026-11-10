# scrapysound

> **Powered by Gentle Shell** 🐚 — parte del multiverso de proyectos de Gentleman Programming.

> Herramienta para descargar subtítulos y audio de videos de YouTube, estudiar las frases más usadas y extraer segmentos de audio por timestamp.

## ¿Qué es?

`scrapysound` es un pequeño toolkit que combina `yt-dlp` + `ffmpeg` + scripts en Python para:

1. **Descargar subtítulos** de un video de YouTube (en cualquier idioma disponible).
2. **Descargar el audio** del video (mp3).
3. **Analizar las frases más usadas** (palabras, bigramas, trigramas, cues completos).
4. **Extraer segmentos de audio** por timestamp o por búsqueda de frase, generando clips mp3 individuales.

Es una herramienta genérica: el video de entrada puede ser cualquiera. En este repo se incluye un caso de uso real con el video de Gentle Shell.

## Requisitos

- `yt-dlp` (`pip install yt-dlp`)
- `ffmpeg` (en PATH o indicar la ruta en los scripts)
- Python 3.8+

## Uso rápido

### 1. Descargar subtítulos + audio

```bash
yt-dlp --write-subs --write-auto-subs --sub-langs "es-orig,es" --sub-format srt --skip-download -o "%(title)s.%(ext)s" "URL"
yt-dlp -x --audio-format mp3 --audio-quality 5 -o "audio.%(ext)s" "URL"
```

### 2. Analizar frases

Ver `scrapysounds_task/phrase_analysis.md` como ejemplo. Script inline en Python (parsea el SRT y cuenta n-gramas).

### 3. Extraer una frase por timestamp

```bash
python3 tools/extract_phrase.py 00:02:41,919 00:02:49,046 -o clips/mi_frase.mp3
```

### 4. Extraer todas las ocurrencias de una frase

```bash
python3 tools/extract_phrase.py --search "abuela" --extract
# -> clips/001_...mp3, 002_...mp3, ...
```

Timestamps aceptan `HH:MM:SS,mmm`, `HH:MM:SS`, `MM:SS` o segundos (float).

## Estructura

```
scrapysound/
├── README.md
├── tools/
│   └── extract_phrase.py       # Extractor de clips por timestamp/búsqueda
├── scrapysounds_task/          # Caso de uso: video de Gentle Shell
│   ├── README.md
│   ├── phrase_analysis.md      # Análisis de frases del streamer
│   ├── audio_event_mapping.md  # Mapeo estados auditivos ↔ frases
│   ├── *.srt                   # Subtítulos del video
│   └── tools/                  # Copia del extractor
└── work/                       # (no versionado) audio.mp3, clips/, event_sounds/
```

## Caso de uso incluido: video de Gentle Shell

Ver `scrapysounds_task/README.md`.

## Conexión con el multiverso Gentle

`scrapysound` alimenta al fork `gentle-emote-arcade`: las frases extraídas del streamer se asocian a los 14 estados auditivos de Gentle Shell (ver `scrapysounds_task/audio_event_mapping.md`).

## Licencia

Uso personal. El audio y subtítulos pertenecen a sus respectivos autores (YouTube).
