from typing import Protocol, TypeVar, TypeAlias

from ldap3 import Server, Connection
from sqlalchemy import select, insert, delete
import aiohttp
from aiohttp.web_exceptions import HTTPError

from ..database.ldap.config import config as ldap_config
from ..database.sqlalchemy.setup import async_session_maker
from ..database.sqlalchemy.models import AuthenticatedUser
from .external_api.config import weather_api_config


Entity = TypeVar('Entity')
Model = TypeVar('Model')

EntityId: TypeAlias = int


class AbstractWeatherRepository(Protocol):

    async def get_current(self, city: str) -> dict:
        ...

    async def get_forecast_upon(self, days: int, city: str) -> list[dict]:
        ...


class WeatherRepository:

    async def get_current(self, city: str):
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.get(
                    f'{weather_api_config.url}current.json?q={city}&key={weather_api_config.weather_api_token}'
                    )
                result = await response.json()
                return result['current']
            
            except HTTPError:
                pass

    async def get_forecast_upon(self, days: int, city: str):
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.get(
                    f'{weather_api_config.url}forecast.json?q={city}&days={days}&key={weather_api_config.weather_api_token}'
                    )
                result: list = await response.json()
                return result['forecast']['forecastday']
            
            except HTTPError:
                pass


class AbstractLDAPRepository(Protocol):

    def check_ad_credentials(self, username: str, password: str) -> bool:
        ...


class LDAPRepository:

    def check_ad_credentials(self, username: str, password: str):

        if not password:
            return False

        server = Server(ldap_config.server, get_info='ALL')
        # The user format for NTLM is DOMAIN\username
        user_dn = f"{ldap_config.domain}\\{username}"

        try:
            # Establish a connection with the user's credentials
            # This will succeed only if the username/password is correct.
            conn = Connection(server, user=user_dn, password=password, authentication='SIMPLE', auto_bind=True)
            # Don't forget to close the connection
            conn.unbind()
            return True
        except Exception as e:
            print(e)
            return False
        

class SQLAlchemyRepository[Model](Protocol):
    model: Model = ...


class AbstractAuthenticatedUserRepository[Entity](Protocol):
    
    async def add(self, schema: dict) -> EntityId:
        ...

    async def get(self, name: str) -> Entity | None:
        ...

    async def delete_by_nickname(self, name: str) -> None:
        ...

    async def get_by_domain_name(self, name: str) -> Entity:
        ...


class AuthenticatedUserRepository:

    model = AuthenticatedUser

    async def add(self, schema: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**schema).returning(self.model.id)

            result = await session.execute(stmt)
            await session.commit()

            return result.scalar_one()
        
        
    async def get(self, name: str):
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.nickname == name)

            result = await session.execute(query)

            return result.scalar_one_or_none()
        

    async def delete_by_nickname(self, name: str):
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.nickname == name)
            
            await session.execute(stmt)
            await session.commit()


    async def get_by_domain_name(self, name: str):
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.domain_name == name)

            result = await session.execute(query)

            return result.scalar_one_or_none()