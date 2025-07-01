from __future__ import annotations
from collections import UserDict
from datetime import date, timedelta
from pathlib import Path
import pickle

from .record import Record

DATA_PATH = Path(__file__).resolve().parent / "assistant_book.pkl"


class AddressBook(UserDict):
    """Контейнер для Record з базовими операціями та збереженням"""

    # ---------- CRUD ----------
    def add_record(self, rec: Record) -> None:
        self.data[rec.name.value] = rec

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete_record(self, name: str) -> bool:
        if name in self.data:
            del self.data[name]
            return True
        return False

    # ---------- birthdays ----------
    def get_upcoming_birthdays(self, days: int = 7) -> list[tuple[str, str]]:
        today = date.today()
        last_day = today + timedelta(days=days)
        upcoming: list[tuple[str, str]] = []

        for rec in self.data.values():
            if rec.birthday:
                bday = rec.birthday.value.replace(year=today.year)
                if bday < today:  # уже минув
                    bday = bday.replace(year=today.year + 1)
                if today <= bday <= last_day:
                    upcoming.append((rec.name.value, bday.strftime("%d.%m.%Y")))
        return upcoming

    # ---------- persistence ----------
    def save(self, path: Path = DATA_PATH) -> None:
        with open(path, "wb") as fh:
            pickle.dump(self.data, fh)

    @classmethod
    def load(cls, path: Path = DATA_PATH) -> "AddressBook":
        book = cls()
        if path.exists():
            with open(path, "rb") as fh:
                book.data = pickle.load(fh)
        return book