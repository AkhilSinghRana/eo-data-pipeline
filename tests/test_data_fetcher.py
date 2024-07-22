from unittest.mock import MagicMock

import pytest
from omegaconf import DictConfig

from eo_data_pipeline.data_fetcher.fetcher import DataFetcher


@pytest.fixture
def config():
    return DictConfig({"earth_search": {"url": "https://earth-search-url"}})


@pytest.fixture
def fetcher(config):
    return DataFetcher(config)


def test_fetch_data(mocker, fetcher):
    # Mock the pystac_client.Client.open method
    mock_client = mocker.patch("pystac_client.Client.open", autospec=True)

    # Mock the catalog object and its search method
    mock_catalog = MagicMock()
    mock_client.return_value = mock_catalog

    # Mock the search object and its items method
    mock_search = MagicMock()
    mock_catalog.search.return_value = mock_search

    # Create fake STAC items with specific bands
    fake_item_1 = MagicMock()
    fake_item_1.assets = {"B01": MagicMock(), "B02": MagicMock(), "B03": MagicMock()}

    fake_item_2 = MagicMock()
    fake_item_2.assets = {"B01": MagicMock(), "B02": MagicMock()}  # Missing one band

    mock_search.items.return_value = [fake_item_1, fake_item_2]

    time_range = ("2023-01-01", "2023-01-31")
    aoi = [-10.0, 50.0, 10.0, 60.0]
    spectral_bands = ["B01", "B02", "B03"]

    # Call the method
    items = fetcher.fetch_data(time_range, aoi, spectral_bands)

    # Check the filtered items
    assert len(items) == 1
    assert items[0] == fake_item_1


def test_fetch_data_no_results(mocker, fetcher):
    # Mock the pystac_client.Client.open method
    mock_client = mocker.patch("pystac_client.Client.open", autospec=True)

    # Mock the catalog object and its search method
    mock_catalog = MagicMock()
    mock_client.return_value = mock_catalog

    # Mock the search object and its items method
    mock_search = MagicMock()
    mock_catalog.search.return_value = mock_search

    mock_search.items.return_value = []  # No items returned

    time_range = ("2023-01-01", "2023-01-31")
    aoi = [-10.0, 50.0, 10.0, 60.0]
    spectral_bands = ["B01", "B02", "B03"]

    # Call the method
    items = fetcher.fetch_data(time_range, aoi, spectral_bands)

    # Check the results
    assert len(items) == 0


def test_fetch_data_partial_match(mocker, fetcher):
    # Mock the pystac_client.Client.open method
    mock_client = mocker.patch("pystac_client.Client.open", autospec=True)

    # Mock the catalog object and its search method
    mock_catalog = MagicMock()
    mock_client.return_value = mock_catalog

    # Mock the search object and its items method
    mock_search = MagicMock()
    mock_catalog.search.return_value = mock_search

    # Create fake STAC items with specific bands
    fake_item = MagicMock()
    fake_item.assets = {
        "B01": MagicMock(),
        "B02": MagicMock(),
        "B03": MagicMock(),
        "B04": MagicMock(),
    }

    mock_search.items.return_value = [fake_item]

    time_range = ("2023-01-01", "2023-01-31")
    aoi = [-10.0, 50.0, 10.0, 60.0]
    spectral_bands = ["B01", "B02", "B03", "B05"]

    # Call the method
    items = fetcher.fetch_data(time_range, aoi, spectral_bands)

    # Check the results
    assert len(items) == 0
