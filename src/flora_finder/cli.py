import click

from .evc_layer import EVCLayer
from .flora_finder import taxon_in_wkt, EstablishmentMeans


@click.command()
@click.option(
    "--pickle-path",
    default="shp/nv1750_pickle.dat",
    help="Path of pickled evc layer",
    show_default=True,
)
@click.option(
    "--latitude", required=True, type=float, help="Latitude in decimal degrees"
)
@click.option(
    "--longitude", required=True, type=float, help="Longitude in decimal degrees"
)
def cli(pickle_path, latitude, longitude):
    evc_layer = EVCLayer.from_pickle(pickle_path)
    if evc := evc_layer.find_evc_containing_point(latitude, longitude):
        taxons = taxon_in_wkt(evc.to_wkt())
        for taxon in taxons:
            if taxon.establishmentMeans == EstablishmentMeans.NATIVE:
                click.echo(f"https://vicflora.rbg.vic.gov.au/flora/taxon/{taxon.id}")
    else:
        click.echo("No polygon found containing the point.")


@click.command()
@click.option(
    "--input-file",
    default="shp/NV1750_EVC.shp",
    help="Path of .shp layer file",
    show_default=True,
)
@click.option(
    "--output-file",
    default="shp/nv1750_pickle.dat",
    help="Path of resulting pickle file",
)
def pickle_shp_file(input_file, output_file):
    """
    Creates EVCLayer from .shp file and pickles the resulting object
    """
    click.echo(f"Loading {input_file} file, this may take a few minutes...")
    evc_layer = EVCLayer.from_shapefile(input_file)
    click.echo("Pickling...")
    evc_layer.pickle(output_file)
    click.echo(f"{output_file} created!")
