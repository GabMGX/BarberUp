from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Any
from .repository import Repository
from .db_connection import DBConnection
from .barber_repo import BarberRepo
from .client_repo import ClientRepo
from BarberUp.Model import Appointment, Service, Barber, Client


class AppointmentRepo(Repository[Appointment]):
    def __init__(self, db: DBConnection) -> None:
        self._db = db
        self._barber_repo = BarberRepo(db)
        self._client_repo = ClientRepo(db)

    def _to_datetime(self, value: Any) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except Exception:
                # fallback common DB format
                from datetime import datetime as _dt
                return _dt.strptime(value, "%Y-%m-%d %H:%M:%S")
        raise TypeError("scheduled_at value is not a recognized datetime format")

    def get_by_id(self, id: UUID) -> Appointment | None:
        row = self._db.fetchone(
            "SELECT id, service_id, barber_id, client_id, scheduled_at, finished FROM tb_appointments WHERE id = %s",
            (id.bytes,)
        )
        if row is None:
            return None

        service_id = UUID(bytes=row[1])
        barber_id = UUID(bytes=row[2])
        client_id = UUID(bytes=row[3])

        barber = self._barber_repo.get_by_id(barber_id)
        client = self._client_repo.get_by_id(client_id)

        # If related entities are missing, return None to signal incomplete data
        if barber is None or client is None:
            return None

        service = Service(id=service_id, description="", price=Decimal("0"), active=True)

        return Appointment(
            id=UUID(bytes=row[0]),
            service=service,
            barber=barber,
            client=client,
            scheduled_at=self._to_datetime(row[4]),
            finished=bool(row[5])
        )

    def get_by_barber(self, barber_id: UUID) -> list[Appointment]:
        barber = self._barber_repo.get_by_id(barber_id)
        if barber is None:
            return []

        rows = self._db.fetchall(
            "SELECT id, service_id, barber_id, client_id, scheduled_at, finished FROM tb_appointments WHERE barber_id = %s ORDER BY scheduled_at",
            (barber_id.bytes,)
        )

        appointments: list[Appointment] = []
        client_cache: dict[UUID, Client] = {}

        for row in rows:
            service_id = UUID(bytes=row[1])
            client_id = UUID(bytes=row[3])

            if client_id in client_cache:
                client = client_cache[client_id]
            else:
                client = self._client_repo.get_by_id(client_id)
                if client is None:
                    continue
                client_cache[client_id] = client

            service = Service(id=service_id, description="", price=Decimal("0"), active=True)

            appointments.append(
                Appointment(
                    id=UUID(bytes=row[0]),
                    service=service,
                    barber=barber,
                    client=client,
                    scheduled_at=self._to_datetime(row[4]),
                    finished=bool(row[5]),
                )
            )

        return appointments

    def get_by_client(self, client_id: UUID) -> list[Appointment]:
        client = self._client_repo.get_by_id(client_id)
        if client is None:
            return []

        rows = self._db.fetchall(
            "SELECT id, service_id, barber_id, client_id, scheduled_at, finished FROM tb_appointments WHERE client_id = %s ORDER BY scheduled_at",
            (client_id.bytes,)
        )

        appointments: list[Appointment] = []
        barber_cache: dict[UUID, Barber] = {}

        for row in rows:
            service_id = UUID(bytes=row[1])
            barber_id = UUID(bytes=row[2])

            if barber_id in barber_cache:
                barber = barber_cache[barber_id]
            else:
                barber = self._barber_repo.get_by_id(barber_id)
                if barber is None:
                    continue
                barber_cache[barber_id] = barber

            service = Service(id=service_id, description="", price=Decimal("0"), active=True)

            appointments.append(
                Appointment(
                    id=UUID(bytes=row[0]),
                    service=service,
                    barber=barber,
                    client=client,
                    scheduled_at=self._to_datetime(row[4]),
                    finished=bool(row[5]),
                )
            )

        return appointments

    def get_by_barber_and_date(self, barber_id: UUID, date_str: str) -> list[Appointment]:
        barber = self._barber_repo.get_by_id(barber_id)
        if barber is None:
            return []

        rows = self._db.fetchall(
            "SELECT id, service_id, barber_id, client_id, scheduled_at, finished FROM tb_appointments WHERE barber_id = %s AND DATE(scheduled_at) = %s ORDER BY scheduled_at",
            (barber_id.bytes, date_str)
        )

        appointments: list[Appointment] = []
        client_cache: dict[UUID, Client] = {}

        for row in rows:
            service_id = UUID(bytes=row[1])
            client_id = UUID(bytes=row[3])

            if client_id in client_cache:
                client = client_cache[client_id]
            else:
                client = self._client_repo.get_by_id(client_id)
                if client is None:
                    continue
                client_cache[client_id] = client

            service = Service(id=service_id, description="", price=Decimal("0"), active=True)

            appointments.append(
                Appointment(
                    id=UUID(bytes=row[0]),
                    service=service,
                    barber=barber,
                    client=client,
                    scheduled_at=self._to_datetime(row[4]),
                    finished=bool(row[5]),
                )
            )

        return appointments

    def get_by_client_and_date(self, client_id: UUID, date_str: str) -> list[Appointment]:
        client = self._client_repo.get_by_id(client_id)
        if client is None:
            return []

        rows = self._db.fetchall(
            "SELECT id, service_id, barber_id, client_id, scheduled_at, finished FROM tb_appointments WHERE client_id = %s AND DATE(scheduled_at) = %s ORDER BY scheduled_at",
            (client_id.bytes, date_str)
        )

        appointments: list[Appointment] = []
        barber_cache: dict[UUID, Barber] = {}

        for row in rows:
            service_id = UUID(bytes=row[1])
            barber_id = UUID(bytes=row[2])

            if barber_id in barber_cache:
                barber = barber_cache[barber_id]
            else:
                barber = self._barber_repo.get_by_id(barber_id)
                if barber is None:
                    continue
                barber_cache[barber_id] = barber

            service = Service(id=service_id, description="", price=Decimal("0"), active=True)

            appointments.append(
                Appointment(
                    id=UUID(bytes=row[0]),
                    service=service,
                    barber=barber,
                    client=client,
                    scheduled_at=self._to_datetime(row[4]),
                    finished=bool(row[5]),
                )
            )

        return appointments
    
    def insert(self, entity: Appointment) -> None:
        self._db.execute(
            "INSERT INTO tb_appointments (SELECT id, service_id, barber_id, client_id, scheduled_at, finished) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                entity.id.bytes,
                entity.service.id.bytes,
                entity.barber.id.bytes,
                entity.client.id.bytes,
                entity.scheduled_at,
                entity.finished,
            ),
        )

    def update(self, entity: Appointment) -> None:
        self._db.execute(
            "UPDATE tb_appointments SET service_id = %s, barber_id = %s, client_id = %s, scheduled_at = %s, finished = %s WHERE id = %s",
            (
                entity.service.id.bytes,
                entity.barber.id.bytes,
                entity.client.id.bytes,
                entity.scheduled_at,
                entity.finished,
                entity.id.bytes,
            ),
        )

    def delete(self, id: UUID) -> None:
        self._db.execute("DELETE FROM tb_appointments WHERE id = %s", (id.bytes,))
