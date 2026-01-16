import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract
from typing import Optional, Union


class MySQL:
    def __init__(self) -> None:
        self._connection: Optional[Union[MySQLConnection, PooledMySQLConnection, MySQLConnectionAbstract]] = None

    def connect(self, user: str, password: str, database: str, host: str = "localhost", port: int = 3306) -> Union[MySQLConnection, PooledMySQLConnection, MySQLConnectionAbstract]:
        conn = mysql.connector.connect(user=user, password=password, database=database, host=host, port=port)
        self._connection = conn
        return conn