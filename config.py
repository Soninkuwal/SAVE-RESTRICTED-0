import os
from dotenv import load_dotenv
load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL', '')
LOG_CHANNEL_ID = os.getenv('LOG_CHANNEL_ID')
