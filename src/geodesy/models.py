from __future__ import annotations

import textwrap

from pydantic import BaseModel


class MicrometerInput(BaseModel):
    left_circle: float
    right_circle: float

    @classmethod
    def from_str(cls, value: str) -> MicrometerInput:
        left_circle, right_circle = map(float, value.split(" "))
        return cls(left_circle=left_circle, right_circle=right_circle)


class MicrometerOutput(BaseModel):
    average_first: float
    average_second: float
    c_2: float
    average: float

    def to_str(self) -> str:
        return textwrap.dedent(
            f"""
            Среднее из КП и КЛ 1 отчета: {self.average_first:.2f}
            Среднее из КП и КЛ 2 отчета: {self.average_second:.2f}
            Коллимационная ошибка: {self.c_2:.2f}
            Среднее: {self.average:.2f}
            """
        )
