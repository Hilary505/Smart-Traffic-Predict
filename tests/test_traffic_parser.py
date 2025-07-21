import pytest
from unittest.mock import patch, MagicMock
from json_parser import traffic_parser

@patch('json_parser.traffic_parser.urlopen')
@patch('json_parser.traffic_parser.predict.tensorflow_pred')
def test_get_traffic_success(mock_predict, mock_urlopen):
    # Mock API response
    mock_urlopen.return_value.read.return_value = b'{"features": [{"properties": {"region": "SYD_MET", "title": "Test Cam", "view": "Front", "direction": "North", "href": "http://test.com/image.jpg"}}]}'
    mock_predict.return_value = 'high congestion (score = 0.95)'
    result = traffic_parser.get_traffic('SYD_MET')
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['region'] == 'SYD_MET'
    assert 'predict' in result[0]
    assert result[0]['predict'] == 'high congestion (score = 0.95)'

@patch('json_parser.traffic_parser.urlopen')
def test_get_traffic_api_error(mock_urlopen):
    mock_urlopen.side_effect = Exception('API error')
    result = traffic_parser.get_traffic('SYD_MET')
    assert result == [] 