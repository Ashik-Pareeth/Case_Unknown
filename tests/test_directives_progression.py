"""
Automated headless test suite validating directives.txt specifications:
- Progression through narrative understanding and world unlocking (no RPG XP).
- Evidence states: Undiscovered -> Recorded -> Connected.
- Prevention of duplicate evidence records (§9).
- Clue connections and question resolutions (§6).
- Level 1 room layouts, furniture, and interactables (§4).
- Progression gates unlocking doors upon recording required clues (§2.3, §7).
- Evidence Journal 3-tab navigation and rendering (§6).
- Local JSON save and load persistence (§9).
"""

import os
import sys

# Ensure headless execution
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.evidence_manager import (
    EvidenceManager,
    STATE_UNDISCOVERED,
    STATE_RECORDED,
    STATE_CONNECTED,
    TYPE_EVIDENCE,
)
from src.interaction import InteractionManager
from src.room import Room
from src.rooms_data import ROOMS_DATA
from src.journal_view import JournalView, TAB_EVIDENCE, TAB_CONNECTIONS, TAB_QUESTIONS
from src.save_manager import SaveManager
from src.player import Player


def test_evidence_states_and_no_duplicates():
    """Verify evidence state transitions and prevention of duplicate awards (§2.2, §9)."""
    mgr = EvidenceManager()
    item_id = "hale_autopsy_report"

    # Initially undiscovered
    item = mgr.get_evidence(item_id)
    assert item is not None
    assert item.state == STATE_UNDISCOVERED
    assert not mgr.is_recorded(item_id)

    # First recording succeeds
    recorded = mgr.record_evidence(item_id)
    assert recorded is True
    assert mgr.is_recorded(item_id)
    assert len(mgr.get_recorded_items()) == 1

    # Second recording attempt is blocked (no duplicate)
    duplicate_recorded = mgr.record_evidence(item_id)
    assert duplicate_recorded is False
    assert len(mgr.get_recorded_items()) == 1


def test_clue_connections_and_lead_resolution():
    """Verify that discovering related clues creates connections and resolves leads (§6)."""
    mgr = EvidenceManager()

    # Before collecting clues
    assert len(mgr.get_discovered_connections()) == 0
    q_timeline = next(q for q in mgr.get_all_questions() if q.id == "q_hale_timeline")
    assert q_timeline.resolved is False

    # Record first clue
    mgr.record_evidence("hale_autopsy_report")
    assert len(mgr.get_discovered_connections()) == 0
    assert q_timeline.resolved is False

    # Record contradicting clue
    mgr.record_evidence("shattered_chronometer")

    # Connection should now be recognized
    conns = mgr.get_discovered_connections()
    assert len(conns) >= 1
    assert any(c.id == "conn_staged_timeline" for c in conns)
    assert q_timeline.resolved is True

    # Evidence states should now be CONNECTED
    assert mgr.get_evidence("hale_autopsy_report").state == STATE_CONNECTED
    assert mgr.get_evidence("shattered_chronometer").state == STATE_CONNECTED


def test_level1_room_blueprints_and_furniture():
    """Verify all 4 Level 1 rooms instantiate with valid furniture and solid collisions (§4)."""
    pygame.init()
    pygame.display.set_mode((1, 1))

    level1_rooms = ["crime_scene", "records_room", "recording_room", "restricted_office"]
    interaction_mgr = InteractionManager()

    for r_id in level1_rooms:
        assert r_id in ROOMS_DATA
        room = Room(interaction_mgr, r_id, ROOMS_DATA[r_id])
        assert room.room_id == r_id
        assert len(room.solid_objects) >= 4
        assert len(room.furniture_items) >= 2


def test_progression_gates_and_room_unlocking():
    """Verify doors are gated until key evidence is recorded in journal (§2.3, §7, §12)."""
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    evidence_mgr = EvidenceManager()
    interaction_mgr = InteractionManager(evidence_mgr)

    # 1. Start in Room 1: The Crime Scene
    room = Room(interaction_mgr, "crime_scene", ROOMS_DATA["crime_scene"], evidence_mgr=evidence_mgr)

    # Exit door to records room is on the right wall
    exit_door = next(d for d in room.doorways if d["wall"] == "right")
    assert exit_door["gate_id"] == "door_crime_scene_to_records"

    # Player reaches door without recording evidence -> Gate BLOCKS passage
    player_hitbox = exit_door["trigger_rect"].copy()
    transition = room.check_door_transitions(player_hitbox)
    assert transition is not None
    assert transition.get("blocked") is True

    # Player inspects and records Martin Hale's desk report
    interaction_mgr.add_object(
        obj_id="hale_desk",
        name="Martin Hale's Study Desk",
        description="Desk",
        trigger_rect=pygame.Rect(0, 0, 10, 10),
        badge_pos=(0, 0),
        obj_type=TYPE_EVIDENCE,
        evidence_id="hale_autopsy_report",
    )
    evidence_mgr.record_evidence("hale_autopsy_report")
    assert evidence_mgr.is_gate_unlocked("door_crime_scene_to_records") is True

    # Now player approaches the door again -> Gate allows passage!
    transition_after = room.check_door_transitions(player_hitbox)
    assert transition_after is not None
    assert transition_after.get("blocked") is not True
    assert transition_after["target_room"] == "records_room"


def test_journal_view_tabs_and_rendering():
    """Verify JournalView renders all 3 tabs without graphical errors (§6)."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    evidence_mgr = EvidenceManager()
    evidence_mgr.record_evidence("hale_autopsy_report")
    evidence_mgr.record_evidence("shattered_chronometer")

    journal = JournalView(evidence_mgr)

    # Test tab navigation
    assert journal.current_tab == TAB_EVIDENCE
    event_tab = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_TAB})
    journal.handle_event(event_tab)
    assert journal.current_tab == TAB_CONNECTIONS

    event_3 = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_3})
    journal.handle_event(event_3)
    assert journal.current_tab == TAB_QUESTIONS

    # Render each tab
    for tab in (TAB_EVIDENCE, TAB_CONNECTIONS, TAB_QUESTIONS):
        journal.current_tab = tab
        journal.render(screen)


def test_save_and_load_persistence(tmp_path=None):
    """Verify local JSON persistence of room, player position, and evidence states (§9)."""
    test_save_file = "test_save_game.json"
    save_mgr = SaveManager(test_save_file)

    try:
        # Create and advance progress
        mgr1 = EvidenceManager()
        mgr1.record_evidence("hale_autopsy_report")
        mgr1.record_evidence("shattered_chronometer")

        saved = save_mgr.save_game(
            current_room_id="records_room",
            player_pos=(250.0, 360.0),
            visited_rooms={"crime_scene", "records_room"},
            evidence_mgr=mgr1,
            level=1,
        )
        assert saved is True
        assert save_mgr.has_save() is True

        # Load in a fresh EvidenceManager
        mgr2 = EvidenceManager()
        assert not mgr2.is_recorded("hale_autopsy_report")

        loaded = save_mgr.load_game(mgr2)
        assert loaded is not None
        assert loaded["current_room_id"] == "records_room"
        assert loaded["player_pos"] == (250.0, 360.0)
        assert "records_room" in loaded["visited_rooms"]

        # Evidence and connections must be restored exactly
        assert mgr2.is_recorded("hale_autopsy_report") is True
        assert mgr2.is_gate_unlocked("door_crime_scene_to_records") is True
        assert len(mgr2.get_discovered_connections()) >= 1

    finally:
        save_mgr.delete_save()


if __name__ == "__main__":
    test_evidence_states_and_no_duplicates()
    test_clue_connections_and_lead_resolution()
    test_level1_room_blueprints_and_furniture()
    test_progression_gates_and_room_unlocking()
    test_journal_view_tabs_and_rendering()
    test_save_and_load_persistence()
    print("ALL DIRECTIVES TESTS PASSED SUCCESSFULLY!")
