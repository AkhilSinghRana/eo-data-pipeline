# eo_data_pipeline/config/config_schema.py
from dataclasses import dataclass, field
from typing import List


@dataclass
class EarthSearchConfig:
    url: str


@dataclass
class TimeStepsConfig:
    start: str
    end: str


@dataclass
class PipelineConfig:
    time_steps: TimeStepsConfig
    aoi: List[float]
    spectral_bands: List[str]


@dataclass
class StorageConfig:
    type: str
    path: str
    catalog_path: str


@dataclass
class Config:
    earth_search: EarthSearchConfig
    pipeline: PipelineConfig
    storage: StorageConfig
