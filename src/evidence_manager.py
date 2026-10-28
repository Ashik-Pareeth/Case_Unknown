"""
Evidence & Narrative Progression Engine for Case Unknown.

Strictly adheres to directives.txt:
- No conventional XP, levels, or rank points.
- Tracks evidence across states: Undiscovered -> Discovered -> Recorded -> Connected.
- Manages investigative Questions, Clue Connections, and Progression Gates.
- Provides subtle, non-intrusive atmospheric HUD notifications on journal updates.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import pygame
from src.settings import (
    SCREEN_WIDTH,
    UI_PANEL_BG,
    UI_PANEL_BORDER,
    UI_TEXT_TITLE,
    UI_TEXT_BODY,
    UI_TEXT_MUTED,
    UI_ACCENT_GOLD,
    UI_SUCCESS_GREEN,
)

# Evidence States (§2.2)
STATE_UNDISCOVERED = "undiscovered"
STATE_DISCOVERED = "discovered"
STATE_RECORDED = "recorded"
STATE_CONNECTED = "connected"

# Object Classifications (§5.2)
TYPE_ENVIRONMENTAL = "environmental"
TYPE_EXAMINABLE = "examinable"
TYPE_EVIDENCE = "evidence"


@dataclass
class EvidenceItem:
    id: str
    name: str
    room_id: str
    room_name: str
    short_desc: str
    full_text: str
    importance: str = "primary"  # "primary", "secondary", "context"
    state: str = STATE_UNDISCOVERED
    connected_to: list[str] = field(default_factory=list)


@dataclass
class InvestigationQuestion:
    id: str
    question: str
    lead: str
    resolved: bool = False
    required_evidence: list[str] = field(default_factory=list)


@dataclass
class EvidenceConnection:
    id: str
    title: str
    evidence_ids: list[str]
    deduction: str
    discovered: bool = False


@dataclass
class JournalToast:
    title: str
    subtitle: str
    timer: float = 3.6
    max_duration: float = 3.6


class EvidenceManager:
    """Core evidence tracking and narrative progression manager."""

    def __init__(self):
        self.evidence_db: dict[str, EvidenceItem] = {}
        self.questions: list[InvestigationQuestion] = []
        self.connections: list[EvidenceConnection] = []
        self.unlocked_gates: set[str] = set()
        self.found_keys: set[str] = set()

        # Toast notification system
        self.active_toast: JournalToast | None = None
        self.toast_queue: list[JournalToast] = []

        # Fonts
        pygame.font.init()
        self.font_title = pygame.font.SysFont("georgia", 14, bold=True)
        self.font_sub = pygame.font.SysFont("segoeui", 12)

        self._init_level1_narrative()

    def _init_level1_narrative(self):
        """Initializes default Level 1 investigative items and questions."""
        # Level 1 — Room 1 (The Crime Scene)
        self.register_evidence(
            EvidenceItem(
                id="hale_autopsy_report",
                name="Preliminary Incident Log — Martin Hale",
                room_id="crime_scene",
                room_name="The Crime Scene",
                short_desc="First responder dispatch noting Martin Hale found deceased at his desk.",
                full_text=(
                    "INCIDENT REPORT #4092\n"
                    "Subject: Martin Hale, Senior Archivist.\n"
                    "Found: Seated upright at study desk, sharp trauma to upper torso.\n"
                    "Status: Time of death estimated at 21:40. Office window latched from inside.\n"
                    "Note: Hale's personal diary is missing, but desk drawers remain locked."
                ),
                importance="primary",
            )
        )

        self.register_evidence(
            EvidenceItem(
                id="shattered_chronometer",
                name="Shattered Pocket Chronometer",
                room_id="crime_scene",
                room_name="The Crime Scene",
                short_desc="Gold pocket watch halted abruptly at 22:15, 35 minutes after estimated death.",
                full_text=(
                    "ARTIFACT EXAMINATION:\n"
                    "Heavy brass pocket watch found beneath the desk edge.\n"
                    "The casing was cracked by sudden blunt impact.\n"
                    "Hands are frozen at 22:15. Contradicts the 21:40 time of death in the initial dispatch."
                ),
                importance="secondary",
            )
        )

        # Level 1 — Room 2 (The Records Room)
        self.register_evidence(
            EvidenceItem(
                id="altered_archive_ledger",
                name="Altered Directorate Ledger Entry",
                room_id="records_room",
                room_name="The Records Room",
                short_desc="Official dispatch log with three dates systematically scrubbed with chemical solvent.",
                full_text=(
                    "DIRECTORATE DISPATCH LOG 1988-B:\n"
                    "Entries for October 12-14 show evident chemical erasure.\n"
                    "A faint carbon impression underneath reads: 'Requisition - Dossier Echo 4 - Voss, A.'\n"
                    "Someone altered official records prior to the detective squad arriving."
                ),
                importance="primary",
            )
        )

        # Level 1 — Room 3 (The Recording Room)
        self.register_evidence(
            EvidenceItem(
                id="hale_magnetic_tape",
                name="Damaged Dictaphone Reel — Hale's Final Memo",
                room_id="recording_room",
                room_name="The Recording Room",
                short_desc="Magnetic cassette recording fragments of Hale's voice referencing Project Echo.",
                full_text=(
                    "AUDIO TRANSCRIPT [REEL EXCERPT]:\n"
                    "HALE (audio raspy): '...if they seal the west archive, it's not to protect the data.\n"
                    "They are burying the personnel rosters. Adrian Voss signed the transfer order himself...\n"
                    "Nora tried to warn them. The town... they never even knew what was tested...'"
                ),
                importance="primary",
            )
        )

        # Level 1 — Room 4 (The Restricted Office)
        self.register_evidence(
            EvidenceItem(
                id="voss_authorization_slip",
                name="Executive Authorization Slip #88-C",
                room_id="restricted_office",
                room_name="The Restricted Office",
                short_desc="Official directive on Directorate letterhead with Adrian Voss's personal embossed seal.",
                full_text=(
                    "DIRECTORATE EXECUTIVE DIRECTIVE:\n"
                    "Authorized by: Adrian Voss, Operations Directorate.\n"
                    "Action: Immediate relocation of all Project Echo field journals to deep vault.\n"
                    "Mandate: No personnel outside Class-4 clearance may review Hale's historical files.\n"
                    "Signature verified: Adrian Voss."
                ),
                importance="primary",
            )
        )

        # Questions (§6)
        self.questions = [
            InvestigationQuestion(
                id="q_hale_timeline",
                question="Why does Hale's pocket watch contradict the medical dispatch timeline?",
                lead="Compare the broken chronometer with the first responder report.",
                required_evidence=["hale_autopsy_report", "shattered_chronometer"],
            ),
            InvestigationQuestion(
                id="q_altered_records",
                question="Who altered the Directorate ledgers and what was removed?",
                lead="Inspect the chemical erasure marks in the Records Room.",
                required_evidence=["altered_archive_ledger"],
            ),
            InvestigationQuestion(
                id="q_voss_involvement",
                question="What was Adrian Voss's direct role in Project Echo?",
                lead="Examine Voss's executive authorizations in the Restricted Office.",
                required_evidence=["hale_magnetic_tape", "voss_authorization_slip"],
            ),
        ]

        # Connections (§6)
        self.connections = [
            EvidenceConnection(
                id="conn_staged_timeline",
                title="Staged Crime Scene Timeline",
                evidence_ids=["hale_autopsy_report", "shattered_chronometer"],
                deduction="The 35-minute discrepancy proves someone broke the chronometer to falsify the murder window.",
            ),
            EvidenceConnection(
                id="conn_voss_coverup",
                title="Directorate Suppression Link",
                evidence_ids=["altered_archive_ledger", "voss_authorization_slip"],
                deduction="The erased requisition records match Adrian Voss's executive order sealing Project Echo.",
            ),
        ]

    def register_evidence(self, item: EvidenceItem):
        """Adds or updates an evidence item in the registry."""
        self.evidence_db[item.id] = item

    def get_evidence(self, item_id: str) -> EvidenceItem | None:
        return self.evidence_db.get(item_id)

    def is_recorded(self, item_id: str) -> bool:
        item = self.evidence_db.get(item_id)
        return item is not None and item.state in (STATE_RECORDED, STATE_CONNECTED)

    def record_evidence(self, item_id: str) -> bool:
        """
        Marks an item as RECORDED in the journal (§2.2).
        Guarantees no duplicate reward or entry.
        Returns True if newly recorded, False if already recorded.
        """
        item = self.evidence_db.get(item_id)
        if not item:
            return False

        if item.state in (STATE_RECORDED, STATE_CONNECTED):
            return False  # Already recorded, prevent duplicates (§9)

        item.state = STATE_RECORDED
        self._queue_toast(
            title="EVIDENCE RECORDED",
            subtitle=item.name,
        )

        # Check for connections & question progression
        self._evaluate_progress()
        return True

    def _evaluate_progress(self):
        """Checks connections and progression gates after evidence updates."""
        # Check connections
        for conn in self.connections:
            if not conn.discovered:
                all_recorded = all(self.is_recorded(e_id) for e_id in conn.evidence_ids)
                if all_recorded:
                    conn.discovered = True
                    for e_id in conn.evidence_ids:
                        if self.evidence_db[e_id].state == STATE_RECORDED:
                            self.evidence_db[e_id].state = STATE_CONNECTED
                    self._queue_toast(
                        title="NEW CLUE CONNECTION",
                        subtitle=conn.title,
                    )

        # Check questions resolution
        for q in self.questions:
            if not q.resolved and q.required_evidence:
                if all(self.is_recorded(e_id) for e_id in q.required_evidence):
                    q.resolved = True

        # Passage access is earned by finding keys and solving door mechanisms,
        # rather than by recording evidence.

    def is_gate_unlocked(self, gate_id: str) -> bool:
        """Returns True if the world progression gate is open."""
        return gate_id in self.unlocked_gates

    def collect_key(self, key_id: str) -> bool:
        """Record a discovered key and return whether it was newly found."""
        if key_id in self.found_keys:
            return False
        self.found_keys.add(key_id)
        return True

    def has_key(self, key_id: str) -> bool:
        return key_id in self.found_keys

    def get_recorded_items(self) -> list[EvidenceItem]:
        """Returns all evidence items that have been added to the journal."""
        return [
            item for item in self.evidence_db.values()
            if item.state in (STATE_RECORDED, STATE_CONNECTED)
        ]

    def get_discovered_connections(self) -> list[EvidenceConnection]:
        """Returns all resolved evidence connections."""
        return [conn for conn in self.connections if conn.discovered]

    def get_all_questions(self) -> list[InvestigationQuestion]:
        """Returns investigative leads."""
        return self.questions

    def _queue_toast(self, title: str, subtitle: str):
        toast = JournalToast(title=title, subtitle=subtitle)
        if self.active_toast is None:
            self.active_toast = toast
        else:
            self.toast_queue.append(toast)

    def update(self, dt: float):
        """Updates toast notification animations."""
        if self.active_toast:
            self.active_toast.timer -= dt
            if self.active_toast.timer <= 0:
                if self.toast_queue:
                    self.active_toast = self.toast_queue.pop(0)
                else:
                    self.active_toast = None

    def render_toast(self, surface: pygame.Surface):
        """Renders subtle, atmospheric journal notifications without XP bars."""
        if not self.active_toast:
            return

        toast = self.active_toast
        elapsed = toast.max_duration - toast.timer
        alpha = 255
        if elapsed < 0.35:
            alpha = int((elapsed / 0.35) * 255)
        elif toast.timer < 0.4:
            alpha = int((toast.timer / 0.4) * 255)
        alpha = max(0, min(255, alpha))

        w, h = 350, 58
        x = (SCREEN_WIDTH - w) // 2
        y = 18

        toast_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        # Background
        toast_surf.fill((*UI_PANEL_BG[:3], int(alpha * 0.94)))
        # Border
        pygame.draw.rect(toast_surf, (112, 112, 94, alpha), (0, 0, w, h), width=1, border_radius=5)
        pygame.draw.rect(toast_surf, (165, 137, 86, alpha), (0, 0, 3, h), border_top_left_radius=5, border_bottom_left_radius=5)
        pygame.draw.rect(toast_surf, (66, 75, 66, alpha), (13, 15, 24, 29), border_radius=2)
        pygame.draw.rect(toast_surf, (147, 157, 137, alpha), (13, 15, 24, 29), width=1, border_radius=2)
        pygame.draw.line(toast_surf, (147, 157, 137, alpha), (19, 22), (31, 22), 1)
        pygame.draw.line(toast_surf, (147, 157, 137, alpha), (19, 28), (31, 28), 1)
        pygame.draw.line(toast_surf, (147, 157, 137, alpha), (19, 34), (28, 34), 1)

        # Title
        title_surf = self.font_title.render(toast.title, True, (213, 194, 150))
        title_surf.set_alpha(alpha)
        toast_surf.blit(title_surf, (48, 8))

        # Subtitle
        sub_text = toast.subtitle
        if len(sub_text) > 46:
            sub_text = sub_text[:43] + "..."
        sub_surf = self.font_sub.render(sub_text, True, (184, 190, 179))
        sub_surf.set_alpha(alpha)
        sub_surf.blit(sub_surf, (48, 31))

        surface.blit(toast_surf, (x, y))

    def export_save_data(self) -> dict:
        """Returns JSON-serializable progression state (§9)."""
        return {
            "evidence": {
                item_id: item.state
                for item_id, item in self.evidence_db.items()
                if item.state != STATE_UNDISCOVERED
            },
            "unlocked_gates": list(self.unlocked_gates),
            "found_keys": list(self.found_keys),
            "connections": [c.id for c in self.connections if c.discovered],
        }

    def import_save_data(self, data: dict):
        """Restores state from save data."""
        evidence_dict = data.get("evidence", {})
        for item_id, state in evidence_dict.items():
            if item_id in self.evidence_db:
                self.evidence_db[item_id].state = state

        self.unlocked_gates = set(data.get("unlocked_gates", []))
        self.found_keys = set(data.get("found_keys", []))
        discovered_conns = set(data.get("connections", []))
        for c in self.connections:
            if c.id in discovered_conns:
                c.discovered = True
