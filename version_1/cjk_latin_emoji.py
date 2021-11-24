import re
import string

RE_SEPARATORS = re.compile(r"[:?！？，。“”【】\"：…\n、（）～；•《》—「」·~]")

_LETTER_DIGITS = set(string.digits + string.ascii_letters)


def is_cjk(c: str) -> bool:
    return 0x4E00 <= ord(c) <= 0x9FFF


def is_letter_digit(c: str) -> bool:
    return c in _LETTER_DIGITS

