# eo_data_pipeline/data_loader/loader.py
from omegaconf import DictConfig
import os
import logging
import urllib.request

class DataLoader:
    def __init__(self, config: DictConfig):
        self.storage_path = config.storage.path
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)


    def load_data(self, items, spectral_bands):
        """
        Load data into the specified storage system.

        Args:
            items (list): List of STAC items to load.
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
        Download the asset from the given URL to the specified file path.

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
