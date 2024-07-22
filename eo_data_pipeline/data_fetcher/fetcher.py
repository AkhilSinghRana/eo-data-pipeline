# eo_data_pipeline/data_fetcher/fetcher.py

import pystac_client
from omegaconf import DictConfig

from .validator import ParameterValidator


class DataFetcher:
    """
    A class for fetching Sentinel-2 data from the Earth Search catalog.

    This class handles the creation of a STAC client, searching for relevant data,
    and filtering the results based on specified criteria.

    Attributes:
        catalog_url (str): The URL of the Earth Search catalog.
    """

    def __init__(self, config: DictConfig):
        """
        Initialize the DataFetcher with the given configuration.

        Args:
            config (DictConfig): Configuration containing the Earth Search catalog URL.
        """
        self.catalog_url = config.earth_search.url

    def fetch_data(self, time_range, aoi, spectral_bands):
        """
        Fetch Sentinel-2 data from Earth Search catalog based on specified criteria.

        Args:
            time_range (tuple): Start and end dates for the search in format (start_date, end_date).
            aoi (list): Bounding box coordinates [lon_min, lat_min, lon_max, lat_max].
            spectral_bands (list): List of spectral bands to fetch.

        Returns:
            list: List of STAC items matching the search criteria and containing all specified spectral bands.

        Note:
            The method filters for items with cloud cover less than 20%. This threshold
            could be moved to the configuration for more flexibility.
        """
        # Create a STAC client
        catalog = pystac_client.Client.open(self.catalog_url)

        # Create a search with specified parameters
        search = catalog.search(
            collections=["sentinel-2-l2a"],
            datetime=f"{time_range[0]}/{time_range[1]}",
            bbox=aoi,
            query={"eo:cloud_cover": {"lt": 20}},  # Filter for low cloud cover
        )

        # Execute the search and get all items
        items = list(search.items())

        # Filter items to ensure all required bands are present
        filtered_items = [
            item
            for item in items
            if all(band in item.assets for band in spectral_bands)
        ]

        print(f"Total items based on filter criteria in config: {len(filtered_items)}")

        return filtered_items
