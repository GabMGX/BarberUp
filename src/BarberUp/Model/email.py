import re


class Email:
    """Classe para representar um e-mail, imutável, com normalização e validação simples."""

    __slots__ = ("_address",)

    def __init__(self, address: str) -> None:
        self._address: str = self._normalize(address)
    
    @property
    def data(self) -> str:
        """Retorna o e-mail normalizado (minúsculo)."""
        return self._address
    
    def _normalize(self, address: str) -> str:
        address = address.strip().lower()
        pattern = r'^[a-z0-9_.+-]+@[a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,}$'
        if not re.fullmatch(pattern, address):
            raise ValueError(f"{address} não é um email válido.")
        return address
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}( {self._address} )"
