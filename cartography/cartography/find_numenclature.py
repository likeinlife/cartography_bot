from abc import ABC, abstractmethod
from typing import Generator
from cartography.utils.classes import Alphabet, CoordinatePair, Numenclat
from .find_numenclate_functions import get_first, get_numenculat_by_parts
from .create_image import create_image


class AbstractFindNumenclature(ABC):

    def __init__(self, coordinates: CoordinatePair) -> None:
        self.coordinates = coordinates

    @abstractmethod
    def get_numenculat_values(self) -> list[Numenclat]:
        ...

    @abstractmethod
    def get_images(self) -> Generator[bytes, None, None]:
        ...


class FindNumenclat_1M(AbstractFindNumenclature):

    def get_numenculat_values(self) -> list[Numenclat]:
        return [get_first(self.coordinates)]

    def get_images(self) -> Generator[bytes, None, None]:
        yield create_image(self.get_numenculat_values()[0], 1, [' '])


class FindNumenclat_500k(FindNumenclat_1M):

    def get_numenculat_values(self) -> list[Numenclat]:
        previous = super().get_numenculat_values()
        this = get_numenculat_by_parts(self.coordinates, 2, previous[0], Alphabet.UPPER_ALPHA)
        return previous + [this]

    def get_images(self) -> Generator[bytes, None, None]:
        for previous_values in FindNumenclat_1M(self.coordinates).get_images():
            yield previous_values
        values = self.get_numenculat_values()
        yield create_image(values[0], 2, Alphabet.UPPER_ALPHA)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_300k(FindNumenclat_500k):

    def get_numenculat_values(self) -> list[Numenclat]:
        previous = super().get_numenculat_values()
        numenclature_format = lambda x, y: f'{y}-{x}'
        this = get_numenculat_by_parts(self.coordinates, 3, previous[0], Alphabet.ROMAN, numenclature_format)
        return previous + [this]

    def get_images(self) -> Generator[bytes, None, None]:
        for previous_values in FindNumenclat_500k(self.coordinates).get_images():
            yield previous_values
        values = self.get_numenculat_values()
        yield create_image(values[0], 3, Alphabet.ROMAN)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_200k(FindNumenclat_300k):

    def get_numenculat_values(self) -> list[Numenclat]:
        previous = super().get_numenculat_values()
        this = get_numenculat_by_parts(self.coordinates, 6, previous[0])
        return previous + [this]

    def get_images(self) -> Generator[bytes, None, None]:
        for previous_values in FindNumenclat_300k(self.coordinates).get_images():
            yield previous_values
        values = self.get_numenculat_values()
        yield create_image(values[0], 6)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_100k(FindNumenclat_200k):

    def get_numenculat_values(self) -> list[Numenclat]:
        previous = super().get_numenculat_values()
        this = get_numenculat_by_parts(self.coordinates, 12, previous[0])
        return previous + [this]

    def get_images(self) -> Generator[bytes, None, None]:
        for previous_values in FindNumenclat_200k(self.coordinates).get_images():
            yield previous_values
        values = self.get_numenculat_values()
        yield create_image(values[0], 12)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_50k(FindNumenclat_100k):

    def get_numenculat_values(self) -> list[Numenclat]:
        previous = super().get_numenculat_values()
        this = get_numenculat_by_parts(self.coordinates, 2, previous[-1], Alphabet.UPPER_ALPHA)
        return previous + [this]

    def get_images(self) -> Generator[bytes, None, None]:
        for previous_values in FindNumenclat_100k(self.coordinates).get_images():
            yield previous_values
        values = self.get_numenculat_values()
        yield create_image(values[-2], 2, Alphabet.UPPER_ALPHA)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_25k(FindNumenclat_50k):

    def get_numenculat_values(self) -> list[Numenclat]:
        previous = super().get_numenculat_values()
        this = get_numenculat_by_parts(self.coordinates, 2, previous[-1], Alphabet.LOWER_ALPHA)
        return previous + [this]

    def get_images(self) -> Generator[bytes, None, None]:
        for previous_values in FindNumenclat_50k(self.coordinates).get_images():
            yield previous_values
        values = self.get_numenculat_values()
        yield create_image(values[-2], 2, Alphabet.LOWER_ALPHA)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_10k(FindNumenclat_25k):

    def get_numenculat_values(self) -> list[Numenclat]:
        previous = super().get_numenculat_values()
        this = get_numenculat_by_parts(self.coordinates, 2, previous[-1])
        return previous + [this]

    def get_images(self) -> Generator[bytes, None, None]:
        for previous_values in FindNumenclat_25k(self.coordinates).get_images():
            yield previous_values
        values = self.get_numenculat_values()
        yield create_image(values[-2], 2)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_5k(FindNumenclat_10k):

    def get_numenculat_values(self) -> list[Numenclat]:
        previous = super().get_numenculat_values()
        numenclature_format = lambda x, y: f'{x}-({y})'
        this = get_numenculat_by_parts(self.coordinates, 16, previous[-4], numenclature_format=numenclature_format)
        return previous + [this]

    def get_images(self) -> Generator[bytes, None, None]:
        for previous_values in FindNumenclat_10k(self.coordinates).get_images():
            yield previous_values
        values = self.get_numenculat_values()
        yield create_image(values[-5], 16)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_2k(FindNumenclat_5k):

    def get_numenculat_values(self) -> list[Numenclat]:
        previous = super().get_numenculat_values()
        numenclature_format = lambda x, y: f'{x}-({y})'
        this = get_numenculat_by_parts(self.coordinates, 3, previous[-1], Alphabet.LOWER_ALPHA_EXTENDENT,
                                       numenclature_format)
        return previous + [this]

    def get_images(self) -> Generator[bytes, None, None]:
        for previous_values in FindNumenclat_5k(self.coordinates).get_images():
            yield previous_values
        values = self.get_numenculat_values()
        yield create_image(values[-2], 3, Alphabet.LOWER_ALPHA_EXTENDENT)
        yield create_image(values[-1], 1, [' '])