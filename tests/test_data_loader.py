import pytest
import os
import tempfile
from unittest.mock import patch, Mock
from omegaconf import DictConfig
from eo_data_pipeline.data_loader.loader import DataLoader
from pystac import Item, Asset
from datetime import datetime

@pytest.fixture
def config():
    return DictConfig({
        "storage": {
            "path": tempfile.gettempdir(),
            "catalog_path": tempfile.gettempdir()
        }
    })

@pytest.fixture
def data_loader(config):
    return DataLoader(config)

def test_load_data_single_band(data_loader):
    # Mock items with single band
    mock_asset = Asset(href="http://example.com/B01.tif")
    mock_item = Item(
        id="test_item_1",
        geometry={},
        bbox=[],
        datetime=datetime.now(),
        properties={}
    )
    mock_item.add_asset("B01", mock_asset)

    # Mock download_asset method
    with patch.object(data_loader, 'download_asset') as mock_download:
        mock_download.return_value = None  # No operation for download

        # Call the method
        saved_files = data_loader.load_data([mock_item], ["B01"])

        # Assertions
        assert len(saved_files) == 1
        assert os.path.basename(saved_files[0]) == "test_item_1_B01.tif"
        mock_download.assert_called_once_with("http://example.com/B01.tif", saved_files[0])

def test_load_data_multiple_bands(data_loader):
    # Mock items with multiple bands
    mock_asset_b01 = Asset(href="http://example.com/B01.tif")
    mock_asset_b02 = Asset(href="http://example.com/B02.tif")
    mock_item = Item(
        id="test_item_2",
        geometry={},
        bbox=[],
        datetime=datetime.now(),
        properties={}
    )
    mock_item.add_asset("B01", mock_asset_b01)
    mock_item.add_asset("B02", mock_asset_b02)

    # Mock download_asset method
    with patch.object(data_loader, 'download_asset') as mock_download:
        mock_download.return_value = None  # No operation for download

        # Call the method
        saved_files = data_loader.load_data([mock_item], ["B01", "B02"])

        # Assertions
        assert len(saved_files) == 2
        assert os.path.basename(saved_files[0]) == "test_item_2_B01.tif"
        assert os.path.basename(saved_files[1]) == "test_item_2_B02.tif"
        mock_download.assert_any_call("http://example.com/B01.tif", saved_files[0])
        mock_download.assert_any_call("http://example.com/B02.tif", saved_files[1])

def test_load_data_no_assets(data_loader):
    # Mock item with no assets
    mock_item = Item(
        id="test_item_3",
        geometry={},
        bbox=[],
        datetime=datetime.now(),
        properties={}
    )

    # Call the method
    saved_files = data_loader.load_data([mock_item], ["B01", "B02"])

    # Assertions
    assert len(saved_files) == 0