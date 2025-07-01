from __future__ import annotations

from ..models import AddressBook, Record
from ..errors import input_error

# ───────────────────── КОМАНДИ ДЛЯ КОНТАКТІВ ─────────────────────

@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """add <ім'я> <телефон>"""
    if len(args) < 2:
        raise IndexError("Використання: add <ім'я> <телефон>")
    name, phone = args[0], args[1]

    rec = book.find(name) or Record(name)
    rec.add_phone(phone)
    book.add_record(rec)
    return f"Контакт '{name}' збережено."


@input_error
def show_phones(args: list[str], book: AddressBook) -> str:
    """phone <ім'я>"""
    if not args:
        raise IndexError("Використання: phone <ім'я>")
    name = args[0]
    rec = book.find(name)
    if not rec:
        raise KeyError("Контакт не знайдено")
    return ", ".join(p.value for p in rec.phones) or "Немає телефонів"


@input_error
def change_phone(args, book):
    """change <ім'я> <старий_телефон> <новий_телефон>"""
    name, old, new, *_ = args
    rec = book.find(name)
    if not rec:
        raise KeyError("Контакт не знайдено")
    rec.change_phone(old, new)
    return "Телефон оновлено."


@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
    """delete <ім'я>"""
    if not args:
        raise IndexError("Використання: delete <ім'я>")
    name = args[0]
    if book.delete_record(name):
        return f"Контакт '{name}' видалено."
    return "Контакт не знайдено."


def list_all(_: list[str], book: AddressBook) -> str:
    """all"""
    if not book.data:
        return "Адресна книга порожня."
    return "\n".join(str(r) for r in book.data.values())


# ───────────────────── ЕЛЕКТРОННА ПОШТА ──────────────────────

@input_error
def add_email(args, book):
    """add-email <ім'я> <email>"""
    name, email, *_ = args
    rec = book.find(name)
    if not rec:
        raise KeyError("Контакт не знайдено")
    rec.add_email(email)
    return "Email додано."


@input_error
def change_email(args, book):
    """change-email <ім'я> <старий_email> <новий_email>"""
    name, old, new, *_ = args
    rec = book.find(name)
    if not rec:
        raise KeyError("Контакт не знайдено")
    rec.change_email(old, new)
    return "Email оновлено."


@input_error
def list_emails(args, book):
    """emails <ім'я>"""
    name, *_ = args
    rec = book.find(name)
    if not rec:
        raise KeyError("Контакт не знайдено")
    return ", ".join(e.value for e in rec.emails) or "Немає email-адрес"


# ────────────────────────── АДРЕСА ──────────────────────────

@input_error
def set_address(args, book):
    """set-address <ім'я> <адреса ...>"""
    name, *addr = args
    if not addr:
        raise IndexError("Використання: set-address <ім'я> <адреса>")
    rec = book.find(name)
    if not rec:
        raise KeyError("Контакт не знайдено")
    rec.set_address(" ".join(addr))
    return "Адресу збережено."


@input_error
def show_address(args, book):
    """address <ім'я>"""
    name, *_ = args
    rec = book.find(name)
    if not rec:
        raise KeyError("Контакт не знайдено")
    return rec.address.value if rec.address else "Адресу не задано"


# ────────────────────── ДНІ НАРОДЖЕННЯ ──────────────────────

@input_error
def add_birthday(args, book):
    """add-birthday <ім'я> <ДД.ММ.РРРР>"""
    name, date_str, *_ = args
    rec = book.find(name)
    if not rec:
        raise KeyError("Контакт не знайдено")
    rec.add_birthday(date_str)
    return "День народження збережено."


@input_error
def show_birthday(args, book):
    """show-birthday <ім'я>"""
    name, *_ = args
    rec = book.find(name)
    if not rec or not rec.birthday:
        raise KeyError("Немає дня народження")
    return rec.birthday.value.strftime("%d.%m.%Y")


@input_error
def list_birthdays(args, book):
    """birthdays [днів]"""
    days = int(args[0]) if args else 7
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return "Немає найближчих днів народження."
    return "\n".join(f"{n}: {d}" for n, d in upcoming)


# ─────────────────────────── ПОШУК ───────────────────────────

def find_contact(args, book):
    """find <текст> — шукає в імені, телефоні або email"""
    query = " ".join(args).lower()
    result = []
    for rec in book.data.values():
        if query in rec.name.value.lower() or \
           any(query in p.value for p in rec.phones) or \
           any(query in e.value.lower() for e in rec.emails):
            result.append(str(rec))
    return "\n".join(result) if result else "Нічого не знайдено."


# ─────────────────── СЛОВНИКИ КОМАНД ────────────────────

COMMANDS = {
    # базові
    "add": add_contact,
    "phone": show_phones,
    "change": change_phone,
    "delete": delete_contact,
    "all": list_all,
    # email
    "add-email": add_email,
    "change-email": change_email,
    "emails": list_emails,
    # address
    "set-address": set_address,
    "address": show_address,
    # birthday
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": list_birthdays,
    # search
    "find": find_contact,
}

MUTATING = {
    "add", "delete", "change",
    "add-email", "change-email",
    "set-address",
    "add-birthday",
}