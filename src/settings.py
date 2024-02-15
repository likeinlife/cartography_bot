from pathlib import Path

from domain.types import ImageColorType
from enums import Color
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    bot_token: str = Field()
    admin_id: int = Field()
    dev_mode: bool = Field(True, description="True - admin only use ")

    static_path: Path = Field(Path(__file__).parent.parent / Path("static"))

    logging_level: str = Field("WARNING")

    ban_list_path: Path = Field(static_path / Path("banned_users.json"))


app_settings = Config()  # type: ignore


class ImageConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="IMAGE_")

    height: int = Field(800, description="Height of image in pixels")
    width: int = Field(800, description="Width of image in pixels")
    resolution: tuple = (width, height)

    padding: int = Field(15, description="Length to image borders in pixels")
    text_angle: int = Field(310, description="Angle of column labels in degrees")
    bottom_label_offset: int = Field(0, description="Vertical length to table bottom")
    right_label_offset: int = Field(3, description="Horizontal length to table right")

    background_color: ImageColorType = Field(Color.WHITE)
    filled_cell_color: ImageColorType = Field(Color.GRAY)
    text_color: ImageColorType = Field(Color.BLACK)
    inverse_text_color: ImageColorType = Field(Color.WHITE)

    font_path: Path = Field(app_settings.static_path / Path("font.otf"))


image_settings = ImageConfig()  # type: ignore
