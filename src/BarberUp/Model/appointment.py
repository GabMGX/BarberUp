from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from . import Service, Barber, Client


@dataclass
class Appointment:
    id: UUID
    service: Service
    barber: Barber
    client: Client
    scheduled_at: datetime
    finished: bool = False
