"""
Assets package for Case Unknown.

Provides modular SVG vector assets, character animation generators, room furniture,
and the cached surface rendering pipeline.
"""

from assets.renderer import (
    _SURFACE_CACHE,
    render_svg,
)
from assets.characters import (
    CharacterPalette,
    DETECTIVE_PALETTE,
    get_character_animations,
)
from assets.props import (
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
    "_SURFACE_CACHE",
    "render_svg",
    "CharacterPalette",
    "DETECTIVE_PALETTE",
    "get_character_animations",
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
