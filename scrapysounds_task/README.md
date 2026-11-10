# scrapysounds_task — Caso de uso: video de Gentle Shell

Tarea realizada con `scrapysound` sobre el video:
- **URL:** https://www.youtube.com/watch?v=KTRoVbZeo3s
- **Título:** "Te muestro la EVOLUCIÓN de Gentle Shell ! y... anuncio IMPORTANTE !"
- **Duración:** ~02:05:13
- **Idioma:** Español (original, auto-generado por YouTube)

## Archivos

- `phrase_analysis.md` — Análisis de las frases más usadas por el streamer (Gentleman Programming): top palabras, bigramas, trigramas, muletillas, timestamps.
- `audio_event_mapping.md` — Mapeo propuesto entre los 14 estados auditivos de Gentle Shell (del repo `gentle-emote-arcade`) y las frases reales del streamer.
- `*.srt` — Subtítulos descargados (es-orig y es).
- `tools/extract_phrase.py` — Extractor de clips de audio por timestamp o búsqueda de frase.

## Lo que se hizo

1. **Descarga de subtítulos** en español (original y traducido).
2. **Descarga del audio** del video (mp3, 92 MB).
3. **Análisis de frases:** se parsearon los 2572 cues del SRT y se contaron palabras, bigramas, trigramas y cues completos. Se identificaron las muletillas características del streamer ("así no más", "ahí está/ahí lo tienen/ahí lo tenés", "espectacular", "la verdad eh", "voy a mentir", "qué les parece", "me gusta", "una cosa así", "gentle shell", "locura/locurita").
4. **Extracción de clips:** se generaron ~1786 clips mp3 organizados por frase en `work/video/clips/<frase>/` (no versionados por tamaño).
5. **Mapeo audio-evento:** se asociaron los 14 eventos de notificación de Gentle Shell (del repo `gentle-emote-arcade`) a frases reales del streamer, con timestamps. Los 14 wavs de los eventos se copiaron a `work/video/event_sounds/`.

## Frases características identificadas

- "así no más" (22x)
- "ahí está" (6x) / "ahí lo tienen" (11x) / "ahí lo tenés" (7x)
- "espectacular" (8x)
- "la verdad eh" (3x)
- "voy a mentir" (10x)
- "qué les parece" (11x)
- "me gusta" (24x)
- "una cosa así" (8x)
- "gentle shell" (25x)
- "locura / locurita" (21x)
- "bien" (17x), "no" (10x), "eh" (7x), "sí" (5x), "gente" (3x)

## Mapeo audio-evento (resumen)

| Evento | Sonido | Frase propuesta |
|---|---|---|
| session.started | aldeanospawn | "Bienvenidos a otro stream..." |
| agent.started | priestconversion | "Vamos a ver magia, gente" |
| agent.completed | priestconverted | "espectacular / perfecto / correcto" |
| agent.failed | rogan | "No." / "La verdad, eh." |
| agent.cancelled | malesounddeath5 | "Así no más" |
| agent.attention | attack | "¿Qué les parece?" |
| subagent.queued | farmexhausted | "A ver..." |
| subagent.running | wololo | "Locura" |
| subagent.waiting | interface-population-limit | "Gente" / "Bien" |
| subagent.completed | aldeanospawn | "Ahí está / Ahí lo tienen / Ahí lo tenés" |
| subagent.failed | generic-male-death3 | "No." / "La verdad, eh." |
| subagent.cancelled | generic-female-death3 | "Así no más" |
| subagent.timed_out | generic-siege-weapon-death | "No más" / "La verdad, eh." |
| context.high | interface-town-bell1 | "Locura" / "Es una locura" |

## Herramienta de extracción

```bash
# Ver cues de una frase
python3 tools/extract_phrase.py --search "abuela"

# Extraer segmento por timestamp
python3 tools/extract_phrase.py 00:02:41,919 00:02:49,046 -o clips/mi_frase.mp3

# Extraer todas las ocurrencias
python3 tools/extract_phrase.py --search "abuela" --extract
```

## Notas

- Los subtítulos auto-generados tienen errores y cues solapados.
- El pairing frase↔evento es inferencia creativa, no evidencia registrada.
- Los archivos binarios pesados (audio.mp3, clips/, *.wav) no se versionan.
