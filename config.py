import os
from dotenv import load_dotenv

# .env 파일 불러오기
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = os.getenv("DB_PATH", "data/db/memory.db")  # 기본값 지정

AUDIO_PATH = os.getenv("AUDIO_PATH", "data/audio")
DEFAULT_VOLUME = 15

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN이 설정되지 않았습니다. .env 파일 또는 환경변수를 확인하세요.")
