"""
Module: super_pocket.iconify

Expose les primitives de génération d'icônes iOS au format squircle.
Le package contient la logique métier de masquage ainsi que la couche
CLI dédiée à la commande `pocket iconify`.
"""

from super_pocket.iconify.service import (
    DEFAULT_ICON_SIZE,
    DEFAULT_SUPERELLIPSE_EXPONENT,
    generate_superellipse_mask,
    iconify_image,
)

__all__ = [
    "DEFAULT_ICON_SIZE",
    "DEFAULT_SUPERELLIPSE_EXPONENT",
    "generate_superellipse_mask",
    "iconify_image",
]
