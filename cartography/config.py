from dotenv import load_dotenv
import os

load_dotenv()


class Config:

    @property
    def bot_token(self) -> str:
        return os.environ['API-TOKEN']

    @property
    def admin_id(self) -> int:
        admin_id = os.environ['ADMIN-ID']
        return int(admin_id)


config = Config()
