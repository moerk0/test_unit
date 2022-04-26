import logging as log
from random import randint
from excelHandler import Excel
from test_data import ReturnCode, TestData


class Encoder:
    def __init__(self, d: "list[TestData]", lang) -> None:
        self.d = d
        self.lang = str(lang)
        self.filename = f"./data/braille_{self.create_suffix(False)}.h"

    def sort_data(self) -> None:
        self.d.sort(key=lambda x: getattr(x, "num"))

    def create_suffix(self, up: bool) -> str:
        special_char_map = {ord("ä"): "a", ord("ü"): "u", ord("ö"): "o"}
        suffix = (
            self.lang[0:3].replace("-", "").translate(special_char_map).replace("/", "")
        )
        if up:
            return suffix.upper()
        else:
            return suffix.lower()

    def header(self) -> str:
        s = "\n"

        ifguard = (
            f"#ifndef __BRAILLE_{self.create_suffix(True)}_H__",
            f"#define __BRAILLE_{self.create_suffix(True)}_H__",
            2 * "\n",
        )

        include = (
            "#include <stdint.h>",
            '#include "keylayouts.h"',
            2 * "\n",
        )

        declaration = (
            "// Erich Schmids 8 Keys Braille",
            "const static uint8_t chord_id_keycode_"
            + self.create_suffix(False)
            + "[256][4] = {",
            "\t//            {char, char_modifier, deadkey, deadkey_modifier}",
        )
        head = ifguard + include + declaration
        return s.join(head)

    @staticmethod
    def convert_key(arg, deadkey: bool):
        if arg == None:
            return 0
        elif arg == "GRAVE" or arg == "SCANCODE_GRAVE":
            return "SCANCODE_GRAVE"

        elif deadkey and "DEADKEY_" not in arg:
            return "DEADKEY_" + arg

        elif "KEY_" not in arg:
            return "KEY_" + arg

        else:
            return arg

    @staticmethod
    def convert_modifier(arg):
        if arg == None:
            return 0
        elif "MODIFIERKEY_" not in arg:
            return "MODIFIERKEY_" + arg
        else:
            return arg

    @staticmethod
    def tab_handler(len) -> str:
        max_space = 72
        space = max_space - len
        return space * " "

    @staticmethod
    def data_is_shitty(l: list) -> bool:
        for i in l:
            if i >= ReturnCode.YELLOW:
                return True
        return False

    @staticmethod
    def num(num) -> str:
        s = f"\t/* {num}  */"
        return s

    def array(self, key, mod, dead, dmod) -> str:
        s = f"{self.convert_key(key,False)}, {self.convert_modifier(mod)}, {self.convert_key(dead,True)}, {self.convert_modifier(dmod)}"
        return "{" + s + "},"

    @staticmethod
    def braille_cha(brai, cha) -> str:
        s = f"/* '{cha}' dots-{brai} */"
        return s

    @staticmethod
    def null_line(num) -> str:
        s = f"\t/* {num}  */\t" + "{0, 0, 0, 0}," + 59 * " " + "// 0"
        return s

    @staticmethod
    def end_of_file() -> str:
        s = "};" + 2 * "\n" + "#endif"
        return s

    def run(self):
        self.sort_data()

        with open(self.filename, "w") as file:  # a = append, w = (over)write
            print(self.header(), file=file)
            idx = 0
            cnt = 0
            prev_num = -1
            while idx < len(self.d):
                data = self.d[idx]
                if prev_num == data.num or cnt > data.num:
                    log.error(
                        f"{prev_num} exists twice !!!! Not good. You almost buffer overflowed"
                    )
                    break

                elif self.data_is_shitty(
                    [data.color_key, data.color_mod, data.color_ded, data.color_dmo]
                ):
                    print(self.null_line(cnt), file=file)
                    idx += 1

                elif cnt == data.num:
                    print(self.num(data.num), file=file, end="\t")
                    arr = self.array(data.key, data.mod, data.dead, data.dmod)
                    print(arr, file=file, end=self.tab_handler(len(arr)))
                    print(self.braille_cha(data.brai, data.cha), file=file)
                    prev_num = data.num
                    idx += 1
                else:
                    print(self.null_line(cnt), file=file)

                cnt += 1

            print(self.end_of_file(), file=file)

            log.info(f"{cnt} Rows encoded")


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
# dat = [TestData(0, i, randint(100, 200000), n, n, n, n, n, n) for i, n in enumerate(l)]
# for data in dat:
#     data.validate_all()

# encoder = Encoder(dat, "us-englisch")


# encoder.sort_data()
# encoder.run()
# print(encoder.create_suffix(True))
# print(encoder.array("A", "SHIFT", "CIRCUMFLEX", "MODIFIERKEY_ACCUTE"))

# print(encoder.data_is_shitty([ReturnCode.GREEN, ReturnCode.GREEN, ReturnCode.BLANK]))
