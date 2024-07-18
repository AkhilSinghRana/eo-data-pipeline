# eo_data_pipeline/pipeline/flow.py
from prefect import flow, task
from eo_data_pipeline.data_fetcher.fetcher import DataFetcher
from eo_data_pipeline.data_fetcher.validator import ParameterValidator
from eo_data_pipeline.data_loader.loader import DataLoader
from eo_data_pipeline.config.config_schema import Config
import logging

@task
def validate_inputs(config: Config):
    ParameterValidator.validate_time_range(
        [config.pipeline.time_steps.start, config.pipeline.time_steps.end]
    )
    ParameterValidator.validate_aoi(config.pipeline.aoi)
    ParameterValidator.validate_spectral_bands(config.pipeline.spectral_bands)


@task
def fetch_data(config: Config):
    fetcher = DataFetcher(config)
    items = fetcher.fetch_data(
        [config.pipeline.time_steps.start, config.pipeline.time_steps.end],
        config.pipeline.aoi,
        config.pipeline.spectral_bands,
    )
    
    logging.info(f"Fetched {len(items)} items")

    return items

@task
def load_data(config: Config, items):
    loader = DataLoader(config)
    return loader.load_data(items, config.pipeline.spectral_bands)


@flow
def eo_pipeline(config: Config):
    logging.info("Starting the EO pipeline...")
    validate_inputs(config)
    items = fetch_data(config)
    saved_files = load_data(config, items)
    logging.info(f"Pipeline finished, saved files: {saved_files}")

    return saved_files


def run_pipeline(config: Config):
    return eo_pipeline(config)
