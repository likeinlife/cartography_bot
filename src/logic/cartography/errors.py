from dataclasses import dataclass

from domain.errors import BaseError


class CartographyError(BaseError):
    @property
    def msg(self) -> str:
        return "Cartography error"


@dataclass
class PartNomenclatureError(CartographyError):
    part: str

    @property
    def msg(self) -> str:
        return f"Некорректная часть номенклатуры: {self.part}"


@dataclass
class NoLatitudeCharError(CartographyError):
    latitude: str

    @property
    def msg(self) -> str:
        return f"Некорректная широта: {self.latitude}"


@dataclass
class NoLongitudeIndexError(CartographyError):
    longitude: str

    @property
    def msg(self) -> str:
        return f"Некорректная долгота: {self.longitude}"


@dataclass
class InvalidNomenclatureTitleError(CartographyError):
    nomenclature: str

    @property
    def msg(self) -> str:
        return f"Некорректная номенклатура: {self.nomenclature}"
