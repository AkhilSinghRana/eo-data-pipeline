# eo_data_pipeline/data_loader/loader.py

import logging
import os
import urllib.request

from omegaconf import DictConfig
from pystac import Catalog, Item


class DataLoader:
    """
    A class for loading and saving Earth Observation data and metadata.

    This class handles the storage of fetched data and metadata, including
    saving STAC items to a PySTAC catalog and downloading asset files.

    Attributes:
        storage_path (str): Path to store downloaded asset files.
        catalog_path (str): Path to store the PySTAC catalog.
        logger (logging.Logger): Logger for this class.
    """

    def __init__(self, config: DictConfig):
        """
        Initialize the DataLoader with the given configuration.

        Args:
            config (DictConfig): Configuration containing storage paths.
        """
        self.storage_path = config.storage.path
        self.catalog_path = config.storage.catalog_path
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def save_metadata(self, items: list):
        """
        Save metadata of STAC items to a PySTAC catalog.

        Args:
            items (list): List of STAC items to save as metadata.
        """
        # Ensure Catalog path exists
        if not os.path.exists(self.catalog_path):
            os.makedirs(self.catalog_path)
            self.logger.info(f"Created catalog path: {self.catalog_path}")

        # Create and save PySTAC catalog
        catalog = Catalog(
            id="my-catalog", description="PySTAC catalog for saving Metadata"
        )
        for item in items:
            catalog.add_item(item)
        catalog.normalize_hrefs(self.catalog_path)
        catalog.save(catalog_type="SELF_CONTAINED")

    def load_data(self, items, spectral_bands):
        """
        Load data by downloading assets for specified STAC items and spectral bands.

        Args:
            items (list): List of STAC items to load data from.
            spectral_bands (list): List of spectral bands to load.

        Returns:
            list: List of file paths to the saved items.
        """
        saved_files = []

        # Ensure storage path exists
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
            self.logger.info(f"Created storage path: {self.storage_path}")

        for item in items:
            for band in spectral_bands:
                asset = item.assets.get(band)
                if asset:
                    file_path = os.path.join(self.storage_path, f"{item.id}_{band}.tif")
                    self.logger.info(
                        f"Downloading asset from {asset.href} to {file_path}"
                    )
                    self.download_asset(asset.href, file_path)
                    saved_files.append(file_path)
                    self.logger.info(f"Saved file: {file_path}")

        self.logger.info(f"Total files saved: {len(saved_files)}")
        return saved_files

    def download_asset(self, url, file_path):
        """
        Download an asset from a given URL to a specified file path.

        Args:
            url (str): URL of the asset to download.
            file_path (str): Local path to save the downloaded asset.
        """
        try:
            urllib.request.urlretrieve(url, file_path)
        except Exception as e:
            self.logger.error(
                f"Failed to download asset from {url} to {file_path}: {e}"
            )
