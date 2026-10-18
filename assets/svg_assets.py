"""
Backward-compatibility facade for the assets package.

This module re-exports the rendering pipeline, character animations, room objects,
color palettes, and SVG string constants from the modular sub-packages:
- assets.renderer
- assets.characters
- assets.props

All existing imports across src/ and tests/ continue to work without modification.
"""

from assets.renderer import (
    _SURFACE_CACHE,
    render_svg,
)
from assets.characters import (
    CharacterPalette,
    DETECTIVE_PALETTE,
    _svg_character_defs,
    _generate_detective_down_svg,
    _generate_detective_up_svg,
    _generate_detective_side_svg,
    get_character_animations,
)
from assets.props import (
    _svg_cabinet_drawer,
    _svg_desk_pedestal_drawers,
    SVG_DETECTIVE_DESK,
    SVG_LEATHER_SOFA,
    SVG_FILING_CABINET,
    SVG_EVIDENCE_BOARD,
    SVG_BOOKSHELF,
    SVG_NOIR_WINDOW,
    SVG_VINTAGE_RUG,
    SVG_POTTED_PLANT,
    SVG_WALL_SCONCE,
    SVG_INTERACTION_BADGE,
    get_room_objects,
)

__all__ = [
    # Renderer
    "_SURFACE_CACHE",
    "render_svg",
    # Characters
    "CharacterPalette",
    "DETECTIVE_PALETTE",
    "_svg_character_defs",
    "_generate_detective_down_svg",
    "_generate_detective_up_svg",
    "_generate_detective_side_svg",
    "get_character_animations",
    # Props & Environment
    "_svg_cabinet_drawer",
    "_svg_desk_pedestal_drawers",
    "SVG_DETECTIVE_DESK",
    "SVG_LEATHER_SOFA",
    "SVG_FILING_CABINET",
    "SVG_EVIDENCE_BOARD",
    "SVG_BOOKSHELF",
    "SVG_NOIR_WINDOW",
    "SVG_VINTAGE_RUG",
    "SVG_POTTED_PLANT",
    "SVG_WALL_SCONCE",
    "SVG_INTERACTION_BADGE",
    "get_room_objects",
]
