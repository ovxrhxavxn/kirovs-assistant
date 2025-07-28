from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Игнорировать лишние переменные в .env
    )

class BotConfig(BaseConfig):
    token: str


bot_config = BotConfig()