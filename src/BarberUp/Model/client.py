from dataclasses import dataclass
from BarberUp.Model import Phone, Email


@dataclass
class Client:
    id: int
    name: str
    phone: Phone
    email: Email
    active: bool = True