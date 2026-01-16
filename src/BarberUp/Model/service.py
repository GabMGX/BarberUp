from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Service:
    id: int
    description: str
    price: Decimal
    active: bool
