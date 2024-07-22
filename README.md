
---

## GitHub Workflows Status

| Workflow | Status |
| --- | --- |
| Tests | [![Tests](https://github.com/AkhilSinghRana/eo-data-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/AkhilSinghRana/eo-data-pipeline/actions/workflows/ci.yml) |

---

# EO Data Pipeline

The EO Data Pipeline is a Python package for generating data pipelines to fetch Earth Observation (EO) data from the EarthSearchCatalog.

## Features

- Fetches data from EarthSearchCatalog based on user-defined search parameters
- Stores raw data and metadata in a local directory structure
- Metadata follows the pySTAC format

## Requirements

- Python 3.12+
- Poetry

## Installation

1. Install Poetry if you haven't already:

    ```curl -sSL https://install.python-poetry.org | python3 -```

2. Clone this repository:

    ```git clone https://github.com/your-username/eo-data-pipeline.git```


3. Change to the project directory:

    ```cd eo-data-pipeline```

4. Install the package dependencies using Poetry:

    ```poetry install```


If you want to install development dependencies, use:
    
    poetry install --with dev


## Usage

1. Modify the configuration file `eo_data_pipeline/config/hydra_config.yaml` to specify your search parameters, such as the area of interest, time range, and spectral bands.
2. Run the pipeline script:
python scripts/run_pipeline.py

The pipeline will fetch the data from EarthSearchCatalog and store it in the `data` directory. Raw images will be stored in `data/raw` and metadata in `data/catalog_metadata`.
3. Check the output of the pipeline in the `output` directory.

## Notebooks

You can find helper notebooks in the `notebooks` directory to visualize and analyze the data.

## Contributing

We welcome contributions to the EO Data Pipeline! Please see our [contributing guidelines](CONTRIBUTING.md) (*To be added) for more information.

