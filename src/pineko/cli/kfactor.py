"""CLI entry point to generation of the inclusion of kfactor in a grid."""

import pathlib

import click

from .. import kfactor
from ._base import command


@command.command("kfactor")
@click.argument("grids_folder", type=click.Path(exists=True))
@click.argument("kfactor_folder", type=click.Path(exists=True))
@click.argument("yamldb_file", type=click.Path(exists=True))
@click.argument("target_folder", type=click.Path(exists=True))
@click.argument("pto_to_update", type=int)
@click.option("--order_exists", is_flag=True, help="Overwrite an existing order.")
def k_factor_inclusion(
    grids_folder,
    kfactor_folder,
    yamldb_file,
    target_folder,
    pto_to_update,
    order_exists,
):
    """Construct new grid with k_factor included."""
    grids_folder = pathlib.Path(grids_folder)
    kfactor_folder = pathlib.Path(kfactor_folder)
    yamldb_file = pathlib.Path(yamldb_file)
    target_folder = pathlib.Path(target_folder)
    kfactor.compute_k_factor_grid(
        grids_folder,
        kfactor_folder,
        yamldb_file,
        pto_to_update,
        target_folder=target_folder,
        order_exists=order_exists,
    )
