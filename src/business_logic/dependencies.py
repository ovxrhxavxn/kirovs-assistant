from ..data_access.repositories import LDAPRepository, AuthenticatedUserRepository, WeatherRepository
from .services import LDAPService, AuthenticatedUserService, WeatherService


def get_ldap_service():
    return LDAPService(LDAPRepository)


def get_auth_user_service():
    return AuthenticatedUserService(AuthenticatedUserRepository)


def get_weather_service():
    return WeatherService(WeatherRepository)