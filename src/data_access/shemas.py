from pydantic import BaseModel


class AuthenticatedUser(BaseModel):
    nickname: str
    domain_name: str


class AuthenticatedUserFromDB(AuthenticatedUser):
    id: int

    class Config:
        from_attributes = True


class Weather(BaseModel):
    temp_c: float
    is_day: bool
    wind_kph: float
    cloud: float
    feelslike_c: float