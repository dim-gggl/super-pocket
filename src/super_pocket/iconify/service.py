"""
Module: super_pocket.iconify.service

Implémente la logique métier nécessaire pour générer une icône iOS avec
un masque de type squircle. Ce module ne contient aucune logique CLI :
il expose uniquement des fonctions pures ou quasi pures orientées image.

Dépendances : math, pathlib, Pillow
"""

import math
from pathlib import Path

from PIL import Image

DEFAULT_ICON_SIZE = 1024
DEFAULT_SUPERELLIPSE_EXPONENT = 5.0
MASK_BACKGROUND_VALUE = 0
MASK_FOREGROUND_VALUE = 255
TRANSPARENT_RGBA = (0, 0, 0, 0)


def generate_superellipse_mask(size: int,
                               exponent: float = DEFAULT_SUPERELLIPSE_EXPONENT) -> Image.Image:
    """
    Génère un masque de superellipse en niveaux de gris.

    Args:
        size (int): Largeur et hauteur du masque en pixels. Doit être > 0.
        exponent (float): Exposant de la superellipse. Doit être > 0.

    Returns:
        Image.Image: Image Pillow en mode `L` où la zone interne vaut 255
        et la zone externe vaut 0.

    Raises:
        ValueError: Si `size` ou `exponent` n'est pas strictement positif.
    """
    if size <= 0:
        raise ValueError("Icon size must be strictly positive.")

    if exponent <= 0:
        raise ValueError("Superellipse exponent must be strictly positive.")

    mask = Image.new("L", (size, size), color=MASK_BACKGROUND_VALUE)
    pixels = mask.load()

    if size == 1:
        pixels[0, 0] = MASK_FOREGROUND_VALUE
        return mask

    scale_denominator = size - 1

    for row_index in range(size):
        normalized_y = (2 * row_index / scale_denominator) - 1

        for column_index in range(size):
            normalized_x = (2 * column_index / scale_denominator) - 1
            distance = math.pow(abs(normalized_x), exponent) + math.pow(abs(normalized_y), exponent)

            if distance <= 1.0:
                pixels[column_index, row_index] = MASK_FOREGROUND_VALUE

    return mask


def iconify_image(input_path: str | Path,
                  output_path: str | Path,
                  size: int = DEFAULT_ICON_SIZE,
                  exponent: float = DEFAULT_SUPERELLIPSE_EXPONENT) -> Path:
    """
    Applique un masque squircle à une image et enregistre le PNG résultant.

    Args:
        input_path (str | Path): Chemin vers l'image source.
        output_path (str | Path): Chemin du fichier PNG à produire.
        size (int): Taille cible de l'icône carrée en pixels.
        exponent (float): Exposant utilisé pour le masque superellipse.

    Returns:
        Path: Chemin absolu du fichier généré.

    Raises:
        FileNotFoundError: Si l'image source n'existe pas.
        ValueError: Si `size` ou `exponent` n'est pas strictement positif.
        OSError: Si Pillow ne peut pas lire ou écrire l'image.
    """
    source_path = Path(input_path)
    destination_path = Path(output_path)

    if not source_path.exists():
        raise FileNotFoundError(f"Input image not found: {source_path}")

    mask = generate_superellipse_mask(size=size, exponent=exponent)
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(source_path) as source_image:
        square_image = source_image.convert("RGBA").resize((size, size), Image.LANCZOS)
        output_image = Image.new("RGBA", (size, size), TRANSPARENT_RGBA)
        output_image.paste(square_image, mask=mask)
        output_image.save(destination_path, format="PNG")

    return destination_path.resolve()
