import os

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()
DB_URL = os.getenv("DB_URL")
if DB_URL is None:
    raise RuntimeError

engine: Engine = create_engine(url=DB_URL)


class Base(DeclarativeBase):
    pass
