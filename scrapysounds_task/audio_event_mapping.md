# Mapeo: Estados auditivos de Gentle Shell ↔ Frases reales del streamer

## Contexto
- Gentle Shell dispara 14 eventos de notificación, cada uno con un sonido (AoE) y un sprite.
- Fuente del mapeo oficial: `gentle-emote-arcade/sounds/aoe/seleccion.json` + `docs/MAPA-ESCENAS-aoe.md`
- Los sonidos se copiaron a `work/video/event_sounds/*.wav`
- Las frases del streamer (Gentleman Programming) provienen del video `https://www.youtube.com/watch?v=KTRoVbZeo3s` (subtítulos `...es-orig.srt`). Los clips están en `work/video/clips/<frase>/`.

> **Nota:** este pairing es una propuesta creativa/inferencia, no evidencia registrada. El streamer no mapeó explícitamente sus frases a los eventos.

## Tabla de mapeo propuesto

| # | Evento Gentle Shell | Sonido (AoE) | Significado del evento | Frase propuesta del streamer | Timestamp video | Clip |
|---|---|---|---|---|---|---|
| 1 | `session.started` | `aldeanospawn` | La sesión arranca (nace una unidad) | "Bienvenidos a otro stream impresionante de Genting" | 00:08:53 | `gentle_shell/` |
| 2 | `agent.started` | `priestconversion` | El modelo empieza a razonar | "Vamos a ver magia, gente" | 00:08:57 | `a_ver/` |
| 3 | `agent.completed` | `priestconverted` | Terminó bien (conversión consumada) | "Todo espectacular" / "Perfecto" / "Correcto" | 00:09:08 / 00:28:57 / 00:38:22 | `espectacular/` `perfecto/` `correcto/` |
| 4 | `agent.failed` | `rogan` | Algo falló ("¿Rogan?") | "No." / "La verdad, eh." | 00:01:43 / 00:34:51 | `no/` `la_verdad_eh/` |
| 5 | `agent.cancelled` | `malesounddeath5` | Cancelado (muerte masculina) | "Así no más" | 00:09:05 | `así_no_más/` |
| 6 | `agent.attention` | `attack` | Necesita intervención (cuerno de ataque) | "¿Qué les parece?" | 00:16:00 | `qué_les_parece/` |
| 7 | `subagent.queued` | `farmexhausted` | Subagente en cola (recurso agotado) | "A ver..." | 00:08:57 | `a_ver/` |
| 8 | `subagent.running` | `wololo` | Subagente corriendo (cántico) | "Locura" | 00:09:25 | `locura/` |
| 9 | `subagent.waiting` | `interface-population-limit` | Bloqueado, necesita acción | "Gente" / "Bien" | 00:02:41 / 00:01:43 | `gente/` `bien/` |
| 10 | `subagent.completed` | `aldeanospawn` | Subagente terminó (nacimiento) | "Ahí está" / "Ahí lo tienen" / "Ahí lo tenés" | 00:16:30 / 00:37:36 / 00:21:03 | `ahí_está/` `ahí_lo_tienen/` `ahí_lo_tenés/` |
| 11 | `subagent.failed` | `generic-male-death3` | Subagente falló (muerte) | "No." / "La verdad, eh." | 00:01:43 / 00:34:51 | `no/` `la_verdad_eh/` |
| 12 | `subagent.cancelled` | `generic-female-death3` | Subagente cancelado | "Así no más" | 00:09:05 | `así_no_más/` |
| 13 | `subagent.timed_out` | `generic-siege-weapon-death` | Se trabó (máquina rota) | "No más" / "La verdad, eh." | 00:01:43 / 00:34:51 | `no/` `la_verdad_eh/` |
| 14 | `context.high` | `interface-town-bell1` | Contexto al 90% (alarma del pueblo) | "Locura" / "Es una locura" | 00:09:25 / 00:33:52 | `locura/` |

## Muletillas del streamer (corpus completo)
Ver `phrase_analysis.md`. Las más características: "así no más", "ahí está/ahí lo tienen/ahí lo tenés", "espectacular", "la verdad eh", "voy a mentir", "qué les parece", "me gusta", "una cosa así", "gentle shell", "locura/locurita".

## Sonidos de eventos (copiados)
`work/video/event_sounds/` contiene los 14 wavs:
aldeanospawn, priestconversion, priestconverted, rogan, malesounddeath5, attack, farmexhausted, wololo, interface-population-limit, interface-town-bell1, generic-male-death3, generic-female-death3, generic-siege-weapon-death.

## Mi opinión
Es un proyecto muy creativo y coherente. El streamer ya tiene un vocabulario verbal muy marcado que encaja naturalmente con los estados del agente:

- **"espectacular / perfecto / correcto"** → `agent.completed`: el streamer dice estas palabras exactamente cuando algo salió bien en el stream.
- **"ahí está / ahí lo tienen / ahí lo tenés"** → `subagent.completed`: son frases de "mirá, ya está" que encajan con un subagente que terminó.
- **"así no más"** → cancelaciones: es la frase de cierre/cancelación del streamer.
- **"locura"** → `subagent.running` / `context.high`: el streamer dice "es una locura" cuando algo impresionante pasa.
- **"qué les parece"** → `agent.attention`: es la pregunta que hace cuando necesita input del chat.
- **"no" / "la verdad eh"** → failures: son reacciones de decepción.
- **"voy a mentir"** → podría ser un preámbulo antes de `agent.started` (anticipando lo que va a hacer).

**Sugerencia:** Si querés, puedo crear una "playlist" por evento que combine el sonido AoE + la frase del streamer en un solo audio (sonido + voz). O puedo generar un JSON con el mapeo completo para que Gentle Shell lo consuma. Decime qué preferís.
