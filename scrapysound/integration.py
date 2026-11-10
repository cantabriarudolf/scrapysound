"""Register scrapysound clips as Gentle Shell notification sounds. Powered by Gentle Shell."""
import json
import os
import shutil
import time

KNOWN_EVENTS = [
    "session.started",
    "agent.started",
    "agent.completed",
    "agent.failed",
    "agent.cancelled",
    "agent.attention",
    "subagent.queued",
    "subagent.running",
    "subagent.waiting",
    "subagent.completed",
    "subagent.failed",
    "subagent.cancelled",
    "subagent.timed_out",
    "context.high",
]

DEFAULT_CONFIG = os.path.expanduser("~/.gentle-shell/config/gentle-ai/notifications.json")


def validate_event(event):
    if event not in KNOWN_EVENTS:
        raise ValueError(f"Unknown event {event!r}. Known: {', '.join(KNOWN_EVENTS)}")
    return event


def register_clip_as_notification(clip_path, event, config_path=None, dry_run=False):
    """Point a Gentle Shell notification event at a scrapysound clip.

    Returns (old_value, new_value). Backs up config before writing.
    """
    validate_event(event)
    cfg = config_path or DEFAULT_CONFIG
    if not os.path.exists(clip_path):
        raise FileNotFoundError(f"Clip not found: {clip_path}")
    new_value = "file:" + os.path.abspath(clip_path)
    if not os.path.exists(cfg):
        raise FileNotFoundError(f"notifications.json not found: {cfg}")
    with open(cfg, encoding="utf-8") as f:
        data = json.load(f)
    # support both flat {event: sound} and nested {events: {...}} shapes
    if "events" in data and isinstance(data["events"], dict):
        old_value = data["events"].get(event)
    else:
        old_value = data.get(event)
    if dry_run:
        return old_value, new_value
    backup = f"{cfg}.bak-{time.strftime('%Y%m%d-%H%M%S')}"
    shutil.copy2(cfg, backup)
    if "events" in data and isinstance(data["events"], dict):
        data["events"][event] = new_value
    else:
        data[event] = new_value
    with open(cfg, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return old_value, new_value
