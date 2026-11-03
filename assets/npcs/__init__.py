"""Reusable character art for non-player characters.

Exports:
  get_npc_animations(palette_index) – cached animation dict for each NPC type.
    0 → Mob Grunt         (cartoon oval mob, black overcoat, full balaclava)
    1 → The Fixer         (inner-room schemer; detective rig, navy suit, cigar)
    2 → Mob Grunt Alt     (same cartoon mob, slightly different coat shade)

  NPC_PALETTES – tuple of CharacterPalette or None (None for custom-SVG types).
  NPC_NAMES    – human-readable name strings.
  FIXER_PALETTE – the palette used by The Fixer (index 1).
"""

from assets.npcs.characters import (
    NPC_PALETTES,
    NPC_NAMES,
    FIXER_PALETTE,
    get_npc_animations,
)

__all__ = [
    "NPC_PALETTES",
    "NPC_NAMES",
    "FIXER_PALETTE",
    "get_npc_animations",
]
