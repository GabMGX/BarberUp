from dataclasses import dataclass
from datetime import datetime
from BarberUp.Model import Service, Barber, Client


@dataclass
class Appointment:
    id: int
    service: Service
    barber: Barber
    client: Client
    scheduled_at: datetime
    finished: bool = False