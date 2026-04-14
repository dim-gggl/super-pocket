"""
Module: super_pocket.iconify.cli

Expose la commande CLI `pocket iconify`. Cette couche adapte les entrées
utilisateur en appelant le service de génération d'icône sans y mélanger
la logique métier.

Dépendances : rich-click, pathlib, super_pocket.iconify.service
"""

from pathlib import Path

from super_pocket.iconify.service import (
    DEFAULT_ICON_SIZE,
    DEFAULT_SUPERELLIPSE_EXPONENT,
    iconify_image,
)
from super_pocket.settings import CONTEXT_SETTINGS, add_help_argument, click
from super_pocket.utils import console


@click.command(name="iconify", context_settings=CONTEXT_SETTINGS)
@click.option("-i",
              "--input",
              "input_path",
              required=True,
              type=click.Path(exists=True, dir_okay=False, path_type=Path),
              help="Source image to transform into an iOS squircle icon.")
@click.option("-o",
              "--output",
              "output_path",
              required=True,
              type=click.Path(dir_okay=False, path_type=Path),
              help="Destination PNG path.")
@click.option("-s",
              "--size",
              type=int,
              default=DEFAULT_ICON_SIZE,
              show_default=True,
              help="Target square icon size in pixels.")
@click.option("-e",
              "--exponent",
              type=float,
              default=DEFAULT_SUPERELLIPSE_EXPONENT,
              show_default=True,
              help="Superellipse exponent used to shape the squircle.")
def iconify_cli(input_path: Path,
                output_path: Path,
                size: int,
                exponent: float) -> None:
    """
    Génère une icône iOS au format squircle à partir d'une image source.

    Args:
        input_path (Path): Chemin du fichier source à convertir.
        output_path (Path): Chemin du PNG de sortie.
        size (int): Taille carrée de l'icône finale.
        exponent (float): Exposant de la superellipse.

    Raises:
        click.BadParameter: Si les paramètres numériques sont invalides.
        click.ClickException: Si la génération échoue.
    """
    try:
        generated_path = iconify_image(input_path=input_path,
                                       output_path=output_path,
                                       size=size,
                                       exponent=exponent)
    except ValueError as exc:
        raise click.BadParameter(str(exc)) from exc
    except FileNotFoundError as exc:
        raise click.ClickException(str(exc)) from exc
    except OSError as exc:
        raise click.ClickException(f"Unable to generate icon: {exc}") from exc

    console.print(
        f"[green]✓[/green] Squircle icon generated at '{generated_path}'",
        style="bold"
    )


add_help_argument(iconify_cli)
