import os
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlalchemy import Select
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column

load_dotenv()
DB_URL = os.getenv("DB_URL")
if DB_URL is None:
    raise RuntimeError

engine: Engine = create_engine(url=DB_URL)


class Base(DeclarativeBase):
    pass


class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    card_number: Mapped[str]
    password: Mapped[int]
    bank_name: Mapped[str]
    full_name: Mapped[str]
    balance: Mapped[float]

    def save(self):
        with Session(engine) as s:
            s.add(self)
            s.commit()

    @classmethod
    def get_if_exist(
        cls, card_number: str, password: int
    ) -> Optional["BankAccount"]:
        selector = (
            Select(BankAccount)
            .where(BankAccount.card_number == card_number)
            .where(BankAccount.password == password)
        )
        with Session(engine) as s:
            try:
                return s.scalars(selector).one()
            except Exception:
                return None

    @classmethod
    def is_exist(cls, card_number: str, password: int) -> bool:
        return bool(cls.get_if_exist(card_number, password))


Base.metadata.create_all(engine)
