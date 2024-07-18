import pytest
from eo_data_pipeline.data_fetcher.fetcher import fetch_data


def test_fetch_data():
    start_date = "2021-01-01"
    end_date = "2021-01-31"
    aoi = {
        "type": "Polygon",
        "coordinates": [
            [
                [-122.5, 37.7],
                [-122.4, 37.7],
                [-122.4, 37.8],
                [-122.5, 37.8],
                [-122.5, 37.7],
            ]
        ],
    }
    results = fetch_data(start_date, end_date, aoi)
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(url.startswith("https://") for url in results)
