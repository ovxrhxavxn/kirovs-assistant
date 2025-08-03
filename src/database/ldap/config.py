from ...config import BaseConfig


class LDAPConfig(BaseConfig):
    server: str
    domain: str


config = LDAPConfig()