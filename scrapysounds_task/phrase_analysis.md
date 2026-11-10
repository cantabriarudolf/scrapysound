# Análisis de frases — video "Te muestro la EVOLUCIÓN de Gentle Shell ! y... anuncio IMPORTANTE !"

- Video: https://www.youtube.com/watch?v=KTRoVbZeo3s
- Duración: ~02:05:13 (7512.92s)
- Subtítulos: `work/video/...es-orig.srt` (español original, auto-generados)
- Audio: `work/video/audio.mp3` (92 MB, mp3)

## Top palabras
que(588) es(413) no(394) de(387) lo(365) a(346) y(317) la(271) el(261) eh(251) bien(241) está(193) esto(184) un(173) sí(156) en(151) se(151) ahí(151) para(145) una(125) me(123) todo(120) ya(120) qué(117) por(117) ver(116) pero(116) más(110) con(102) así(101) te(100) gente(95) ahora(95) yo(90) acá(86) si(86) los(86) va(75) voy(72)

## Top bigramas (>=5)
lo que(103) a ver(86) voy a(60) vamos a(53) es que(53) es el(46) esto es(46) que es(41) va a(40) ahí está(40) es un(39) es una(31) ya está(30) que no(30) así no(29) ahí lo(29) la idea(26) no más(25) una cosa(25) gentle shell(25) ya lo(25) me gusta(24) es la(23) que se(23) no me(22) de la(21) van a(21) no se(21) la verdad(21) y ya(21)

## Top trigramas (>=4)
así no más(22) vamos a ver(14) este es el(14) es la idea(13) y ya está(13) van a ver(13) les voy a(11) qué les parece(11) todo lo que(11) es un poco(11) de lo que(11) es lo que(11) ahí lo tienen(11) lo que es(10) a ver qué(10) lo que vos(10) voy a mentir(10) te voy a(9) esto es un(9)

## Frases completas más repetidas (verbatim)
bien(17) no(10) espectacular(8) eh(7) ahí está(6) sí(5) o no(4) qué les parece(4) la verdad eh(3) bueno(3) a ver(3) perfecto(3) ahí va(3) mentir(3) correcto(3) así no más(3) gente(3)

## Muletillas / frases características del streamer
- "así no más"
- "ahí está" / "ahí lo tienen" / "ahí lo tenés"
- "espectacular"
- "la verdad eh"
- "voy a mentir" (frase recurrente antes de una afirmación)
- "qué les parece"
- "me gusta"
- "una cosa así"
- "gentle shell"

## Cómo extraer una frase del audio

Herramienta: `tools/extract_phrase.py`

```bash
# Ver en qué cues aparece una frase (con timestamps)
python3 tools/extract_phrase.py --search "abuela"

# Extraer un segmento por timestamp (inicio fin)
python3 tools/extract_phrase.py 00:02:41,919 00:02:49,046 -o work/video/clips/mi_frase.mp3

# Extraer TODAS las ocurrencias de una frase (con 0.3s de margen)
python3 tools/extract_phrase.py --search "abuela" --extract
# -> work/video/clips/001_...mp3, 002_...mp3, ...
```

Timestamps aceptan `HH:MM:SS,mmm`, `HH:MM:SS`, `MM:SS` o segundos (float).

## Ejemplo del usuario: "abuelaa" ~1:30:55
En ese timestamp el streamer habla de repos/packages ("Esto no es un package... es un project"), no dice "abuela".
Las ocurrencias reales de "abuela" están en 00:02:41, 00:08:27 y 00:08:42 (frase "Abuela, salió video de gente").
