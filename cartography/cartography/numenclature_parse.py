import re
from .find_geographcoord import *


class NumenclatureParser:

    def __init__(self, numenclature: str) -> None:
        self.numenclature = numenclature

    def get_parts(self):
        if re_match := re.fullmatch(r'(?P<m1>[A-Z]-[0-9]{1,2})', self.numenclature):  # 1m
            return FindNumenclat_1M(re_match.groupdict())
        elif re_match := re.fullmatch(r'(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k500>[А-Г])', self.numenclature):  # 500k
            return FindNumenclat_500k(re_match.groupdict())
        elif re_match := re.fullmatch(r'(?P<k300>[IVX]{1,4})-(?P<m1>[A-Z]-[0-9]{1,2})', self.numenclature):  # 300k
            return FindNumenclat_300k(re_match.groupdict())
        elif re_match := re.fullmatch(r'(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k200>[IVX]{1,6})', self.numenclature):  # 200k
            return FindNumenclat_200k(re_match.groupdict())
        elif re_match := re.fullmatch(r'(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})', self.numenclature):  # 100k
            return FindNumenclat_100k(re_match.groupdict())
        elif re_match := re.fullmatch(r'(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-(?P<k50>[А-Г])',
                                      self.numenclature):  # 50k
            return FindNumenclat_50k(re_match.groupdict())
        elif re_match := re.fullmatch(r'(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-(?P<k50>[А-Г])-(?P<k25>[а-г])',
                                      self.numenclature):  # 25k
            return FindNumenclat_25k(re_match.groupdict())
        elif re_match := re.fullmatch(
                r'(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-(?P<k50>[А-Г])-(?P<k25>[а-г])-(?P<k10>[0-4])',
                self.numenclature):  # 10k
            return FindNumenclat_10k(re_match.groupdict())
        elif re_match := re.fullmatch(r'(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-\((?P<k5>[0-9]{1,3})\)',
                                      self.numenclature):  # 5k
            return FindNumenclat_5k(re_match.groupdict())
        elif re_match := re.fullmatch(
                r'(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-\((?P<k5>[0-9]{1,3})-(?P<k2>[а-и])\)',
                self.numenclature):  # 2k
            return FindNumenclat_2k(re_match.groupdict())


# U-32
# U-32-А
# I-N-37
# N-37-XXI
# N-37-39

# N-37-39-Г
# N-37-39-Г-г
# N-37-39-Г-г-4

# N-37-144-(120)
# N-37-144-(120-и)