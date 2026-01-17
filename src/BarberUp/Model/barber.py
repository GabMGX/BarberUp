from dataclasses import dataclass
from . import Phone, Email


@dataclass
class Barber:
    id: int
    name: str
    phone: Phone
    email: Email
    active: bool = True
