import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB = os.path.join(BASE_DIR / "messages.db")
ENV = os.path.join(BASE_DIR / ".env")