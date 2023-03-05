from __future__ import annotations
from typing import NamedTuple
from tabulate import tabulate


class Alphabet:
    LOWER_ALPHA = ['а', 'б', 'в', 'г']
    LOWER_ALPHA_EXTENDENT = ['а', 'б', 'в', 'г', 'е', 'ж', 'з', 'и']
    UPPER_ALPHA = ['А', 'Б', 'В', 'Г']
    NUMBERS = ['1', '2', '3', '4']


class Degrees:

    def __init__(self, degree: int | float = 0, minute: int | float = 0, second: float | int = 0) -> None:
        self.degree = degree
        self.minute = minute
        if second == int(second):
            self.second = int(second)
        else:
            self.second = round(second, 2)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Degrees):
            return all([self.degree == __o.degree, self.minute == __o.minute, self.second == __o.second])
        raise Exception('Not a Degrees instance')

    def __add__(self, __o: Degrees):
        return Degrees.collectFromSeconds(self.getAllInSeconds() + __o.getAllInSeconds())

    def __sub__(self, __o: Degrees):
        return Degrees.collectFromSeconds(self.getAllInSeconds() - __o.getAllInSeconds())

    def __lt__(self, __o: Degrees):
        return self.getAllInSeconds() < __o.getAllInSeconds()

    def __gt__(self, __o: Degrees):
        return self.getAllInSeconds() > __o.getAllInSeconds()

    def __truediv__(self, divider: int):
        return self.collectFromSeconds(self.getAllInSeconds() / divider)

    def __mul__(self, multiplyer: int):
        return self.collectFromSeconds(self.getAllInSeconds() * multiplyer)

    @staticmethod
    def collectFromSeconds(all_seconds: float) -> Degrees:
        degree = round(all_seconds // 3600)
        all_seconds -= degree * 3600
        minute = round(all_seconds // 60)
        all_seconds -= minute * 60
        second = all_seconds
        return Degrees(degree, minute, second)

    @staticmethod
    def findCenter(first: Degrees, second: Degrees) -> Degrees:
        return Degrees.collectFromSeconds((first.getAllInSeconds() + second.getAllInSeconds()) // 2)

    def getAllInSeconds(self) -> float:
        return self.degree * 3600 + self.minute * 60 + self.second

    def __repr__(self) -> str:
        degree = (f'{f"{self.degree}°" if self.degree else " "}').rjust(4, ' ')
        minute = (f'{f"{self.minute}′" if self.minute else " "}').rjust(4, ' ')
        second = (f'{f"{self.second}″" if self.second else " "}').rjust(6, ' ')
        return f'{degree}{minute}{second}'


class CoordinatePair:

    def __init__(self, latitude: Degrees | int, longitude: Degrees | int) -> None:
        if isinstance(latitude, int):
            self.latitude = Degrees(latitude)
        else:
            self.latitude = latitude
        if isinstance(longitude, int):
            self.longitude = Degrees(longitude)
        else:
            self.longitude = longitude

    def __repr__(self) -> str:
        return f'φ = {self.latitude} ;λ = {self.longitude}'

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, CoordinatePair):
            return all([self.latitude == __o.latitude, self.longitude == __o.longitude])
        return False


class Numenculat(NamedTuple):
    lower_bound: CoordinatePair
    upper_bound: CoordinatePair
    numenculat: str
    delta: CoordinatePair = CoordinatePair(0, 0)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Numenculat):
            return all([
                self.lower_bound == __o.lower_bound, self.upper_bound == __o.upper_bound,
                self.numenculat == __o.numenculat
            ])
        return False

    def __repr__(self) -> str:
        headers = ('φ', 'λ')
        content = ((str(self.lower_bound.latitude), str(self.lower_bound.longitude)), (str(self.upper_bound.latitude),
                                                                                       str(self.upper_bound.longitude)))
        tab = tabulate(content, headers, tablefmt='simple_outline')
        summarize = f'<pre>{self.numenculat: ^20}\n{tab}</pre>'
        return summarize
