import re

from .find_geographcoord import (
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

patterns = {
    "1m": r"(?P<m1>[A-Z]-[0-9]{1,2})",
    "500k": r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k500>[А-Г])",
    "300k": r"(?P<k300>[IVX]{1,4})-(?P<m1>[A-Z]-[0-9]{1,2})",
    "200k": r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k200>[IVX]{1,6})",
    "100k": r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})",
    "50k": r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-(?P<k50>[А-Г])",
    "25k": r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-(?P<k50>[А-Г])-(?P<k25>[а-г])",
    "10k": r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-(?P<k50>[А-Г])-(?P<k25>[а-г])-(?P<k10>[0-4])",
    "5k": r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-\((?P<k5>[0-9]{1,3})\)",
    "2k": r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-\((?P<k5>[0-9]{1,3})-(?P<k2>[а-и])\)",
}


def parse_nomenclature_string(nomenclature_string: str) -> AbstractFindNumenclature:
    """
    Parse nomenclature string.

    Examples
    --------
    - U-32
    - U-32-А
    - I-N-37
    - N-37-XXI
    - N-37-39
    - N-37-39-Г
    - N-37-39-Г-г
    - N-37-39-Г-г-4
    - N-37-144-(120)
    - N-37-144-(120-и)
    """
    if re_match := re.fullmatch(patterns["1m"], nomenclature_string):
        return FindNumenclat_1M(re_match.groupdict())
    elif re_match := re.fullmatch(patterns["500k"], nomenclature_string):  # 500k
        return FindNumenclat_500k(re_match.groupdict())
    elif re_match := re.fullmatch(patterns["300k"], nomenclature_string):  # 300k
        return FindNumenclat_300k(re_match.groupdict())
    elif re_match := re.fullmatch(patterns["200k"], nomenclature_string):  # 200k
        return FindNumenclat_200k(re_match.groupdict())
    elif re_match := re.fullmatch(patterns["100k"], nomenclature_string):  # 100k
        return FindNumenclat_100k(re_match.groupdict())
    elif re_match := re.fullmatch(patterns["50k"], nomenclature_string):
        return FindNumenclat_50k(re_match.groupdict())
    elif re_match := re.fullmatch(patterns["25k"], nomenclature_string):
        return FindNumenclat_25k(re_match.groupdict())
    elif re_match := re.fullmatch(patterns["10k"], nomenclature_string):
        return FindNumenclat_10k(re_match.groupdict())
    elif re_match := re.fullmatch(patterns["5k"], nomenclature_string):
        return FindNumenclat_5k(re_match.groupdict())
    elif re_match := re.fullmatch(patterns["2k"], nomenclature_string):
        return FindNumenclat_2k(re_match.groupdict())
    else:
        return None
