from tgbot.config import load_config
from infrastructure.database.postgresql import Database


db = Database()
config = load_config(".env")
