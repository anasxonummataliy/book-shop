import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

BOT_NAME = "📚 Kitob Do'koni"
BOT_DESCRIPTION = "Eng yaxshi kitoblarni topish va sotib olish uchun bot"
BOT_SHORT_DESCRIPTION = "Kitoblar sotib oling"
