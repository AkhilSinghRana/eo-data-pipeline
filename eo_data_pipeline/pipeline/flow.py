import logging

from prefect import flow, task

from eo_data_pipeline.config.config_schema import Config
from eo_data_pipeline.data_fetcher.fetcher import DataFetcher
from eo_data_pipeline.data_fetcher.validator import ParameterValidator
from eo_data_pipeline.data_loader.loader import DataLoader


@task(name="Validate Inputs", log_prints=True)
def validate_inputs(config: Config):
    ParameterValidator.validate_time_range(
        [config.pipeline.time_steps.start, config.pipeline.time_steps.end]
    )
    ParameterValidator.validate_aoi(config.pipeline.aoi)
    ParameterValidator.validate_spectral_bands(config.pipeline.spectral_bands)


@task(name="Fetch Data", log_prints=True)
def fetch_data(config: Config):
    fetcher = DataFetcher(config)
    items = fetcher.fetch_data(
        [config.pipeline.time_steps.start, config.pipeline.time_steps.end],
        config.pipeline.aoi,
        config.pipeline.spectral_bands,
    )

    logging.info(f"Fetched {len(items)} items")
    return items


@task(name="save Metadata", log_prints=True)
def save_metadata(config: Config, items):
    print("Saving metadta")
    loader = DataLoader(config)
    loader.save_metadata(items=items)
    return items


@task(name="Load and Process Data", log_prints=True, retries=3)
def load_data(config: Config, item):
    loader = DataLoader(config)
    return loader.load_data([item], config.pipeline.spectral_bands)


@task
def process_data(config: Config, saved_files: list):
    # Process the data into netcdf for faster read during downstream applications
    # TO-DO for later
    pass


@flow(name="Earth Observation Pipeline")
def eo_pipeline(config: Config):
    logging.info("Starting the EO pipeline...")
    validate_inputs(config)
    items = fetch_data(config)
    items = save_metadata(config, items)

    # Run load_data concurrently for each item
    saved_files = load_data.map(config=config, item=items)

    logging.info(f"Pipeline finished, saved files: {saved_files}")
    return saved_files


# Function to run the flow locally
def run_pipeline(config: Config):
    return eo_pipeline(config)
