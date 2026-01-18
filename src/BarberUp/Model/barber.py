from dataclasses import dataclass
from . import Phone, Email, Password


@dataclass
class Barber:
    id: int
    name: str
    password: Password
    phone: Phone
    email: Email
    active: bool = True
