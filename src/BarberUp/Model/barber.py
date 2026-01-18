from dataclasses import dataclass
from uuid import UUID
from . import Phone, Email, Password


@dataclass
class Barber:
    id: UUID
    name: str
    password: Password
    phone: Phone
    email: Email
    active: bool = True
