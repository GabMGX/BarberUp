from argon2 import PasswordHasher, exceptions


class Password:
    _hasher = PasswordHasher()

    @classmethod
    def hash(cls, plain_password: str) -> Password:
        pwd_hash = cls._hasher.hash(plain_password)
        return cls(pwd_hash)

    def __init__(self, password_hash: str):
        self._password_hash = password_hash

    @property
    def data(self) -> str:
        return self._password_hash
    
    def verify(self, plain_password: str) -> bool:
        try:
            return self.__class__._hasher.verify(self._password_hash, plain_password)
        except exceptions.VerifyMismatchError:
            return False
        
    def __repr__(self) -> str: 
        return f"{self.__class__.__name__}( **** )"
