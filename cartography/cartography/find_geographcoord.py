from abc import ABC, abstractmethod

from cartography.utils.classes import Alphabet
from cartography.utils.types import ImageGenerator, NumenclatList

from .create_image import create_image
from .find_geograph_functions import get_first, get_part

NumenclatList: TypeAlias = list[Numenclat]
ImageGenerator: TypeAlias = Generator[bytes, None, None]


class AbstractFindNumenclature(ABC):
    def __init__(self, numenclature: dict) -> None:
        self.numenclature: dict = numenclature
        self.values: NumenclatList = []

    @abstractmethod
    def get_numenculat_values(self) -> NumenclatList:
        ...

    @abstractmethod
    def get_images(self) -> ImageGenerator:
        ...


class FindNumenclat_1M(AbstractFindNumenclature):
    def get_numenculat_values(self) -> NumenclatList:
        self.values = [get_first(self.numenclature["m1"])]
        return self.values

    def get_images(self) -> ImageGenerator:
        yield create_image(self.get_numenculat_values()[0], 1, [" "])


class FindNumenclat_500k(FindNumenclat_1M):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        this = get_part(self.numenclature["k500"], previous[0], 2, Alphabet.UPPER_ALPHA)
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_1M(self.numenclature)
        for previous_images in lower_scale.get_images():
            yield previous_images
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[0], 2, Alphabet.UPPER_ALPHA, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_300k(FindNumenclat_1M):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        numenclature_format = lambda x, y: f"{y}-{x}"
        this = get_part(
            self.numenclature["k300"],
            previous[0],
            3,
            Alphabet.ROMAN,
            numenclature_format,
        )
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_1M(self.numenclature)
        for previous_images in lower_scale.get_images():
            yield previous_images
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[0], 3, Alphabet.ROMAN, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_200k(FindNumenclat_1M):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        this = get_part(self.numenclature["k200"], previous[0], 6)
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_1M(self.numenclature)
        for previous_images in lower_scale.get_images():
            yield previous_images
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[0], 6, Alphabet.ROMAN_EXTENDED, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_100k(FindNumenclat_1M):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        this = get_part(self.numenclature["k100"], previous[0], 12)
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_1M(self.numenclature)
        for previous_images in lower_scale.get_images():
            yield previous_images
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[0], 12, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_50k(FindNumenclat_100k):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        this = get_part(self.numenclature["k50"], previous[-1], 2, Alphabet.UPPER_ALPHA)
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_100k(self.numenclature)
        for previous_images in lower_scale.get_images():
            yield previous_images
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[-2], 2, Alphabet.UPPER_ALPHA, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_25k(FindNumenclat_50k):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        this = get_part(self.numenclature["k25"], previous[-1], 2, Alphabet.LOWER_ALPHA)
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_50k(self.numenclature)
        for previous_images in lower_scale.get_images():
            yield previous_images
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[-2], 2, Alphabet.LOWER_ALPHA, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_10k(FindNumenclat_25k):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        this = get_part(self.numenclature["k10"], previous[-1], 2)
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_25k(self.numenclature)
        for previous_images in lower_scale.get_images():
            yield previous_images
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[-2], 2, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_5k(FindNumenclat_100k):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        numenclature_format = lambda x, y: f"{x}-({y})"
        this = get_part(
            self.numenclature["k5"],
            previous[-1],
            16,
            numenclature_format=numenclature_format,
        )
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_100k(self.numenclature)
        for previous_images in lower_scale.get_images():
            yield previous_images
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[-5], 16, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])


class FindNumenclat_2k(FindNumenclat_5k):
    def get_numenculat_values(self) -> NumenclatList:
        previous = self.values if self.values else super().get_numenculat_values()
        numenclature_format = lambda x, y: f"{x}-({y})"
        this = get_part(
            self.numenclature["k2"],
            previous[-1],
            3,
            Alphabet.LOWER_ALPHA_EXTENDENT,
            numenclature_format,
        )
        self.values = previous + [this]
        return self.values

    def get_images(self) -> ImageGenerator:
        lower_scale = FindNumenclat_5k(self.numenclature)
        for previous_images in lower_scale.get_images():
            yield previous_images
        self.values = lower_scale.values
        values = self.get_numenculat_values()
        yield create_image(values[-2], 3, Alphabet.LOWER_ALPHA_EXTENDENT, cell_to_fill=values[-1].part)
        yield create_image(values[-1], 1, [" "])
