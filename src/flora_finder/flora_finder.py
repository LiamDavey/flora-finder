import httpx
from enum import StrEnum
from dataclasses import dataclass


class EstablishmentMeans(StrEnum):
    NATIVE = "NATIVE"
    NATIVE_REINTRODUCED = "NATIVE_REINTRODUCED"
    INTRODUCED = "INTRODUCED"
    UNCERTAIN = "UNCERTAIN"


class CurrentProfile:
    profile: str


@dataclass
class TaxonName:
    rank: str
    fullName: str


@dataclass
class TaxonConcept:
    taxonName: TaxonName
    establishmentMeans: EstablishmentMeans
    id: str
    currentProfile: CurrentProfile


def query_flora_api(query: str, variables: dict = {}):
    """
    Wraps HTTP client for super simple interface.
    Returns .json() response
    """

    url = "https://vicflora.rbg.vic.gov.au/graphql"

    try:
        response = httpx.post(
            url, json={"query": query, "variables": variables}, timeout=10
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise e
    except httpx.HTTPError as e:
        raise e
    data = response.json()
    return data


def taxon_in_wkt(wkt: str, first: int = 10) -> list[TaxonConcept]:
    """
    Return list of taxons found within the given WKT (Well Known Text)
    """
    query = """
    query findTaxons($wkt: String!, $first: Int, $page: Int) {
        taxonConceptsByWkt(wkt: $wkt, first: $first, page: $page){
            paginatorInfo{
                hasMorePages
            }
            data{
                taxonName{
                    rank
                    fullName
                }
                establishmentMeans
                id
                currentProfile{
                    profile
                }
            }
        }
    }
    """

    taxons = []
    page = 1
    while True:
        variables = dict(wkt=wkt, first=first, page=page)
        response = query_flora_api(query, variables)
        data = response["data"]["taxonConceptsByWkt"]["data"]
        if not data:
            break
        for taxon in data:
            taxons.append(TaxonConcept(**taxon))
        if response["data"]["taxonConceptsByWkt"]["paginatorInfo"]["hasMorePages"]:
            page += 1
        else:
            break
    return taxons
