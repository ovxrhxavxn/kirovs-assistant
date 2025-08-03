from ...config import BaseConfig


class BotConfig(BaseConfig):
    bot_token: str


bot_config = BotConfig()