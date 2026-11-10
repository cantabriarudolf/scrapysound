import json
import pytest
from scrapysound import integration


def test_validate_event_ok():
    assert integration.validate_event("agent.completed") == "agent.completed"


def test_validate_event_bad():
    with pytest.raises(ValueError):
        integration.validate_event("nope")


def test_register_dry_run(tmp_path):
    cfg = tmp_path / "notifications.json"
    cfg.write_text(json.dumps({"agent.completed": "file:/old.wav"}), encoding="utf-8")
    clip = tmp_path / "clip.mp3"
    clip.write_text("x", encoding="utf-8")
    old, new = integration.register_clip_as_notification(
        str(clip), "agent.completed", config_path=str(cfg), dry_run=True)
    assert old == "file:/old.wav"
    assert new.endswith("clip.mp3")
    # dry-run does not write
    assert json.loads(cfg.read_text(encoding="utf-8"))["agent.completed"] == "file:/old.wav"


def test_register_writes_and_backs_up(tmp_path):
    cfg = tmp_path / "notifications.json"
    cfg.write_text(json.dumps({"events": {"agent.completed": "file:/old.wav"}}),
                   encoding="utf-8")
    clip = tmp_path / "clip.mp3"
    clip.write_text("x", encoding="utf-8")
    old, new = integration.register_clip_as_notification(
        str(clip), "agent.completed", config_path=str(cfg))
    assert old == "file:/old.wav"
    data = json.loads(cfg.read_text(encoding="utf-8"))
    assert data["events"]["agent.completed"] == new
    backups = list(tmp_path.glob("notifications.json.bak-*"))
    assert len(backups) == 1
