import re

re_string = re.compile(
    r'(?P<one_mil>[A-Z])-(?P<one_mil2>[0-9]{1,3})-?(?P<one_100>[0-9]{1,3})?(-\()?(?P<one_5>[0-9]{1,3})?\)?-?(?P<one_2>[а-и])?\)?-?(?P<one_50>[А-Г])?-?(?P<one_25>[а-г])?-?(?P<one_10>[1-4])?'
)
