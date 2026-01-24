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

        return {"id": user.name}

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
        return {"id": user.id.hex, "name": user.name}


webview.create_window("BarberUp", "Frontend/index.html", width=390, height=720, js_api=API(), min_size=(390, 720), resizable=False)
webview.start(debug=True)
