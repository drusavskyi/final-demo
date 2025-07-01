from __future__ import annotations
from .fields import Name, Phone, Email, Address, Birthday


class Record:
    """Контакт: ім’я + телефони + email-и + адреса + день народження"""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.emails: list[Email] = []
        self.address: Address | None = None
        self.birthday: Birthday | None = None

    # ---------- телефони ----------
    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def change_phone(self, old: str, new: str) -> None:
        for i, ph in enumerate(self.phones):
            if ph.value == old:
                self.phones[i] = Phone(new)
                return
        raise ValueError("Old phone not found")

    # ---------- e-mail ----------
    def add_email(self, email: str) -> None:
        self.emails.append(Email(email))

    def change_email(self, old: str, new: str) -> None:
        for i, em in enumerate(self.emails):
            if em.value == old:
                self.emails[i] = Email(new)
                return
        raise ValueError("Old email not found")

    # ---------- адреса ----------
    def set_address(self, addr: str) -> None:
        self.address = Address(addr)

    # ---------- день народження ----------
    def add_birthday(self, date_str: str) -> None:
        if self.birthday:
            raise ValueError("Birthday already set")
        self.birthday = Birthday(date_str)

    # ---------- представлення ----------
    def __str__(self) -> str:
        phones = ", ".join(p.value for p in self.phones) or "—"
        mails  = ", ".join(e.value for e in self.emails) or "—"
        addr   = self.address.value if self.address else "—"
        bday   = (
            self.birthday.value.strftime("%d.%m.%Y")
            if self.birthday
            else "—"
        )
        return f"{self.name.value}: {phones} | {mails} | {addr} | {bday}"