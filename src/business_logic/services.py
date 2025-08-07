import asyncio

from ..data_access.repositories import (
    AbstractLDAPRepository, 
    AbstractAuthenticatedUserRepository,
    AbstractWeatherRepository
)
from ..data_access.shemas import (
    AuthenticatedUser, 
    AuthenticatedUserFromDB, 
    CurrentWeather,
    DailyForecast
)


class LDAPService:

    def __init__(self, repo: type[AbstractLDAPRepository]):
        self._repo = repo()
        
    async def check_ad_credentials(self, username: str, password: str):
        is_authed = await asyncio.to_thread(self._repo.check_ad_credentials, username, password)
        return is_authed
    

class AuthenticatedUserService:
    
    def __init__(self, repo: type[AbstractAuthenticatedUserRepository[AuthenticatedUserFromDB]]):
        self._repo = repo()

    async def add(self, schema: AuthenticatedUser):
        return await self._repo.add(schema.model_dump())
    
    async def get(self, name: str):
        user = await self._repo.get(name)
        if user:
            return AuthenticatedUserFromDB.model_validate(user)
        return None
    
    async def delete_by_nickname(self, name: str):
        await self._repo.delete_by_nickname(name)

    async def get_by_domain_name(self, name: str):
        user = await self._repo.get_by_domain_name(name)
        if user:
            return AuthenticatedUserFromDB.model_validate(user)
        return None
    

class WeatherService:

    def __init__(self, repo: type[AbstractWeatherRepository]):
        self._repo = repo()

    async def get_current(self, city: str = "Карабаш"):
        current_weather = await self._repo.get_current(city)
        return CurrentWeather.model_validate(current_weather)
    

    # --- THIS IS THE FIXED METHOD ---
    async def get_forecast_upon(self, days: int = 1, city: str = "Карабаш") -> list[DailyForecast]:
        """
        Fetches forecast data from the repository and validates it into a list of DailyForecast objects.
        """
        # The repo now safely returns a list (or an empty one on error)
        forecast_data = await self._repo.get_forecast_upon(days, city)

        # A clean list comprehension is all we need now!
        # Pydantic will handle all the nested validation.
        validated_forecasts = [DailyForecast.model_validate(day_data) for day_data in forecast_data]

        return validated_forecasts