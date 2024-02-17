class BaseError(Exception):
    """Base error."""


class BaseMsgError(BaseError):
    msg: str
