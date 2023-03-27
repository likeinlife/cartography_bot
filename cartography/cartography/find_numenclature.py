from abc import ABC, abstractmethod

from cartography.utils.classes import Alphabet, CoordinatePair
from cartography.utils.types import ImageGenerator, NumenclatList

from .create_image import create_image
from .find_numenclate_functions import get_first, get_numenculat_by_parts


class AbstractFindNumenclature(ABC):
    def __init__(self, coordinates: CoordinatePair) -> None:
        self.coordinates = coordinates
        self.values: NumenclatList = []

    @abstractmethod
    def get_numenculat_values(self) -> NumenclatList:
        ...

    @abstractmethod
    def get_images(self) -> ImageGenerator:
        ...


class FindNumenclat_1M(AbstractFindNumenclature):
    def get_numenculat_values(self) -> NumenclatList:
        self.values = [get_first(self.coordinates)]
        return self.values

    def get_images(self) -> ImageGenerator:
        values = self.get_numenculat_values()
        yield create_image(values[0], 1, [" "])


class FindNumenclat_500k(FindNumenclat_1M):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        this = get_numenculat_by_parts(self.coordinates, 2, previous[0], Alphabet.UPPER_ALPHA)
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_1M(self.coordinates)
        for previous_values in lower_scale.get_images():
            yield previous_values
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[0], 2, Alphabet.UPPER_ALPHA, values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_300k(FindNumenclat_500k):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        numenclature_format = lambda x, y: f"{y}-{x}"
        this = get_numenculat_by_parts(self.coordinates, 3, previous[0], Alphabet.ROMAN, numenclature_format)
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_500k(self.coordinates)
        for previous_values in lower_scale.get_images():
            yield previous_values
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[0], 3, Alphabet.ROMAN, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_200k(FindNumenclat_300k):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        this = get_numenculat_by_parts(self.coordinates, 6, previous[0], Alphabet.ROMAN_EXTENDED)
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_300k(self.coordinates)
        for previous_values in lower_scale.get_images():
            yield previous_values
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[0], 6, Alphabet.ROMAN_EXTENDED, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_100k(FindNumenclat_200k):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        this = get_numenculat_by_parts(self.coordinates, 12, previous[0])
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_200k(self.coordinates)
        for previous_values in lower_scale.get_images():
            yield previous_values
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[0], 12, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_50k(FindNumenclat_100k):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        this = get_numenculat_by_parts(self.coordinates, 2, previous[-1], Alphabet.UPPER_ALPHA)
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_100k(self.coordinates)
        for previous_values in lower_scale.get_images():
            yield previous_values
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[-2], 2, Alphabet.UPPER_ALPHA, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_25k(FindNumenclat_50k):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        this = get_numenculat_by_parts(self.coordinates, 2, previous[-1], Alphabet.LOWER_ALPHA)
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_50k(self.coordinates)
        for previous_values in lower_scale.get_images():
            yield previous_values
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[-2], 2, Alphabet.LOWER_ALPHA, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_10k(FindNumenclat_25k):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        this = get_numenculat_by_parts(self.coordinates, 2, previous[-1])
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_25k(self.coordinates)
        for previous_values in lower_scale.get_images():
            yield previous_values
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[-2], 2, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_5k(FindNumenclat_10k):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        numenclature_format = lambda x, y: f"{x}-({y})"
        this = get_numenculat_by_parts(self.coordinates, 16, previous[-4], numenclature_format=numenclature_format)
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_10k(self.coordinates)
        for previous_values in lower_scale.get_images():
            yield previous_values
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[-5], 16, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_2k(FindNumenclat_5k):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        numenclature_format = lambda x, y: f"{x}-({y})"
        this = get_numenculat_by_parts(
            self.coordinates,
            3,
            previous[-1],
            Alphabet.LOWER_ALPHA_EXTENDENT,
            numenclature_format,
        )
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_5k(self.coordinates)
        for previous_values in lower_scale.get_images():
            yield previous_values
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[-2], 3, Alphabet.LOWER_ALPHA_EXTENDENT, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])
