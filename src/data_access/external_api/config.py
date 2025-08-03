from ...config import BaseConfig


class WeatherAPIConfig(BaseConfig):
    weather_api_token: str
    url: str


weather_api_config = WeatherAPIConfig()