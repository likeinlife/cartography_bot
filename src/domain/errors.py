class BaseError(Exception):
    @property
    def msg(self) -> str:
        return "Base error"

    def __str__(self) -> str:
        return self.msg
