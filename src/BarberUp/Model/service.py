from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass
class Service:
    id: UUID
    description: str
    price: Decimal
    active: bool
