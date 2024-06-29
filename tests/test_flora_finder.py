from flora_finder.cli import taxon_in_wkt
from flora_finder.evc_layer import EVCLayer


def test_taxon_in_wkt():
    wkt = "POLYGON ((144.637916 -38.192121, 144.637916 -38.180922, 144.657824 -38.180922, 144.657824 -38.192121, 144.637916 -38.192121))"
    taxons = taxon_in_wkt(wkt)
    print(taxons)


def test_evc_layer():
    shapefile_path = "shp/NV1750_EVC.shp"
    evc_layer = EVCLayer.from_shapefile(shapefile_path)
    evc = evc_layer.find_evc_containing_point(-36.45954, 146.13957)
    print(evc.to_wkt())
