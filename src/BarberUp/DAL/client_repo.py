from uuid import UUID
from .repository import Repository
from .db_connection import DBConnection
from BarberUp.Model import Client, Password, Phone, Email


class ClientRepo(Repository[Client]):
    def __init__(self, db: DBConnection) -> None:
        self._db = db
        
    def get_by_id(self, id: UUID) -> Client | None:
        row = self._db.fetchone("SELECT id, name, pwd_hash, phone, email, active FROM tb_clients WHERE id = %s", (id.bytes,))
        if row is None:
            return None
        
        return Client(
            id=UUID(bytes=row[0]),
            name=row[1],
            password=Password(row[2]),
            phone=Phone(row[3]),
            email=Email(row[4]),
            active=bool(row[5])
        )

    def insert(self, entity: Client) -> None:
        self._db.execute(
            "INSERT INTO tb_clients (id, name, pwd_hash, phone, email, active) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                entity.id.bytes,
                entity.name,
                entity.password.data,
                entity.phone.data,
                entity.email.data,
                entity.active
            )
        )

    def update(self, entity: Client) -> None:
        self._db.execute(
            "UPDATE tb_clients SET name = %s, pwd_hash = %s, phone = %s, email = %s, active = %s WHERE id = %s",
            (
                entity.name,
                entity.password.data,
                entity.phone.data,
                entity.email.data,
                entity.active,
                entity.id.bytes
            )
        )

    def delete(self, id: UUID) -> None:
        self._db.execute("UPDATE tb_clients SET active = FALSE WHERE id = %s", (id.bytes,))
