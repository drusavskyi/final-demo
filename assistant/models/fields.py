from __future__ import annotations
import re
from datetime import datetime

__all__ = ["Field", "Name", "Phone", "Email", "Address", "Birthday"]

class Field:
    """Базове поле, просто зберігає value."""
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


PHONE_RE = re.compile(r"^\d{10}$")
EMAIL_RE = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$")


class Phone(Field):
    def __init__(self, value: str):
        if not PHONE_RE.fullmatch(value):
            raise ValueError("Phone must contain exactly 10 digits")
        super().__init__(value)


class Email(Field):
    def __init__(self, value: str):
        if not EMAIL_RE.fullmatch(value):
            raise ValueError("Invalid email address")
        super().__init__(value)


class Address(Field):
    """Поки без валідації ‒ звичайний рядок."""
    pass


class Birthday(Field):
    """Зберігаємо одразу datetime.date"""
    def __init__(self, value: str):
        try:
            date_obj = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Use format DD.MM.YYYY")
        super().__init__(date_obj)