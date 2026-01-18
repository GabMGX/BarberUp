from dataclasses import dataclass
from . import Phone, Email, Password


@dataclass
class Client:
    id: int
    name: str
    password: Password
    phone: Phone
    email: Email
    active: bool = True
