import logging as log
from abc import ABC, abstractmethod
from ast import Return
from dataclasses import dataclass, field
from enum import Enum, IntEnum, auto
from typing import List, Optional

log.basicConfig(level=log.INFO, format="%(levelname)s:%(message)s")


class ReturnCode(IntEnum):
    """ "These Codes color the output file and determine if the giben data is faulty"""

    BLANK = 0
    GREEN = 1
    YELLOW = 2
    RED = 3


class ValidatorErrors(ABC):
    def __init__(self, row: int, var_name: str, arg, msg: str, errtype: ReturnCode):
        self.errtype = errtype
        if errtype == ReturnCode.YELLOW:
            log.warning(f"Validator: Row: {row} - {var_name} >> {arg} << {msg}")
        elif errtype == ReturnCode.GREEN:
            log.info(f"Row: {row} - {var_name} >> {arg} << {msg}")
        elif errtype == ReturnCode.RED:
            log.error(f"Row: {row} - {var_name} >> {arg} << {msg}")

    def return_error_code(self) -> ReturnCode:
        return self.errtype


class ASCIIError(ValidatorErrors):
    def __init__(self, row, var_name, arg):
        super().__init__(row, var_name, arg, " is not Ascii", ReturnCode.YELLOW)

    def return_error_code(self) -> ReturnCode:
        return super().return_error_code()


class SpaceError(ValidatorErrors):
    def __init__(self, row, var_name, arg):
        super().__init__(
            row, var_name, arg, "had a space character. Removed", ReturnCode.GREEN
        )

    def return_error_code(self) -> ReturnCode:
        return super().return_error_code()


class CaseError(ValidatorErrors):
    def __init__(self, row, var_name, arg):
        super().__init__(row, var_name, arg, "was not upper", ReturnCode.GREEN)

    def return_error_code(self):
        return super().return_error_code()


class ListError(ValidatorErrors):
    def __init__(self, row, var_name, arg):
        super().__init__(row, var_name, arg, " not in The list", ReturnCode.YELLOW)

    def return_error_code(self):
        return super().return_error_code()


class NumError(ValidatorErrors):
    def __init__(self, row, var_name, arg):
        super().__init__(row, var_name, arg, " is Integer Type", ReturnCode.YELLOW)

    def return_error_code(self):
        return super().return_error_code()


class EntryError(ValidatorErrors):
    def __init__(self, row, var_name, arg):
        super().__init__(row, var_name, arg, "Entry exists twice", ReturnCode.RED)

    def return_error_code(self) -> ReturnCode:
        return super().return_error_code()


class TooLongError(ValidatorErrors):
    def __init__(self, row, var_name, arg):
        super().__init__(row, var_name, arg, "is too long", ReturnCode.YELLOW)

    def return_error_code(self) -> ReturnCode:
        return super().return_error_code()


class UnderscoreError(ValidatorErrors):
    def __init__(self, row, var_name, arg):
        super().__init__(row, var_name, arg, "had no underscore", ReturnCode.GREEN)

    def return_error_code(self) -> ReturnCode:
        return super().return_error_code()


class MappedKeyError(ValidatorErrors):
    def __init__(self, row, var_name, arg):
        super().__init__(
            row,
            var_name,
            arg,
            " was found in the mapping and changed",
            ReturnCode.GREEN,
        )

    def return_error_code(self):
        return super().return_error_code()


class NoneError(ValidatorErrors):
    def __init__(self, row, var_name, arg):
        super().__init__(row, var_name, arg, " is none Type", ReturnCode.YELLOW)

    def return_error_code(self):
        return super().return_error_code()


class UnkownError(ValidatorErrors):
    def __init__(self, row, var_name, arg):
        super().__init__(
            row, var_name, arg, " Unkown Exception, call the programmer", ReturnCode.RED
        )

    def return_error_code(self):
        return super().return_error_code()


class OutLevel(Enum):
    INITIAL = auto()
    TEST = auto()
    COLOR_CODES = auto()
    VALUE_CODE_PAIR = auto()


# all_nums = []


@dataclass
class TestData:
    """
    Each one object holds one Row of ExcelTable and it holds the Color coding of the result file
    Initially TestData requires 4 Inputs:
    The Bin Num to send, The expected Char, The name of the key and The modifier Key.

    Recieved and Passed are Values that the Test_unit Program fills. They are not mandatory for the Encoder,
    but it is nice to keep them, so a future fusion is possible.

    The Color variables indicate where Data has to be rechecked. They are handled by the validate() Function
    Green means that there was a mistake, that the programm corrected.
    OR
    The Test is passed

    Yellow means there was a mistake that influences the Output of the .h -File
    OR
    for the received Column it means that no data arrieved( receivied = None) during runtime of the test

    Red means Either the Char column or the Int column are Faulty
    OR
    For the passed Column it means that the expected char and the recieved Char are not equal.

    """

    row: int

    num: int
    brai: int
    cha: str

    key: str
    mod: str

    dead: str
    dmod: str

    received = None
    passed: bool = False

    # Color Codes: 0 = No Color, 1 = Green, 2 = Yellow, 3 = Red
    color_num: ReturnCode = ReturnCode.BLANK
    color_cha: ReturnCode = ReturnCode.BLANK
    color_key: ReturnCode = ReturnCode.BLANK
    color_mod: ReturnCode = ReturnCode.BLANK
    color_ded: ReturnCode = ReturnCode.BLANK
    color_dmo: ReturnCode = ReturnCode.BLANK
    color_rec: ReturnCode = ReturnCode.BLANK
    color_pas: ReturnCode = ReturnCode.RED

    def validate_num(self, all_nums: list) -> Optional[int]:
        if not isinstance(self.num, int):
            self.color_num = NumError(self.row, "Num", self.num).return_error_code()
        elif self.num in all_nums:
            self.color_num = EntryError(self.row, "Num", self.num).return_error_code()
        else:
            return self.num

    def validate_cha(self):
        if self.cha is None:
            self.color_cha = NoneError(self.row, "Char", self.cha).return_error_code()

        elif isinstance(self.cha, int):
            pass

        elif len(self.cha) <= 1:
            pass

        elif len(self.cha.strip()) > 1:
            self.color_cha = TooLongError(
                self.row, "Char", self.cha
            ).return_error_code()

        elif " " in self.cha:
            self.cha = self.cha.strip()
            self.color_cha = SpaceError(self.row, "Char", self.cha).return_error_code()

        else:
            self.color_cha = UnkownError(self.row, "Char", self.cha).return_error_code()

    def validate_key(self):
        key_non_mapped_names = [
            "SPACE",
            "TAB",
            "ENTER",
            "GRAVE",
            "BACKSLASH",
            "SCANCODE_GRAVE",
            "BACKSPACE",
            "LEFT",
            "RIGHT",
        ]
        key_mapped_names = {
            "-": "MINUS",
            ",": "COMMA",
            "<": "NON_US_BS",
            "[": "RIGHT_BRACE",
            "]": "LEFT_BRACE",
            '"': "QUOTE",
            "=": "EQUAL",
            "/": "SLASH",
            ".": "PERIOD",
            ";": "SEMICOLON",
            "\\": "BACKSALSH",
        }

        if self.key is None:
            self.color_key = NoneError(self.row, "Key", self.key).return_error_code()

        elif isinstance(self.key, int):
            self.key = str(self.key)

        else:

            if " " in self.key:
                self.key = self.key.strip()
                self.color_key = SpaceError(
                    self.row, "key", self.key
                ).return_error_code()

            if " " in self.key:
                self.key = self.key.replace(" ", "_")
                self.color_key = UnderscoreError(
                    self.row, "key", self.key
                ).return_error_code()

            if self.key.isidentifier() or self.key.isdigit():
                if self.key.isdigit():
                    pass

                elif self.key.isascii() == False:
                    self.color_key = ASCIIError(
                        self.row, "key", self.key
                    ).return_error_code()

                elif self.key.isupper() == False:
                    self.key = self.key.upper()
                    self.color_key = CaseError(
                        self.row, "key", self.key
                    ).return_error_code()

                if (
                    len(self.key) > 1
                    and self.key not in key_non_mapped_names
                    and self.key not in key_mapped_names.values()
                ):
                    self.color_key = ListError(
                        self.row, "key", self.key
                    ).return_error_code()

            elif self.key in key_mapped_names.keys():
                self.key = key_mapped_names[self.key]
                self.color_key = MappedKeyError(
                    self.row, "key", self.key
                ).return_error_code()

            else:
                self.color_key = UnkownError(
                    self.row, "Key", self.key
                ).return_error_code()

    @staticmethod
    def validate_mods_n_deads(
        var_name: str, row: int, arg: str
    ) -> "Optional[tuple[str, ReturnCode]]":
        color_code: ReturnCode = ReturnCode.BLANK
        modifier = ["SHIFT", "RIGHT_ALT", "LEFT_ALT", "CTRL", "GUI"]
        deadkeys = [
            "CIRCUMFLEX",
            "ACUTE_ACCENT",
            "GRAVE",
            "SCANCODE_GRAVE",
            "DEADKEY_CIRCUMFLEX",
        ]

        if arg is not None:
            if isinstance(arg, int):
                color_code = NumError(row, var_name, arg).return_error_code()
            else:
                if arg.isupper() == False:
                    arg = arg.upper()
                    color_code = CaseError(row, var_name, arg).return_error_code()

                if " " in arg:
                    arg = arg.strip()
                    color_code = SpaceError(row, var_name, arg).return_error_code()

                if " " in arg:
                    arg = arg.replace(" ", "_")
                    color_code = UnderscoreError(row, var_name, arg).return_error_code()

                if (
                    arg in modifier
                    and var_name.lower() == "mod"
                    or arg in modifier
                    and var_name.lower() == "dmod"
                ):
                    pass

                elif arg in deadkeys and var_name.lower() == "dead":
                    pass

                else:
                    color_code = ListError(row, var_name, arg).return_error_code()

            return arg, color_code

    def validate_all(self):

        self.validate_cha()
        self.validate_key()

        if (ret := self.validate_mods_n_deads("mod", self.row, self.mod)) != None:
            self.mod = ret[0]
            self.color_mod = ret[1]

        if (ret := self.validate_mods_n_deads("dead", self.row, self.dead)) != None:
            self.dead = ret[0]
            self.color_ded = ret[1]

        if (ret := self.validate_mods_n_deads("dmod", self.row, self.dmod)) != None:
            self.dmod = ret[0]
            self.color_dmo = ret[1]

    def content(self, level: OutLevel):

        if level == OutLevel.INITIAL:
            return {
                "Row": self.row,
                "Num": self.num,
                "Braille": self.brai,
                "Cha": self.cha,
                "Key": self.key,
                "Mod": self.mod,
                "Dead": self.dead,
                "Dmod": self.dmod,
            }

        elif level == OutLevel.TEST:
            return {
                "Num": self.num,
                "cha": self.cha,
                "received": self.received,
                "passed": self.passed,
            }
        elif level == OutLevel.COLOR_CODES:
            return {
                "Num": self.color_num.name,
                "Cha": self.color_cha.name,
                "Key": self.color_key.name,
                "Mod": self.color_mod.name,
                "Dead": self.color_ded.name,
                "Dmod": self.color_dmo.name,
            }
        elif level == OutLevel.VALUE_CODE_PAIR:
            return {
                self.num: self.color_num.name,
                self.cha: self.color_cha.name,
                self.key: self.color_key.name,
                self.mod: self.color_mod.name,
                self.dead: self.color_ded.name,
                self.dmod: self.color_dmo.name,
            }


# l = [
#     "ä",
#     ".",
#     "SCANCODE_grave",
#     "shift",
#     "irg endwas",
#     "nonusbs",
#     "A",
#     1,
#     "?",
#     "klammer",
#     ") ",
#     "DEADKEY_CIRCUMFLEX",
# ]
# d: "list[TestData]" = []
# for i in l:
#     d.append(TestData(1, 1, 1, i, i, i, i, i, i))

# for i in d:
#     i.validate_all()
# for i in d:
#     print(i.content(OutLevel.COLOR_CODES))

# print(len('\x20'))
# if '\x20' == ' ':
#     print('jo')
