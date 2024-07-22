from datetime import datetime

import pytest

from eo_data_pipeline.data_fetcher.validator import ParameterValidator


def test_validate_time_range_valid():
    # Valid time range
    ParameterValidator.validate_time_range(("2023-01-01", "2023-01-31"))


def test_validate_time_range_invalid_format():
    # Invalid date format
    with pytest.raises(ValueError, match="Invalid date format. Use YYYY-MM-DD"):
        ParameterValidator.validate_time_range(("2023-01-01", "2023/01/31"))


def test_validate_time_range_invalid_range():
    # Start date after end date
    with pytest.raises(ValueError, match="Start date must be before end date"):
        ParameterValidator.validate_time_range(("2023-01-31", "2023-01-01"))


def test_validate_aoi_valid():
    # Valid AOI
    ParameterValidator.validate_aoi([-10.0, 50.0, 10.0, 60.0])


def test_validate_aoi_invalid_length():
    # Invalid AOI length
    with pytest.raises(ValueError, match="AOI must be a list of 4 coordinates"):
        ParameterValidator.validate_aoi([-10.0, 50.0, 10.0])


def test_validate_aoi_invalid_coordinates():
    # Invalid AOI coordinates
    with pytest.raises(ValueError, match="Invalid AOI coordinates"):
        ParameterValidator.validate_aoi([-190.0, 50.0, 10.0, 60.0])


def test_validate_spectral_bands_valid():
    # Valid spectral bands
    ParameterValidator.validate_spectral_bands(["blue", "green", "red"])


def test_validate_spectral_bands_invalid():
    # Invalid spectral bands
    with pytest.raises(ValueError, match="Invalid spectral bands"):
        ParameterValidator.validate_spectral_bands(["invalid_band"])


if __name__ == "__main__":
    pytest.main()
