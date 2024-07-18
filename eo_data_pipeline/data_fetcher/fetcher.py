import pystac_client
from omegaconf import DictConfig
from .validator import ParameterValidator


class DataFetcher:
    def __init__(self, config: DictConfig):
        self.catalog_url = config.earth_search.url

    def fetch_data(self, time_range, aoi, spectral_bands):
        """
        Fetch Sentinel-2 data from Earth Search catalog.

        Args:
            time_range (tuple): Start and end dates for the search.
            aoi (list): Bounding box coordinates [lon_min, lat_min, lon_max, lat_max].
            spectral_bands (list): List of spectral bands to fetch.

        Returns:
            list: List of STAC items matching the search criteria.
        """
        # Validate parameters
        ParameterValidator.validate_time_range(time_range)
        ParameterValidator.validate_aoi(aoi)
        ParameterValidator.validate_spectral_bands(spectral_bands)

        # Create a STAC client
        catalog = pystac_client.Client.open(self.catalog_url)

        # Create a search
        search = catalog.search(
            collections=["sentinel-2-l2a"],
            datetime=f"{time_range[0]}/{time_range[1]}",
            bbox=aoi,
            query={"eo:cloud_cover": {"lt": 20}},  # Example: filter for low cloud cover
        )

        # Execute the search and return the items
        items = list(search.items())
        print(f"Total items found: {len(items)}")
        for item in items:
            print(f"Item ID: {item.id}")
            print(f"Item Assets: {list(item.assets.keys())}")

        # Filter items based on required bands
        filtered_items = [
            item
            for item in items
            if all(band in item.assets for band in spectral_bands)
        ]

        print(f"Filtered items count: {len(filtered_items)}")
        for item in filtered_items:
            print(f"Filtered Item ID: {item.id}")
            print(f"Filtered Item Assets: {list(item.assets.keys())}")

        return filtered_items