"""
SVG Rendering & Surface Caching Pipeline for Case Unknown.

This module provides hardware-accelerated SVG rasterization with per-pixel alpha transparency
and an in-memory surface cache to ensure optimal 60 FPS performance.
"""

import io
import pygame

_SURFACE_CACHE = {}


def render_svg(svg_code: str, width: int = None, height: int = None) -> pygame.Surface:
    """
    Renders an SVG string into a Pygame Surface with per-pixel alpha transparency.
    Caches the resulting surface for optimal 60 FPS performance.
    """
    cache_key = (svg_code, width, height)
    if cache_key in _SURFACE_CACHE:
        return _SURFACE_CACHE[cache_key]

    svg_bytes = svg_code.encode("utf-8")
    bytes_io = io.BytesIO(svg_bytes)
    surface = pygame.image.load(bytes_io, "asset.svg")
    if pygame.display.get_surface() is not None:
        surface = surface.convert_alpha()

    # If dimensions requested differ from rendered surface size, smoothscale it
    if width is not None and height is not None:
        if surface.get_size() != (width, height):
            surface = pygame.transform.smoothscale(surface, (width, height))

    _SURFACE_CACHE[cache_key] = surface
    return surface
