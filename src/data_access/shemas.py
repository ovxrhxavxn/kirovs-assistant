from datetime import datetime

from pydantic import BaseModel, Field


class AuthenticatedUser(BaseModel):
    nickname: str
    domain_name: str


class AuthenticatedUserFromDB(AuthenticatedUser):
    id: int

    class Config:
        from_attributes = True


class CurrentWeather(BaseModel):
    temp_c: float
    is_day: bool
    wind_kph: float
    cloud: float
    feelslike_c: float


class WeatherDay(BaseModel):
    maxtemp_c: float
    mintemp_c: float
    avgtemp_c: float
    maxwind_kph: float
    daily_will_it_rain: bool
    daily_chance_of_rain: int
    daily_will_it_snow: bool
    daily_chance_of_snow: int


class WeatherDayHour(BaseModel):
    time: datetime
    temp_c: float
    wind_kph: float
    cloud: int
    feelslike_c: float
    will_it_rain: bool
    chance_of_rain: int
    will_it_snow: bool
    chance_of_snow: int


# --- THIS IS THE NEW SCHEMA ---
class DailyForecast(BaseModel):
    """Represents the complete forecast for a single day."""
    day_summary: WeatherDay = Field(..., alias="day")
    hourly_forecast: list[WeatherDayHour] = Field(..., alias="hour")