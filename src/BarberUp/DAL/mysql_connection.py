import mysql.connector
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from typing import Union, Tuple, Any, Optional, List
from .db_connection import DBConnection


class MySQLConnection(DBConnection):
    def __init__(self, user: str, password: str, database: str, host: str = "localhost", port: int = 3306) -> None:
        self._connection: Union[MySQLConnectionAbstract, 
                                PooledMySQLConnection] = mysql.connector.connect(user=user, 
                                                                                password=password, 
                                                                                database=database, 
                                                                                host=host, 
                                                                                port=port)
    
    def execute(self, query: str, params: Tuple[Any, ...] = ()) -> None:
        cursor: MySQLCursorAbstract = self._connection.cursor()
        try:
            cursor.execute(query, params)
            self._connection.commit()
        finally:
            cursor.close()
    
    def fetchone(self, query: str, params: Tuple[Any, ...] = ()) -> Optional[Tuple[Any, ...]]:
        cursor: MySQLCursorAbstract = self._connection.cursor(dictionary=False)
        try:
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row is None:
                return None
            assert isinstance(row, tuple)
            return row
        finally:
            cursor.close()

    def fetchall(self, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
        cursor: MySQLCursorAbstract = self._connection.cursor(dictionary=False)
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            result: list[Tuple[Any, ...]] = []
            for row in rows:
                assert isinstance(row, tuple)
                result.append(row)
            return result
        finally:
            cursor.close()
