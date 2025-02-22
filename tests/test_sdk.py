import pytest
import requests
from unittest.mock import patch
from weather_sdk.sdk import WeatherSDK
from weather_sdk.exceptions import WeatherSDKException, NetworkErrorException, WeatherAPIException

@pytest.fixture(autouse=True)
def reset_sdk_instances():
    WeatherSDK._instances.clear()

def test_get_weather():
    sdk = WeatherSDK(api_key="36f3011ccd5f433c43123f97049603cc", mode='on-demand')
    weather = sdk.get_weather("Москва")
    assert weather['name'] == 'Moscow'

def test_get_weather_invalid_city():
    sdk = WeatherSDK(api_key="36f3011ccd5f433c43123f97049603cc", mode='on-demand')
    with pytest.raises(WeatherSDKException):
        sdk.get_weather("InvalidCity")

def test_get_weather_invalid_api_key():
    sdk = WeatherSDK(api_key="invalid_api_key", mode='on-demand')

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 401
        mock_get.return_value.json.return_value = {"message": "Invalid API key"}

        with pytest.raises(WeatherAPIException) as excinfo:
            sdk.get_weather("Москва")
        
        assert "Ошибка API OpenWeather" in str(excinfo.value)

def test_get_weather_network_error():
    sdk = WeatherSDK(api_key="36f3011ccd5f433c43123f97049603cc", mode='on-demand')

    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        with pytest.raises(NetworkErrorException) as excinfo:
            sdk.get_weather("Москва")
        
        assert "Ошибка сети" in str(excinfo.value)

def test_singleton_instance_creation():
    sdk1 = WeatherSDK(api_key="36f3011ccd5f433c43123f97049603cc", mode='on-demand')
    with pytest.raises(WeatherSDKException):
        sdk2 = WeatherSDK(api_key="36f3011ccd5f433c43123f97049603cc", mode='on-demand')

def test_delete_weather_data():
    sdk = WeatherSDK(api_key="36f3011ccd5f433c43123f97049603cc", mode='on-demand')
    sdk.get_weather("Москва")
    sdk.delete_weather_data("Москва")
    with pytest.raises(WeatherSDKException):
        sdk.delete_weather_data("Москва")

def test_delete_instance():
    sdk = WeatherSDK(api_key="36f3011ccd5f433c43123f97049603cc", mode='on-demand')
    WeatherSDK.delete_instance("36f3011ccd5f433c43123f97049603cc")
    with pytest.raises(WeatherSDKException):
        WeatherSDK.delete_instance("36f3011ccd5f433c43123f97049603cc")
