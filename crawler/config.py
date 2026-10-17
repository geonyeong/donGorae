"""크롤러 설정 — 환경변수 기반."""

import os

from dotenv import load_dotenv

load_dotenv()

DATABASE = {
    "host": os.getenv("DATABASE_HOST", "127.0.0.1"),
    "port": int(os.getenv("DATABASE_PORT", "3306")),
    "user": os.getenv("DATABASE_USER", "dongorae"),
    "password": os.getenv("DATABASE_PASSWORD", "dongorae"),
    "database": os.getenv("DATABASE_NAME", "dongorae"),
    "charset": "utf8mb4",
}

CRAWL_DELAY_SEC = float(os.getenv("CRAWL_DELAY_SEC", "3"))
USER_AGENT = os.getenv(
    "USER_AGENT",
    "DonGoraeBot/0.1 (+https://dongorae.kr; weekly crawl)",
)
