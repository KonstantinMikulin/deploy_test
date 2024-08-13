from dataclasses import dataclass

from environs import Env


@dataclass
class TgBotConfig:
    token: str
    
    
@dataclass
class Config:
    tg_bot: TgBotConfig
    
    
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    
    return Config(
        tg_bot=TgBotConfig(
            token=env('BOT_TOKEN')
        )
    )
