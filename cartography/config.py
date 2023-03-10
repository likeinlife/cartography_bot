import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:

    @property
    def bot_token(self) -> str:
        return os.environ['API-TOKEN']

    @property
    def admin_id(self) -> int:
        admin_id = os.environ['ADMIN-ID']
        return int(admin_id)

    @property
    def static_path(self) -> Path:
        return Path(__file__).parent / 'static'


config = Config()
