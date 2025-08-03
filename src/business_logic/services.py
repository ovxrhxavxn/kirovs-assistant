import asyncio

from ..data_access.repositories import (
    AbstractLDAPRepository, 
    AbstractAuthenticatedUserRepository,
    AbstractWeatherRepository
)
from ..data_access.shemas import AuthenticatedUser, AuthenticatedUserFromDB, Weather


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
        data = await self._repo.get_current(city)
        return Weather.model_validate(data)