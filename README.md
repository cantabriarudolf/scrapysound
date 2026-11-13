<p align="center">
  <img src="assets/logo.svg" width="120" alt="scrapysound logo" />
</p>

# scrapysound

<p align="center">
  <strong>Powered by Gentle Shell</strong> 🐚 — parte del multiverso de proyectos de Gentleman Programming.
</p>

> Herramienta para descargar subtítulos y audio de videos de YouTube, estudiar las frases más usadas y extraer segmentos de audio por timestamp.

## ¿Qué es?

`scrapysound` es un toolkit que combina `yt-dlp` + `ffmpeg` + Python para:

1. **Descargar subtítulos** de un video de YouTube (cualquier idioma disponible).
2. **Descargar el audio** del video (mp3).
3. **Limpiar el SRT** auto-generado (dedupe solapados, saca `[música]`, normaliza puntuación).
4. **Analizar las frases más usadas** (palabras, bigramas, trigramas, muletillas, timeline, nube de palabras).
5. **Extraer segmentos de audio** por timestamp o por búsqueda de frase, con `manifest.json`.
6. **Registrar clips como sonidos** de notificación de Gentle Shell (`map-sound`).

Es una herramienta genérica: el video de entrada puede ser cualquiera. Incluye un caso de uso real con el video de Gentle Shell.

## Requisitos

- `yt-dlp` (`pip install yt-dlp`)
- `ffmpeg` (en PATH)
- Python 3.10+

## Instalación

```bash
pip install -e ".[dev]"   # dev incluye pytest
# o solo runtime:
pip install -e .
```

## Uso (CLI)

```bash
# Pipeline completo: descarga + analiza + extrae
scrapysound all "URL" -o out --phrase "abuela"

# Solo descargas
scrapysound download "URL" -o out
scrapysound download "URL" -o out --subs-only
scrapysound download "URL" -o out --audio-only

# Análisis
scrapysound analyze video.srt -o phrase_analysis.md
scrapysound analyze video.srt --search "locura"
scrapysound analyze video.srt --rich --outdir rich_out
# --rich genera: phrase_analysis.md + wordcloud.json + timelines.json

# Extracción
scrapysound extract --audio audio.mp3 00:02:41,919 00:02:49,046 -o clips/mi_frase.mp3
scrapysound extract --audio audio.mp3 --srt video.srt --search "abuela" --outdir clips/
# cada extracción escribe clips/manifest.json

# Manifiesto desde clips ya existentes
scrapysound manifest --srt video.srt --phrase "abuela" --outdir clips/

# Registrar un clip como sonido de Gentle Shell (14 eventos)
scrapysound map-sound --clip clips/001_abuela.mp3 --event agent.completed --dry-run
scrapysound map-sound --clip clips/001_abuela.mp3 --event agent.completed
```

Timestamps aceptan `HH:MM:SS,mmm`, `HH:MM:SS`, `MM:SS` o segundos (float).

Eventos válidos: `session.started`, `agent.started`, `agent.completed`, `agent.failed`, `agent.cancelled`, `agent.attention`, `subagent.queued`, `subagent.running`, `subagent.waiting`, `subagent.completed`, `subagent.failed`, `subagent.cancelled`, `subagent.timed_out`, `context.high`.

## Estructura

```
scrapysound/
├── assets/logo.svg
├── scrapysound/            # paquete Python
│   ├── downloader.py       # baja subtítulos + audio (yt-dlp)
│   ├── cleaner.py          # limpia SRT auto-generados
│   ├── analyzer.py         # n-gramas + reportes
│   ├── rich_analysis.py    # muletillas, timeline, wordcloud
│   ├── extractor.py        # recorta clips + manifest.json
│   ├── integration.py      # map-sound → notifications.json
│   └── cli.py              # CLI unificada
├── tests/                  # pytest (15 tests)
├── .github/workflows/ci.yml
├── tools/extract_phrase.py # script original (legacy)
├── scrapysounds_task/      # caso de uso: video de Gentle Shell
└── work/                   # (no versionado) audio.mp3, clips/, event_sounds/
```

## Caso de uso: video de Gentle Shell

Ver `scrapysounds_task/README.md` — análisis de muletillas del streamer + mapeo de los 14 estados auditivos de Gentle Shell a frases reales.

## Conexión con el multiverso Gentle

`scrapysound` alimenta al fork `gentle-emote-arcade`: las frases extraídas del streamer se asocian a los 14 estados auditivos de Gentle Shell (ver `scrapysounds_task/audio_event_mapping.md`). Con `map-sound` un clip extraído se registra directo en `notifications.json`.

## Licencia

MIT — licencia colaborativa y permisiva: usá, modificá, distribuí y contribuí libremente. Ver [LICENSE](LICENSE).

El audio y subtítulos descargados pertenecen a sus respectivos autores (YouTube).

---

<p align="center">
  <img src="assets/logo.svg" width="60" alt="logo" /><br />
  <strong>Powered by Gentle Shell</strong> 🐚
</p>
