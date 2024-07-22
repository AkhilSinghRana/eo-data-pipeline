# eo_data_pipeline/data_fetcher/validator.py

from datetime import datetime


class ParameterValidator:
    """
    A utility class for validating input parameters for the Earth Observation data pipeline.

    This class provides static methods to validate time ranges, areas of interest (AOI),
    and spectral bands according to the Earth Search Catalog recommendations.
    """

    @staticmethod
    def validate_time_range(time_range):
        """
        Validate the given time range.

        Args:
            time_range (list): A list containing start and end dates in 'YYYY-MM-DD' format.

        Raises:
            ValueError: If the date format is invalid or if the start date is after the end date.
        """
        try:
            start = datetime.strptime(time_range[0], "%Y-%m-%d")
            end = datetime.strptime(time_range[1], "%Y-%m-%d")
            assert start < end, "Start date must be before end date"
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        except AssertionError as e:
            raise ValueError(str(e))

    @staticmethod
    def validate_aoi(aoi):
        """
        Validate the given Area of Interest (AOI).

        Args:
            aoi (list): A list of 4 coordinates [lon_min, lat_min, lon_max, lat_max].

        Raises:
            ValueError: If the AOI format is invalid or if the coordinates are out of bounds.
        """
        if len(aoi) != 4:
            raise ValueError(
                f"AOI must be a list of 4 coordinates: [lon_min, lat_min, lon_max, lat_max], received: {aoi}"
            )
        lon_min, lat_min, lon_max, lat_max = aoi
        if not (-180 <= lon_min < lon_max <= 180) or not (
            -90 <= lat_min < lat_max <= 90
        ):
            raise ValueError("Invalid AOI coordinates")

    @staticmethod
    def validate_spectral_bands(spectral_bands):
        """
        Validate the given spectral bands.

        Args:
            spectral_bands (list): A list of spectral band names.

        Raises:
            ValueError: If any of the specified bands are not valid Sentinel-2 bands.
        """
        valid_bands = {
            "aot",
            "blue",
            "coastal",
            "granule_metadata",
            "green",
            "nir",
            "nir08",
            "nir09",
            "red",
            "rededge1",
            "rededge2",
            "rededge3",
            "scl",
            "swir16",
            "swir22",
            "thumbnail",
            "tileinfo_metadata",
            "visual",
            "wvp",
            "aot-jp2",
            "blue-jp2",
            "coastal-jp2",
            "green-jp2",
            "nir-jp2",
            "nir08-jp2",
            "nir09-jp2",
            "red-jp2",
            "rededge1-jp2",
            "rededge2-jp2",
            "rededge3-jp2",
            "scl-jp2",
            "swir16-jp2",
            "swir22-jp2",
            "visual-jp2",
            "wvp-jp2",
        }
        if not set(spectral_bands).issubset(valid_bands):
            raise ValueError(f"Invalid spectral bands. Choose from: {valid_bands}")
