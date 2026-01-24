import webview
from configparser import ConfigParser
from uuid import uuid7
from .Model import Barber, Client, Password, Phone, Email
from .DAL import BarberRepo, ClientRepo, MySQLConnection


config = ConfigParser()
config.read("config.ini")

db = MySQLConnection(
    user=config.get("database", "user"), 
    password=config.get("database", "password"), 
    host=config.get("database", "host"), 
    database=config.get("database", "database"), 
    port=config.getint("database", "port")
    )

cur_user = None


class API:
    def singin(self, username: str, email: str, phone: str, password: str, type: str) -> dict[str, str]:
        id = uuid7()
        pwd: Password = Password.hash(password)
        try:
            phoneN = Phone(phone)
        except ValueError as e:
            return {"error": str(e)}
        
        if type == "barbeiro":
            user: Barber | Client = Barber(id, username, pwd, phoneN, Email(email))
            BarberRepo(db).insert(user)
        else:
            user: Barber | Client = Client(id, username, pwd, phoneN, Email(email))
            ClientRepo(db).insert(user)

        return {"id": str(user.id), "name": user.name}

    def login(self, email: str, password: str, type: str) -> dict[str, str]:
        global cur_user

        try:
            emailM = Email(email)
        except ValueError as e:
            return {"error": str(e)}
        
        if type == "barbeiro":
            user = BarberRepo(db).get_by_email(emailM.data)
        else:
            user = ClientRepo(db).get_by_email(emailM.data)

        if not user:
            return {"error": "Usuário não encontrado."}
        if not user.password.verify(password):
            return {"error": "Senha inválida."}

        cur_user = user
        return {"id": str(user.id), "name": user.name}
    
    def getAvailableBarbers(self) -> list[dict[str, str]]:
        barbers = BarberRepo(db).get_all()
        return [{"id": str(barber.id), "name": barber.name} for barber in barbers]

    def getAppointments(self, barber_id: str, date: str) -> list[dict[str, str]]:
        from uuid import UUID
        from .DAL.appointment_repo import AppointmentRepo

        try:
            barber_uuid = UUID(barber_id)
        except Exception:
            return []

        repo = AppointmentRepo(db)
        appts = repo.get_by_barber_and_date(barber_uuid, date)

        result: list[dict[str, str]] = []
        for a in appts:
            time_str = a.scheduled_at.strftime("%H:%M")
            result.append({
                "id": str(a.id),
                "client": a.client.name,
                "date": a.scheduled_at.date().isoformat(),
                "time": time_str,
            })

        return result


webview.create_window("BarberUp", "Frontend/index.html", width=390, height=720, js_api=API(), min_size=(390, 720), resizable=False)
webview.start(debug=True)
