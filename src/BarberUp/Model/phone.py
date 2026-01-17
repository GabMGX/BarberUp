import re


class Phone:
    """Classe para representar um número de celular brasileiro no formato internacional."""

    __slots__ = ("_number",)

    def __init__(self, number: str) -> None:
        self._number = self._normalize(number)

    @property
    def view(self) -> str:
        """Retorna o número formatado amigavelmente (ex: +55 (11) 99999-9999)."""
        ddi: str = self._number[:2]
        ddd: str = self._number[2:4]
        part1: str = self._number[4:9]
        part2: str = self._number[9:]
        return f"+{ddi} ({ddd}) {part1}-{part2}"
    
    @property
    def data(self) -> str:
        """Retorna o número puro, no formato internacional (ex: 5511999999999)."""
        return self._number
    
    def _normalize(self, number: str) -> str:
        number = re.sub(r'\D', '', number)
        if len(number) == 11:
            number = "55" + number
        if len(number) != 13 or not number.startswith("55") or number[4] != "9":
            raise ValueError(f"{number} não é um número de celular brasileiro válido.")
        return number
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}( {self.view} )"