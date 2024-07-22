# scripts/run_pipeline.py
import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import DictConfig, OmegaConf

from eo_data_pipeline.config.config_schema import (Config, EarthSearchConfig,
                                                   PipelineConfig,
                                                   StorageConfig,
                                                   TimeStepsConfig)
from eo_data_pipeline.pipeline.flow import run_pipeline

cs = ConfigStore.instance()
cs.store(name="hydra_config", node=Config)


@hydra.main(
    config_path="../eo_data_pipeline/config",
    config_name="hydra_config",
    version_base=None,
)
def main(config: DictConfig):
    # Convert DictConfig to Config dataclass
    config_dict = OmegaConf.to_container(config, resolve=True)
    config_instance = Config(
        earth_search=EarthSearchConfig(**config_dict["earth_search"]),
        pipeline=PipelineConfig(
            time_steps=TimeStepsConfig(**config_dict["pipeline"]["time_steps"]),
            aoi=config_dict["pipeline"]["aoi"],
            spectral_bands=config_dict["pipeline"]["spectral_bands"],
        ),
        storage=StorageConfig(**config_dict["storage"]),
    )

    # Run the pipeline
    result = run_pipeline(config_instance)
    print(f"Pipeline execution completed. Result: {result}")


if __name__ == "__main__":
    main()
