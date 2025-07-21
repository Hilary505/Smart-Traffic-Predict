import pytest
from unittest.mock import patch
from run import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('json_parser.traffic_parser.get_traffic')
def test_home_route(mock_get_traffic, client):
    mock_get_traffic.return_value = [
        {"region": "SYD_MET", "title": "Test Cam", "view": "Front", "direction": "North", "href": "http://test.com/image.jpg", "predict": "high congestion (score = 0.95)"}
    ]
    response = client.get('/?region=SYD_MET')
    assert response.status_code == 200
    assert b'Test Cam' in response.data
    assert b'high congestion' in response.data 