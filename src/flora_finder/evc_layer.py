import time
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Self
import fiona
from shapely import Point, Polygon, STRtree
from shapely.geometry import shape


@dataclass
class EVCProperties:
    EVC_STUDY: int
    EVC: int
    EVCFC_UNIT: str
    SCALE: int
    EVC_SRC: int
    EVCFC: str
    EVCFC_DASH: str
    HECTARES: float
    EVC_GP: int
    EVC_SUBGP: float
    X_EVCNAME: str
    AREASQM: float
    XGROUPNAME: str
    X_EVCSTUDY: str
    X_EVCSRC: str
    XSUBGGROUP: str


@dataclass
class EVC:
    """
    Represents an Ecological Vegetation Class (EVC)
    """

    properties: EVCProperties
    polygon: Polygon

    def to_wkt(self) -> str:
        """
        Convert the EVC's polygon into WKT format
        """
        coords = self.polygon.exterior.coords
        if len(coords) < 3 or coords[0] != coords[-1]:
            raise ValueError(
                "The input is not a valid polygon. A polygon must have at least 3 points and should be closed."
            )

        wkt = "POLYGON (("
        wkt += ", ".join(f"{coord[0]} {coord[1]}" for coord in coords[:-1])
        wkt += f", {coords[-1][0]} {coords[-1][1]}"
        wkt += "))"

        return wkt


class EVCLayer:
    """
    Geospatial layer containing "Modelled 1750 Ecological Vegetation Classes".
    EVC polygons are stored in rtree for faster querying.
    Layer can be found at below link.
    https://discover.data.vic.gov.au/dataset/native-vegetation-modelled-1750-ecological-vegetation-classes
    """

    def __init__(self, evc_list: dict[int, EVC], strtree: STRtree):
        self.evc_list: list[EVC] = evc_list
        self.strtree: STRtree = strtree

    @classmethod
    def from_shapefile(cls, file_path: Path) -> Self:
        """
        Primary constructor given the path of a shapefile (.shp)
        """
        start_time = time.time()
        evc_list = []
        poly_list = []

        with fiona.open(file_path, "r") as shp:
            for evc in shp:
                polygon = shape(evc["geometry"])
                if isinstance(polygon, Polygon):
                    props = EVCProperties(**evc["properties"])
                    evc_list.append(EVC(properties=props, polygon=polygon))
                    poly_list.append(polygon)
            strtree = STRtree(poly_list)
            end_time = time.time()
            print(f"Processing time: {end_time - start_time} seconds")
            return cls(evc_list, strtree)

    def find_evc_containing_point(self, latitude, longitude) -> EVC | None:
        """
        Find the EVC polygon that contains the given point
        """
        point = Point(longitude, latitude)

        possible_matches_idx = self.strtree.query(point)

        for idx in possible_matches_idx:
            if self.evc_list[idx].polygon.contains(point):
                return self.evc_list[idx]

        return None

    def pickle(self, path: str) -> None:
        with open(path, "wb") as fp:
            pickle.dump(self, fp)

    @classmethod
    def from_pickle(cls, path: str) -> Self:
        start_time = time.time()
        with open(path, "rb") as fp:
            layer = pickle.load(fp)
            end_time = time.time()
            print(f"Processing time: {end_time - start_time} seconds")
            return layer
