from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    @property
    def bot_token(self) -> str:
        return os.environ['API-TOKEN']
    @property
    def admin_id(self) -> str:
        return os.environ['ADMIN-ID']


config = Config()

