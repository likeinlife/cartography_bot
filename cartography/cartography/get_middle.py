from decimal import Decimal

from ..utils.classes import Degrees


def get_middle(first: Degrees, second: Degrees, number_of_parts: int):
    delta = (second - first) / number_of_parts
    text = ""
    for i in range(number_of_parts + 1):
        text += str(delta * i + first) + "\n"
    return text


def get_middle_list(first: Degrees, second: Degrees, number_of_parts: int):
    delta = (second - first) / number_of_parts
    text = []
    for i in range(number_of_parts + 1):
        text.append(str(delta * i + first))
    return text


if __name__ == "__main__":
    first = Degrees(*list(map(Decimal, input("first >> ").split(" "))))
    second = Degrees(*list(map(Decimal, input("second >> ").split(" "))))
    delta = int(input("Parts >> "))
    get_middle(first, second, delta)
