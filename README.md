# Flora Finder

Flora Finder is a command-line tool that helps you identify native plants suitable for your location (within Victoria, Australia).

Utilising the [Modelled 1750 Ecological Vegetation Class (EVC)](https://maps2.biodiversity.vic.gov.au/Html5viewer/) nearest your location, Flora Finder will query the [VicFlora GraphQL API](https://vicflora.rbg.vic.gov.au/apidocs/), and provide taxonomic information about the native flora identified in your EVC.

## Installation

### Prerequisites

- Python 3.11 or higher
- [Poetry](https://python-poetry.org/docs/)

### Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/LiamDavey/flora-finder.git
    cd flora-finder
    ```

2. Install dependencies:
    ```sh
    poetry install
    ```

3. Download SHP layer from [here](https://discover.data.vic.gov.au/dataset/native-vegetation-modelled-1750-ecological-vegetation-classes), and copy individual files into ./shp/ directory.

## Usage

### Basic Commands

1. **Convert a shapefile to a pickle file:**
    ```sh
    poetry run pickle-shp-file --input-file shp/NV1750_EVC.shp --output-file shp/nv1750_pickle.dat
    ```
    This command converts a shapefile into a pickled format for quicker access.

2. **Identify plants by geographical coordinates:**
    ```sh
    poetry run flora-finder --pickle-path shp/nv1750_pickle.dat --latitude -37.814 --longitude 144.96332
    ```
    This command will output URLs of native plants found within your EVC

### Help

For more information on how to use the commands, you can use the `--help` option:
```sh
poetry run flora-finder --help
poetry run pickle-shp-file --help
```

### Running Tests

```sh
poetry run pytest -rPsv tests/
``````
