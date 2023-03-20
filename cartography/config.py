import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    """ENV variables:
        API-TOKEN - bot token
        ADMIN-ID - admin telegram id
        DEBUG - enable debug mode
        PUBLIC - enable public use
    """

    @property
    def path_to_font(self) -> str:
        return str(Path(os.getcwd()) / Path('static', 'font.otf'))

    @property
    def bot_token(self) -> str:
        return os.environ['API-TOKEN']

    @property
    def admin_id(self) -> int:
        admin_id = os.environ['ADMIN-ID']
        return int(admin_id)

    @property
    def debug(self) -> bool:
        debug = os.getenv('DEBUG')
        if debug:
            print('DEBUG MODE')
            return True
        return False

    @property
    def static_path(self) -> Path:
        return Path(__file__).parent / 'static'

    @property
    def public(self) -> bool:
        public = os.getenv('PUBLIC')
        if public:
            return True
        return False


config = Config()
