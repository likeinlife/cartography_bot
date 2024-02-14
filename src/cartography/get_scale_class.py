from .find_numenclature import (
    AbstractFindNumenclature,
    FindNumenclat_1M,
    FindNumenclat_2k,
    FindNumenclat_5k,
    FindNumenclat_10k,
    FindNumenclat_25k,
    FindNumenclat_50k,
    FindNumenclat_100k,
    FindNumenclat_200k,
    FindNumenclat_300k,
    FindNumenclat_500k,
)

table = {
    1: FindNumenclat_1M,
    2: FindNumenclat_500k,
    3: FindNumenclat_300k,
    4: FindNumenclat_200k,
    5: FindNumenclat_100k,
    6: FindNumenclat_50k,
    7: FindNumenclat_25k,
    8: FindNumenclat_10k,
    9: FindNumenclat_5k,
    10: FindNumenclat_2k,
}


def get_scale(number: int) -> type[AbstractFindNumenclature]:
    return table[number]
