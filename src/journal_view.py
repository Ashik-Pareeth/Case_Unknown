"""
Evidence Journal UI for Case Unknown.

Strictly adheres to directives.txt §6:
- Three simple sections:
  1. Evidence: Discovered items with names, room locations, descriptions, and transcripts.
  2. Connections: Grounded relationships between important clues.
  3. Current Questions: Short list of unresolved investigative leads.
- Minimal list-based clean vintage detective dossier design.
- Toggled via [J] or Tab / Pause Menu.
"""

from __future__ import annotations
import pygame
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    UI_PANEL_BG,
    UI_PANEL_BORDER,
    UI_TEXT_TITLE,
    UI_TEXT_BODY,
    UI_TEXT_MUTED,
    UI_ACCENT_GOLD,
    UI_SUCCESS_GREEN,
    UI_HIGHLIGHT_RED,
)
from src.evidence_manager import (
    EvidenceManager,
    EvidenceItem,
    STATE_RECORDED,
    STATE_CONNECTED,
)

TAB_EVIDENCE = 0
TAB_CONNECTIONS = 1
TAB_QUESTIONS = 2


class JournalView:
    """Renders the noir detective journal interface with 3 tabs."""

    def __init__(self, evidence_manager: EvidenceManager):
        self.evidence_manager = evidence_manager
        self.current_tab = TAB_EVIDENCE
        self.selected_evidence_index = 0
        self.selected_conn_index = 0
        self.selected_q_index = 0

        # Fonts
        pygame.font.init()
        self.font_header = pygame.font.SysFont("georgia", 20, bold=True)
        self.font_tab = pygame.font.SysFont("segoeui", 13, bold=True)
        self.font_item_title = pygame.font.SysFont("georgia", 14, bold=True)
        self.font_item_sub = pygame.font.SysFont("segoeui", 11)
        self.font_body = pygame.font.SysFont("segoeui", 13)
        self.font_doc = pygame.font.SysFont("consolas", 12)
        self.font_stamp = pygame.font.SysFont("segoeui", 11, bold=True)
        self.font_footer = pygame.font.SysFont("segoeui", 12)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Processes navigation and tab switching. Returns True if closed."""
        if event.type != pygame.KEYDOWN:
            return False

        if event.key in (pygame.K_j, pygame.K_ESCAPE):
            return True  # Signal to close journal

        # Tab switching: 1, 2, 3 or TAB
        if event.key == pygame.K_1:
            self.current_tab = TAB_EVIDENCE
        elif event.key == pygame.K_2:
            self.current_tab = TAB_CONNECTIONS
        elif event.key == pygame.K_3:
            self.current_tab = TAB_QUESTIONS
        elif event.key == pygame.K_TAB:
            self.current_tab = (self.current_tab + 1) % 3

        # Arrow key navigation
        elif event.key in (pygame.K_UP, pygame.K_w):
            if self.current_tab == TAB_EVIDENCE:
                items = self.evidence_manager.get_recorded_items()
                if items:
                    self.selected_evidence_index = (self.selected_evidence_index - 1) % len(items)
            elif self.current_tab == TAB_CONNECTIONS:
                conns = self.evidence_manager.get_discovered_connections()
                if conns:
                    self.selected_conn_index = (self.selected_conn_index - 1) % len(conns)
            elif self.current_tab == TAB_QUESTIONS:
                qs = self.evidence_manager.get_all_questions()
                if qs:
                    self.selected_q_index = (self.selected_q_index - 1) % len(qs)

        elif event.key in (pygame.K_DOWN, pygame.K_s):
            if self.current_tab == TAB_EVIDENCE:
                items = self.evidence_manager.get_recorded_items()
                if items:
                    self.selected_evidence_index = (self.selected_evidence_index + 1) % len(items)
            elif self.current_tab == TAB_CONNECTIONS:
                conns = self.evidence_manager.get_discovered_connections()
                if conns:
                    self.selected_conn_index = (self.selected_conn_index + 1) % len(conns)
            elif self.current_tab == TAB_QUESTIONS:
                qs = self.evidence_manager.get_all_questions()
                if qs:
                    self.selected_q_index = (self.selected_q_index + 1) % len(qs)

        return False

    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        lines = []
        for raw_line in text.split("\n"):
            words = raw_line.split(" ")
            cur_line = []
            for w in words:
                test_str = " ".join(cur_line + [w])
                if font.size(test_str)[0] <= max_width:
                    cur_line.append(w)
                else:
                    if cur_line:
                        lines.append(" ".join(cur_line))
                    cur_line = [w]
            if cur_line:
                lines.append(" ".join(cur_line))
        return lines

    def render(self, surface: pygame.Surface):
        """Draws the clean dossier journal window."""
        # Backdrop dim
        dim_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim_surf.fill((10, 12, 16, 210))
        surface.blit(dim_surf, (0, 0))

        # Main Journal Frame
        jw, jh = 860, 560
        jx = (SCREEN_WIDTH - jw) // 2
        jy = (SCREEN_HEIGHT - jh) // 2

        # Outer casing
        journal_surf = pygame.Surface((jw, jh), pygame.SRCALPHA)
        journal_surf.fill(UI_PANEL_BG)
        pygame.draw.rect(journal_surf, UI_PANEL_BORDER, (0, 0, jw, jh), 2, border_radius=6)
        pygame.draw.rect(journal_surf, (60, 50, 36), (4, 4, jw - 8, jh - 8), 1, border_radius=4)
        surface.blit(journal_surf, (jx, jy))

        # Header Title
        title_surf = self.font_header.render("INVESTIGATION JOURNAL — CASE DOSSIER", True, UI_TEXT_TITLE)
        surface.blit(title_surf, (jx + 30, jy + 20))

        # Subtitle / Case Name
        sub_surf = self.font_item_sub.render("PRECINCT 13 ARCHIVES • CLASSIFIED INQUIRY", True, UI_TEXT_MUTED)
        surface.blit(sub_surf, (jx + 32, jy + 46))

        # Top Tabs (§6)
        tab_y = jy + 68
        tab_w = 260
        tab_h = 34

        tabs_data = [
            (TAB_EVIDENCE, f"[1] DISCOVERED EVIDENCE ({len(self.evidence_manager.get_recorded_items())})"),
            (TAB_CONNECTIONS, f"[2] CLUE CONNECTIONS ({len(self.evidence_manager.get_discovered_connections())})"),
            (TAB_QUESTIONS, f"[3] ACTIVE LEADS ({sum(1 for q in self.evidence_manager.get_all_questions() if not q.resolved)})"),
        ]

        for i, (tab_id, label) in enumerate(tabs_data):
            tx = jx + 30 + i * (tab_w + 10)
            is_active = self.current_tab == tab_id
            bg_col = (34, 38, 46) if is_active else (20, 22, 28)
            border_col = UI_ACCENT_GOLD if is_active else (70, 75, 85)
            text_col = UI_ACCENT_GOLD if is_active else UI_TEXT_MUTED

            pygame.draw.rect(surface, bg_col, (tx, tab_y, tab_w, tab_h), border_radius=4)
            pygame.draw.rect(surface, border_col, (tx, tab_y, tab_w, tab_h), 1 if not is_active else 2, border_radius=4)

            t_text = self.font_tab.render(label, True, text_col)
            surface.blit(t_text, (tx + (tab_w - t_text.get_width()) // 2, tab_y + 8))

        # Divider below tabs
        content_y = tab_y + tab_h + 16
        pygame.draw.line(surface, UI_PANEL_BORDER, (jx + 30, content_y - 8), (jx + jw - 30, content_y - 8), 1)

        # Tab Content Area
        if self.current_tab == TAB_EVIDENCE:
            self._render_evidence_tab(surface, jx + 30, content_y, jw - 60, jh - (content_y - jy) - 45)
        elif self.current_tab == TAB_CONNECTIONS:
            self._render_connections_tab(surface, jx + 30, content_y, jw - 60, jh - (content_y - jy) - 45)
        elif self.current_tab == TAB_QUESTIONS:
            self._render_questions_tab(surface, jx + 30, content_y, jw - 60, jh - (content_y - jy) - 45)

        # Footer hints
        footer_text = "Press [1/2/3] or [TAB] to switch tabs • [↑/↓] Navigate • [J] or [ESC] Close Journal"
        footer_s = self.font_footer.render(footer_text, True, UI_TEXT_MUTED)
        surface.blit(footer_s, (jx + 30, jy + jh - 30))

    def _render_evidence_tab(self, surface: pygame.Surface, x: int, y: int, w: int, h: int):
        """Renders 2-column layout: Left = item list, Right = detailed record."""
        recorded_items = self.evidence_manager.get_recorded_items()

        if not recorded_items:
            empty_s = self.font_body.render("No evidence recorded yet. Explore rooms and examine suspicious objects [E].", True, UI_TEXT_MUTED)
            surface.blit(empty_s, (x + 20, y + 40))
            return

        list_w = 320
        detail_w = w - list_w - 20
        detail_x = x + list_w + 20

        # Left Column: Item List
        self.selected_evidence_index = max(0, min(self.selected_evidence_index, len(recorded_items) - 1))
        item_y = y
        for i, item in enumerate(recorded_items):
            is_sel = i == self.selected_evidence_index
            row_h = 60
            row_bg = (38, 42, 52) if is_sel else (24, 27, 34)
            row_border = UI_ACCENT_GOLD if is_sel else (55, 60, 70)

            pygame.draw.rect(surface, row_bg, (x, item_y, list_w, row_h), border_radius=4)
            pygame.draw.rect(surface, row_border, (x, item_y, list_w, row_h), 1 if not is_sel else 2, border_radius=4)

            # Left indicator bar
            if is_sel:
                pygame.draw.rect(surface, UI_ACCENT_GOLD, (x, item_y, 4, row_h), border_top_left_radius=4, border_bottom_left_radius=4)

            # Name
            name_s = self.font_item_title.render(item.name, True, UI_TEXT_TITLE if is_sel else UI_TEXT_BODY)
            surface.blit(name_s, (x + 14, item_y + 10))

            # Location & status
            loc_text = f"Found: {item.room_name}"
            loc_s = self.font_item_sub.render(loc_text, True, UI_TEXT_MUTED)
            surface.blit(loc_s, (x + 14, item_y + 34))

            status_text = "CONNECTED" if item.state == STATE_CONNECTED else "RECORDED"
            status_col = UI_SUCCESS_GREEN if item.state == STATE_CONNECTED else UI_ACCENT_GOLD
            stat_s = self.font_stamp.render(status_text, True, status_col)
            surface.blit(stat_s, (x + list_w - stat_s.get_width() - 12, item_y + 34))

            item_y += row_h + 8

        # Right Column: Detail Pane
        selected_item = recorded_items[self.selected_evidence_index]
        pygame.draw.rect(surface, (18, 20, 26), (detail_x, y, detail_w, h), border_radius=6)
        pygame.draw.rect(surface, (70, 65, 55), (detail_x, y, detail_w, h), 1, border_radius=6)

        # Title
        d_title = self.font_header.render(selected_item.name, True, UI_TEXT_TITLE)
        surface.blit(d_title, (detail_x + 20, y + 16))

        # Metadata row
        meta_str = f"Location: {selected_item.room_name}   |   Classification: {selected_item.importance.upper()} EVIDENCE"
        meta_s = self.font_item_sub.render(meta_str, True, UI_TEXT_MUTED)
        surface.blit(meta_s, (detail_x + 20, y + 44))

        pygame.draw.line(surface, (60, 55, 45), (detail_x + 20, y + 64), (detail_x + detail_w - 20, y + 64), 1)

        # Short summary
        desc_lines = self._wrap_text(selected_item.short_desc, self.font_body, detail_w - 40)
        curr_y = y + 74
        for d_line in desc_lines:
            line_s = self.font_body.render(d_line, True, UI_TEXT_BODY)
            surface.blit(line_s, (detail_x + 20, curr_y))
            curr_y += 20

        # Transcript box if available
        if selected_item.full_text:
            curr_y += 10
            t_box = pygame.Rect(detail_x + 20, curr_y, detail_w - 40, h - (curr_y - y) - 20)
            pygame.draw.rect(surface, (12, 14, 18), t_box, border_radius=4)
            pygame.draw.rect(surface, (70, 75, 85), t_box, 1, border_radius=4)
            pygame.draw.rect(surface, UI_ACCENT_GOLD, (t_box.x, t_box.y, 4, t_box.height), border_top_left_radius=4, border_bottom_left_radius=4)

            doc_lines = self._wrap_text(selected_item.full_text, self.font_doc, t_box.width - 24)
            ty = t_box.y + 12
            for dline in doc_lines:
                if ty + 18 > t_box.bottom - 8:
                    break
                ds = self.font_doc.render(dline, True, (220, 224, 230))
                surface.blit(ds, (t_box.x + 14, ty))
                ty += 18

    def _render_connections_tab(self, surface: pygame.Surface, x: int, y: int, w: int, h: int):
        """Renders recognized clue relationships grounded in evidence (§6)."""
        conns = self.evidence_manager.get_discovered_connections()

        if not conns:
            empty_title = self.font_item_title.render("No recognized clue connections yet.", True, UI_TEXT_MUTED)
            surface.blit(empty_title, (x + 20, y + 40))
            empty_sub = self.font_body.render("Compare records, timestamps, and witness reports across rooms to recognize contradictions.", True, UI_TEXT_BODY)
            surface.blit(empty_sub, (x + 20, y + 68))
            return

        cy = y
        for conn in conns:
            card_h = 100
            pygame.draw.rect(surface, (26, 30, 38), (x, cy, w, card_h), border_radius=6)
            pygame.draw.rect(surface, UI_ACCENT_GOLD, (x, cy, w, card_h), 1, border_radius=6)
            pygame.draw.rect(surface, UI_ACCENT_GOLD, (x, cy, 6, card_h), border_top_left_radius=6, border_bottom_left_radius=6)

            title_s = self.font_item_title.render(f"🔗 {conn.title}", True, UI_TEXT_TITLE)
            surface.blit(title_s, (x + 20, cy + 14))

            # Connected items tags
            items_str = "Linked Evidence: " + " & ".join(
                self.evidence_manager.get_evidence(eid).name if self.evidence_manager.get_evidence(eid) else eid
                for eid in conn.evidence_ids
            )
            item_s = self.font_item_sub.render(items_str, True, UI_TEXT_MUTED)
            surface.blit(item_s, (x + 20, cy + 38))

            # Deduction
            ded_s = self.font_body.render(f"Deduction: {conn.deduction}", True, UI_SUCCESS_GREEN)
            surface.blit(ded_s, (x + 20, cy + 62))

            cy += card_h + 16

    def _render_questions_tab(self, surface: pygame.Surface, x: int, y: int, w: int, h: int):
        """Renders active investigative leads (§6)."""
        questions = self.evidence_manager.get_all_questions()

        qy = y
        for q in questions:
            card_h = 74
            bg_col = (26, 30, 38) if not q.resolved else (20, 26, 22)
            border_col = (85, 90, 100) if not q.resolved else UI_SUCCESS_GREEN

            pygame.draw.rect(surface, bg_col, (x, qy, w, card_h), border_radius=4)
            pygame.draw.rect(surface, border_col, (x, qy, w, card_h), 1, border_radius=4)

            # Status Tag
            status_text = "RESOLVED" if q.resolved else "UNRESOLVED"
            status_col = UI_SUCCESS_GREEN if q.resolved else UI_HIGHLIGHT_RED
            tag_s = self.font_stamp.render(f"[{status_text}]", True, status_col)
            surface.blit(tag_s, (x + 16, qy + 14))

            # Question Text
            q_s = self.font_item_title.render(q.question, True, UI_TEXT_BODY)
            surface.blit(q_s, (x + 115, qy + 13))

            # Lead hint
            lead_s = self.font_item_sub.render(f"Investigative Lead: {q.lead}", True, UI_TEXT_MUTED)
            surface.blit(lead_s, (x + 20, qy + 44))

            qy += card_h + 12
