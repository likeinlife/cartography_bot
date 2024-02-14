import json
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.utils.classes import Color


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    BOT_TOKEN: str
    ADMIN_ID: int
    PUBLIC: bool = Field(False)

    STATIC_PATH: Path = Path(__file__).parent.parent / Path("static")
    BAN_LIST_PATH: Path = STATIC_PATH / Path("banned_users.json")

    LOGS_MAX_SIZE: int = Field(256)
    DISABLE_STREAM_HANDLER: bool = Field(False)
    LOGGING_LEVEL: str = Field("WARNING")
    DEV_MODE: bool = Field(True)
    BAN_LIST: list[int] = []

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.update_banned_users()

    def update_banned_users(self):
        print("update")
        with open(self.BAN_LIST_PATH, "r") as file_obj:
            ban_list = json.load(file_obj)
        self.BAN_LIST = ban_list


config = Config()


class ImageConfig:
    HEIGHT = 800  # pixels
    WIDTH = 800  # pixels
    RESOLUTION = (WIDTH, HEIGHT)
    PADDING = 15  # pixels
    COLUMN_LABEL_ANGLE = 310  # degrees - column labels rotate angle
    BACKGROUND_COLOR = Color.WHITE
    FILLED_CELL_COLOR = Color.GRAY
    TEXT_COLOR = Color.BLACK
    PATH_TO_FONT: str = str(config.STATIC_PATH / Path("font.otf"))
