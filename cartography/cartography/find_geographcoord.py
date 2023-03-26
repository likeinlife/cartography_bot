from abc import ABC, abstractmethod
from typing import Generator, TypeAlias
from cartography.utils.classes import Alphabet, Numenclat
from .find_geograph_functions import get_first, get_part
from .create_image import create_image

NumenclatList: TypeAlias = list[Numenclat]
ImageGenerator: TypeAlias = Generator[bytes, None, None]


class AbstractFindNumenclature(ABC):

    def __init__(self, numenclature: dict) -> None:
        """
        Args:
            numenclature (dict): {'m1': 'N-44', 'k500': 'А'}
        """
        self.numenclature: dict = numenclature

    @abstractmethod
    def get_numenculat_values(self) -> NumenclatList:
        ...

    @abstractmethod
    def get_images(self) -> ImageGenerator:
        ...


class FindNumenclat_1M(AbstractFindNumenclature):

    def get_numenculat_values(self) -> NumenclatList:
        return [get_first(self.numenclature['m1'])]

    def get_images(self) -> ImageGenerator:
        yield create_image(self.get_numenculat_values()[0], 1, [' '])


class FindNumenclat_500k(FindNumenclat_1M):

    def get_numenculat_values(self) -> NumenclatList:
        previous = super().get_numenculat_values()
        this = get_part(self.numenclature['k500'], previous[0], 2, Alphabet.UPPER_ALPHA)
        return previous + [this]

    def get_images(self) -> ImageGenerator:
        for previous_images in FindNumenclat_1M(self.numenclature).get_images():
            yield previous_images
        values = self.get_numenculat_values()
        yield create_image(values[0], 2, Alphabet.UPPER_ALPHA)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_300k(FindNumenclat_1M):

    def get_numenculat_values(self) -> NumenclatList:
        previous = super().get_numenculat_values()
        this = get_part(self.numenclature['k300'], previous[0], 3, Alphabet.ROMAN)
        return previous + [this]

    def get_images(self) -> ImageGenerator:
        for previous_images in FindNumenclat_1M(self.numenclature).get_images():
            yield previous_images
        values = self.get_numenculat_values()
        yield create_image(values[0], 3, Alphabet.ROMAN)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_200k(FindNumenclat_1M):

    def get_numenculat_values(self) -> NumenclatList:
        previous = super().get_numenculat_values()
        this = get_part(self.numenclature['k200'], previous[0], 6)
        return previous + [this]

    def get_images(self) -> ImageGenerator:
        for previous_images in FindNumenclat_1M(self.numenclature).get_images():
            yield previous_images
        values = self.get_numenculat_values()
        yield create_image(values[0], 6)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_100k(FindNumenclat_1M):

    def get_numenculat_values(self) -> NumenclatList:
        previous = super().get_numenculat_values()
        this = get_part(self.numenclature['k100'], previous[0], 12)
        return previous + [this]

    def get_images(self) -> ImageGenerator:
        for previous_images in FindNumenclat_1M(self.numenclature).get_images():
            yield previous_images
        values = self.get_numenculat_values()
        yield create_image(values[0], 12)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_50k(FindNumenclat_100k):

    def get_numenculat_values(self) -> NumenclatList:
        previous = super().get_numenculat_values()
        this = get_part(self.numenclature['k50'], previous[-1], 2, Alphabet.UPPER_ALPHA)
        return previous + [this]

    def get_images(self) -> ImageGenerator:
        for previous_images in FindNumenclat_100k(self.numenclature).get_images():
            yield previous_images
        values = self.get_numenculat_values()
        yield create_image(values[-2], 2, Alphabet.UPPER_ALPHA)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_25k(FindNumenclat_50k):

    def get_numenculat_values(self) -> NumenclatList:
        previous = super().get_numenculat_values()
        this = get_part(self.numenclature['k25'], previous[-1], 2, Alphabet.LOWER_ALPHA)
        return previous + [this]

    def get_images(self) -> ImageGenerator:
        for previous_images in FindNumenclat_50k(self.numenclature).get_images():
            yield previous_images
        values = self.get_numenculat_values()
        yield create_image(values[-2], 2, Alphabet.LOWER_ALPHA)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_10k(FindNumenclat_25k):

    def get_numenculat_values(self) -> NumenclatList:
        previous = super().get_numenculat_values()
        this = get_part(self.numenclature['k10'], previous[-1], 2)
        return previous + [this]

    def get_images(self) -> ImageGenerator:
        for previous_images in FindNumenclat_25k(self.numenclature).get_images():
            yield previous_images
        values = self.get_numenculat_values()
        yield create_image(values[-2], 2)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_5k(FindNumenclat_100k):

    def get_numenculat_values(self) -> NumenclatList:
        previous = super().get_numenculat_values()
        this = get_part(self.numenclature['k5'], previous[-1], 16)
        return previous + [this]

    def get_images(self) -> ImageGenerator:
        for previous_images in FindNumenclat_100k(self.numenclature).get_images():
            yield previous_images
        values = self.get_numenculat_values()
        yield create_image(values[-5], 16)
        yield create_image(values[-1], 1, [' '])


class FindNumenclat_2k(FindNumenclat_5k):

    def get_numenculat_values(self) -> NumenclatList:
        previous = super().get_numenculat_values()
        this = get_part(self.numenclature['k2'], previous[-1], 3, Alphabet.LOWER_ALPHA_EXTENDENT)
        return previous + [this]

    def get_images(self) -> ImageGenerator:
        for previous_images in FindNumenclat_5k(self.numenclature).get_images():
            yield previous_images
        values = self.get_numenculat_values()
        yield create_image(values[-2], 3, Alphabet.LOWER_ALPHA_EXTENDENT)
        yield create_image(values[-1], 1, [' '])