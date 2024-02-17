from typing import Any

from errors import BaseMsgError


class AdditionalInputMixin(BaseMsgError):
    msg: str

    def __init__(self, info: Any) -> None:
        self.msg = self.msg + f": {info}"


class PartNomenclatureError(AdditionalInputMixin):
    msg = "Некорректная часть номенклатуры"


class InvalidLatitudeOrLongitude(AdditionalInputMixin):
    msg = "Некорректные координаты"


class NoLatitudeCharError(AdditionalInputMixin):
    msg = "Некорректная широта"


class NoLongitudeIndexError(AdditionalInputMixin):
    msg = "Некорректная долгота"


class InvalidNomenclatureTitleError(AdditionalInputMixin):
    msg = "Некорректная номенклатура"
