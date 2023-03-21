import os
from pathlib import Path

from dotenv import load_dotenv

from cartography.utils.classes import Color

load_dotenv()


def check_option(option_name: str) -> bool:
    # Check if option defined in enviroment
    option = os.getenv(option_name)
    if option:
        return True
    return False


class Config:

    STATIC_PATH: Path = Path(os.getcwd()) / Path('static')
    DISABLE_STREAM_HANDLER = check_option('DISABLE-STREAM-HANDLER')  # disable logging output in console
    PUBLIC = check_option('PUBLIC')  # open bot for public use(not admin only)
    LOGS_MAX_SIZE = 256  # in kilobytes

    @property
    def DEV_MODE(self) -> bool:
        if mode := check_option('DEV-MODE'):
            print('DEV MODE ON')
        return mode

    @property
    def BOT_TOKEN(self) -> str:
        return os.environ['BOT-TOKEN']

    @property
    def ADMIN_ID(self) -> int:
        admin_id = os.environ['ADMIN-ID']
        return int(admin_id)

    @property
    def LOGGING_LEVEL(self) -> str:
        logging_level = os.getenv('LOGGING-LEVEL')
        if not logging_level:
            return 'WARNING'
        return logging_level


class ImageConfig:
    HEIGHT = 800  # pixels
    WIDTH = 800  # pixels
    RESOLUTION = (WIDTH, HEIGHT)
    PADDING = 15  # pixels
    COLUMN_LABEL_ANGLE = 310  # degrees - column labels rotate angle
    BACKGROUND_COLOR = Color.WHITE
    TEXT_COLOR = Color.BLACK
    PATH_TO_FONT: str = str(Config.STATIC_PATH / Path('font.otf'))


config = Config()
