import webview


class API:
    def singin(self, username, email, phone, password, type):
        print(f"Username: {username}, E-mail: {email}, Telefone: {phone}, Password: {password}, Tipo: {type}")


webview.create_window("BarberUp", "Frontend/index.html", width=390, height=720, js_api=API())
webview.start()
