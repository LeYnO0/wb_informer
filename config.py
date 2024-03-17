import os

from dotenv import load_dotenv


load_dotenv()
# Подгружаем переменные из файла .env
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

TG_TOKEN = os.environ.get("TG_TOKEN")
GETITEM_URL = os.environ.get("GETITEM_URL")
