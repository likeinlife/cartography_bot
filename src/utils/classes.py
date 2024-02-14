from __future__ import annotations

from decimal import Decimal
from math import floor
from typing import NamedTuple


class Alphabet:
    LOWER_ALPHA = ["а", "б", "в", "г"]
    LOWER_ALPHA_EXTENDENT = ["а", "б", "в", "г", "д", "е", "ж", "з", "и"]
    UPPER_ALPHA = ["А", "Б", "В", "Г"]
    NUMBERS = ["1", "2", "3", "4"]
    ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VII", "VIII", "IX"]
    ROMAN_EXTENDED = [
        "I",
        "II",
        "III",
        "IV",
        "V",
        "VI",
        "VII",
        "VIII",
        "IX",
        "X",
        "XI",
        "XII",
        "XIII",
        "XIV",
        "XV",
        "XVI",
        "XVII",
        "XVIII",
        "XIX",
        "XX",
        "XXI",
        "XXII",
        "XXIII",
        "XXIV",
        "XXV",
        "XXVI",
        "XXVII",
        "XXVIII",
        "XXIX",
        "XXX",
        "XXXI",
        "XXXII",
        "XXXIII",
        "XXXIV",
        "XXXV",
        "XXXVI",
    ]


class Degrees:
    def __init__(
        self,
        degree: int | Decimal = 0,
        minute: int | Decimal = 0,
        second: Decimal | int = 0,
    ) -> None:
        self.degree = degree
        self.minute = minute
        if second == int(second):
            self.second: int | Decimal = int(second)
        else:
            self.second = Decimal(str(second))

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Degrees):
            return all(
                [
                    self.degree == __o.degree,
                    self.minute == __o.minute,
                    self.second == __o.second,
                ]
            )
        raise Exception("Not a Degrees instance")

    def __add__(self, __o: Degrees):
        return Degrees.collectFromSeconds(self.getAllInSeconds() + __o.getAllInSeconds())

    def __sub__(self, __o: Degrees):
        return Degrees.collectFromSeconds(self.getAllInSeconds() - __o.getAllInSeconds())

    def __lt__(self, __o: Degrees):
        return self.getAllInSeconds() < __o.getAllInSeconds()

    def __gt__(self, __o: Degrees):
        return self.getAllInSeconds() > __o.getAllInSeconds()

    def __truediv__(self, divider: int):
        return self.collectFromSeconds(Decimal(self.getAllInSeconds()) / Decimal(divider))

    def __mul__(self, multiplyer: int):
        return self.collectFromSeconds(self.getAllInSeconds() * multiplyer)

    @staticmethod
    def collectFromSeconds(all_seconds: Decimal) -> Degrees:
        degree = floor(all_seconds // 3600)
        all_seconds -= degree * 3600
        minute = floor(all_seconds // 60)
        all_seconds -= minute * 60
        second = all_seconds
        return Degrees(degree, minute, second)

    @staticmethod
    def findCenter(first: Degrees, second: Degrees) -> Degrees:
        return Degrees.collectFromSeconds((first.getAllInSeconds() + second.getAllInSeconds()) // 2)

    def getAllInSeconds(self) -> Decimal:
        return Decimal(self.degree) * 3600 + Decimal(self.minute) * 60 + Decimal(self.second)

    def __repr__(self) -> str:
        degree = (f'{f"{self.degree}°" if self.degree else " "}').rjust(4, " ")
        minute = (f'{f"{self.minute}′" if self.minute else " "}').rjust(4, " ")
        second = (f'{f"{round(self.second, 2)}″" if self.second else " "}').rjust(6, " ")
        return f"{degree}{minute}{second}"


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
        return f"φ = {self.latitude} ;λ = {self.longitude}"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, CoordinatePair):
            return all([self.latitude == __o.latitude, self.longitude == __o.longitude])
        return False


class Numenclat(NamedTuple):
    lower_bound: CoordinatePair
    upper_bound: CoordinatePair
    numenculat: str
    delta: CoordinatePair = CoordinatePair(0, 0)
    part: str = ""

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Numenclat):
            return all(
                [
                    self.lower_bound == __o.lower_bound,
                    self.upper_bound == __o.upper_bound,
                    self.numenculat == __o.numenculat,
                ]
            )
        return False

    def __repr__(self) -> str:
        content = (
            f"{self.numenculat}\n"
            f"φ: {self.lower_bound.latitude} - {self.upper_bound.latitude}\n"
            f"λ: {self.lower_bound.longitude} - {self.upper_bound.longitude}"
        )
        return content


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (180, 180, 180)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (70, 70, 255)
    GREEN = (0, 255, 0)
    LIGHT_GREEN = (70, 255, 70)
    RED = (255, 0, 0)
    LIGHT_RED = (255, 70, 70)
