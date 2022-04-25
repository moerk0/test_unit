from dataclasses import dataclass
import logging as log
from enum import IntEnum, Enum, auto

log.basicConfig(level=log.INFO, format="%(levelname)s:%(message)s")


class ReturnCode(IntEnum):
    """ "These Codes color the output file and determine if the giben data is faulty"""

    BLANK = 0
    GREEN = 1
    YELLOW = 2
    RED = 3


class OutLevel(Enum):
    INITIAL = auto()
    TEST = auto()


class DataIndex(Enum):
    ROW = auto()
    NUM = auto()
    BRAI = auto()

    CHA = auto()
    KEY = auto()
    MOD = auto()
    DEAD = auto()
    DMOD = auto()

    REC = auto()
    PASSED = auto()


all_nums = []  # validator occupys global namespace here


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
    brai: str
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

    def checkASCII(self, arg, var_name) -> ReturnCode:
        if str(arg).isascii():
            code = ReturnCode.BLANK
        else:
            log.warning(f"\tRow: {self.row} - {var_name} >> {arg} << is not ASCII")
            code = ReturnCode.YELLOW
        return code

    def checkCase(self, arg, var_name) -> "tuple[str, ReturnCode]":
        if str(arg).isupper() == False:
            arg = arg.upper()
            log.info(
                f"\tRow: {self.row} - {var_name} >> {arg} << is not upper. Corrected"
            )
            code = ReturnCode.GREEN
        else:
            code = ReturnCode.BLANK
        return arg, code

    def checkSpace(self, arg, var_name) -> "tuple[str, ReturnCode]":
        if " " in arg:
            arg = arg.strip()
            log.info(
                f"\tRow: {self.row} - {var_name} >> {arg} << unexpected Space character. Corrected"
            )
            code = ReturnCode.GREEN
        else:
            code = ReturnCode.BLANK
        return arg, code

    def checkList(self, arg: str, l, var_name: str) -> "tuple[str,ReturnCode]":

        if arg in l:
            return arg, ReturnCode.BLANK

        else:
            if arg.replace(" ", "_") in l:
                arg = arg.replace(" ", "_")
                log.info(
                    f"\tRow: {self.row} - {var_name} >> {arg} << had no underscore"
                )
                return arg, ReturnCode.GREEN
            else:
                log.warning(
                    f"Row: {self.row} - {var_name} >> {arg} << is not in Key list"
                )
                return arg, ReturnCode.YELLOW

    def validate_num(self):
        if self.num in all_nums:
            log.error(f"\tRow: {self.row} - Num >> {self.num} << Duplicate Entry!")
            self.color_num = ReturnCode.RED
        else:
            all_nums.append(self.num)

    def validate_cha(self):
        if self.cha is None:
            log.warning(f"Row: {self.row} - Cha is None")
            self.color_cha = ReturnCode.YELLOW

        elif str(self.cha).isspace() == True:  # if it is escaped char
            pass

        else:
            self.cha = str(self.cha)
            len_cha = len(self.cha)

            if len_cha > 1:
                self.cha = self.cha.strip()

                try:
                    ord(self.cha)
                    log.info(
                        f"\tRow: {self.row} - Cha >> {self.cha} << had a space character. Removed"
                    )
                    self.color_cha = ReturnCode.GREEN
                    self.cha = self.cha.strip()
                except:
                    log.error(
                        f"\tRow: {self.row} - Cha >> {self.cha} << is not a single character!"
                    )
                    self.color_cha = ReturnCode.RED
            else:
                pass

    def validate_key(self):
        key_names = [
            "SPACE",
            "TAB",
            "ENTER",
            "PLUS",
            "MINUS",
            "QUOTE",
            "PERIOD",
            "SEMICOLON",
            "EQUAL",
            "SLASH",
            "LEFT_BRACE",
            "RIGHT_BRACE",
            "GRAVE",
            "NON_US_BS",
            "BACKSLASH",
            "COMMA",
            "SCANCODE_GRAVE",
        ]

        if self.key is None:
            log.warning(f"Row: {self.row} - Key is None")
            self.color_key = ReturnCode.YELLOW

            # Key is not a int Number
        else:
            self.key = str(self.key).strip()
            ret = self.checkSpace(self.key, "key")
            self.key = ret[0]
            self.color_key = ret[1]

            if self.key.isalpha() and len(self.key) <= 1:
                ret = self.checkASCII(self.key, "key")
                if self.color_key < ret:
                    self.color_key = ret

                ret = self.checkSpace(self.key, "key")
                self.key = ret[0]
                if self.color_key < ret[1]:
                    self.color_key = ret[1]

            elif self.key.isdigit():
                pass
            else:
                ret = self.checkList(self.key, key_names, "key")
                self.key = ret[0]
                if self.color_key < ret[1]:
                    self.color_key = ret[1]

    def validate_mod(self):
        modifier = ["SHIFT", "RIGHT_ALT", "LEFT_ALT", "CTRL"]

        if self.mod is not None:
            ret = self.checkCase(self.mod, "Mod")
            self.mod = ret[0]
            self.color_mod = ret[1]

            ret = self.checkSpace(self.mod, "Mod")
            self.mod = ret[0]
            if ret[1] >= self.color_mod:
                self.color_mod = ret[1]

            ret = self.checkList(self.mod, modifier, "Mod")
            self.mod = ret[0]
            if ret[1] >= self.color_mod:
                self.color_mod = ret[1]

    def validate_dmod(self):
        modifier = ["SHIFT", "RIGHT_ALT", "LEFT_ALT", "CTRL"]

        if self.dmod is not None:
            ret = self.checkCase(self.dmod, "dmod")
            self.dmod = ret[0]
            self.color_dmo = ret[1]

            ret = self.checkSpace(self.dmod, "dmod")
            self.dmod = ret[0]
            if ret[1] >= self.color_dmo:
                self.color_dmo = ret[1]

            if self.dmod not in modifier:

                if self.dmod in modifier:
                    log.info(
                        f"\tRow: {self.row} - Mod >> {self.dmod} << had no underscore. Corrected"
                    )
                    self.color_dmod = ReturnCode.GREEN
                else:
                    log.warning(
                        f"Row: {self.row} - Mod >> {self.dmod} << is unkonwn modifier"
                    )
                    self.color_dmo = ReturnCode.YELLOW

    #    ret =  self.checkCase(self.dmod)
    #         self.mod =       ret[0]
    #         self.color_mod = ret[1]

    def validate_all(self):
        l = [
            self.validate_num,
            self.validate_cha,
            self.validate_key,
            self.validate_mod,
            self.validate_dmod,
        ]
        for call_func in l:
            call_func()

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


# d = TestData(1,1,1,'\r ','A','SHIFT',None,None)
# d.validate_all()
# print(len('\x20'))
# if '\x20' == ' ':
#     print('jo')
