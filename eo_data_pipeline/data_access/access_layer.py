import rasterio


class DataAccessLayer:
    def __init__(self, path: str):
        self.storage_path = path

    def load_data(self):
        """
        Load data for the specified item and band.

        Returns:
            numpy.ndarray: Array containing the data for the specified item and band.
        """
        with rasterio.open(self.storage_path) as src:
            data = src.read()
            self.transform = src.transform  # Optional just for debugging or plotting
            self.crs = src.crs  # Optional just for debugging or plotting
        return data
