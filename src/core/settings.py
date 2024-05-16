import logging
from pathlib import Path

from cartography.types import ImageColorType
from misc.constants import Color
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    bot_token: str = Field()
    admin_id: int = Field()
    dev_mode: bool = Field(True, description="True - admin only use ")

    static_path: Path = Field(Path(__file__).parent.parent.parent / Path("static"))

    logging_level: str = Field("DEBUG")

    @computed_field
    def numeric_logging_level(self) -> int:
        return getattr(logging, self.logging_level)


app_settings = Config()  # type: ignore


class ImageConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="IMAGE_")

    height: int = Field(1200, description="Height of image in pixels")
    width: int = Field(1200, description="Width of image in pixels")

    padding: int = Field(150, description="Length to image borders in pixels")
    text_size_coefficient: int = Field(10, description="Text size coefficient")
    text_angle: int = Field(310, description="Angle of column labels in degrees")
    bottom_label_offset: int = Field(0, description="Vertical length to table bottom")
    right_label_offset: int = Field(3, description="Horizontal length to table right")

    background_color: ImageColorType = Field(Color.WHITE)
    filling_color: ImageColorType = Field(Color.GRAY)
    text_color: ImageColorType = Field(Color.BLACK)
    inverse_text_color: ImageColorType = Field(Color.WHITE)

    font_path: Path = Field(app_settings.static_path / Path("font.otf"))

    @computed_field
    def resolution(self) -> tuple[int, int]:
        return self.width, self.height


image_settings = ImageConfig()  # type: ignore
