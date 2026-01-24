from uuid import uuid7
from decimal import Decimal
import mysql.connector
from configparser import ConfigParser

# =========================================================
# Instância da conexão
# =========================================================
config = ConfigParser()
config.read("src/config.ini")

conn = mysql.connector.connect(
    user=config.get("database", "user"), 
    password=config.get("database", "password"), 
    host=config.get("database", "host"), 
    database=config.get("database", "database"), 
    port=config.getint("database", "port")
    )

cursor = conn.cursor()

# =========================================================
# Cortes reais + preços estimados (R$)
# =========================================================
haircuts = [
    ("Corte social", Decimal("30.00")),
    ("Corte degradê", Decimal("35.00")),
    ("Degradê navalhado", Decimal("40.00")),
    ("Corte americano", Decimal("35.00")),
    ("Corte militar", Decimal("25.00")),
    ("Corte infantil", Decimal("25.00")),
    ("Corte disfarçado", Decimal("30.00")),
    ("Low fade", Decimal("35.00")),
    ("Mid fade", Decimal("38.00")),
    ("High fade", Decimal("40.00")),
    ("Buzz cut", Decimal("25.00")),
    ("Undercut", Decimal("40.00")),
    ("Corte freestyle", Decimal("45.00")),
    ("Corte + barba", Decimal("55.00")),
    ("Barba simples", Decimal("20.00")),
    ("Barba completa", Decimal("30.00")),
    ("Barba com toalha quente", Decimal("40.00")),
]

# =========================================================
# Insert
# =========================================================
sql = """INSERT INTO tb_services (id, description, price) VALUES (%s, %s, %s)"""

for description, price in haircuts:
    uid = uuid7()
    cursor.execute(sql,(uid.bytes, description, price))

conn.commit()
cursor.close()
conn.close()

print("Seed de cortes de cabelo concluído com sucesso.")
