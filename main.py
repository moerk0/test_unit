from threading import Thread

from encoder import Encoder
from excelHandler import Excel
from GUI import Gooey
from serialHandler import SerialCom
from test_data import OutLevel, ReturnCode, TestData, log
from test_unit import TestUnit


class Validator(Thread):
    def __init__(self, d: "list[TestData]", x: Excel) -> None:
        super().__init__()
        self.d = d
        self.x = x
        self.all_nums = []

    def run(self):
        for data in self.d:
            if (tmp := data.validate_num(self.all_nums)) != None:
                self.all_nums.append(tmp)

            data.validate_all()  # validate all heißt in diesem Fall all außer num -.-
        self.all_nums = []
        self.save()

    def save(self):
        self.x.writeData(self.d)
        self.x.saveResultFile()


class Encoderer(Thread):
    def __init__(self, e: Encoder) -> None:
        super().__init__()
        self.d = d
        self.e = e

    def run(self) -> None:
        self.e.run()


def prepare():

    # It is working but: veeeeeeeeery sketchy!
    gu.delay(5)
    gu.clear_input()
    gu.window.update()

    if tu.running is True:
        gu.button_handler(gu.button_3, "abort", aborted)

        #

        if tu.count_idx() is True:  #
            states["send"]()  # Little Nest
        else:  #
            states["finished"]()  #

    else:
        gu.button_handler(gu.button_3, "send", send)


def send():

    # Set true after the button is pushed
    if tu.running is not True:
        tu.running = True

    # ardu.writeNum(tu.getNextNum())

    log.info(f"State: send: {tu.getNextNum()}")
    # tu.setChar(ardu.readChar())                # use ardu.readchar to read from serial Monitor.

    # as long as no char is recieved and max tries not exceeded the code wil loop
    max_tries = 100
    tries = 0
    while gu.getInputChar() is None:
        gu.window.update()
        gu.delay(10)  # Wait 10ms
        tries += 1
        if tries >= max_tries:
            break

    tu.setChar(
        gu.getInputChar()
    )  # whatever you type in the input bar will be passed for test. it will only accept single chars

    states["test"]()


def test():
    tu.compare()
    print(tu.testdata[tu.idx].content(OutLevel.TEST))

    states["prepare"]()


def aborted():
    gu.output_box_2.config(text="test suspended, Continue?")
    tu.running = False
    gu.window.update()
    states["prepare"]()


def finished():
    gu.output_box_1.config(text="fini, save?")
    gu.output_box_2.config(text=f"saving output to:{ex.outFile}")
    tu.running = False
    gu.button_handler(gu.button_3, "save", ex.saveResultFile)

    ex.writeResults(tu.getResults())


states = {
    "init": True,
    "prepare": prepare,
    "send": send,
    "test": test,
    "aborted": aborted,
    "finished": finished,
    "error": "unexpected error occured",
}


if __name__ == "__main__":

    gu = Gooey()

    try:
        ex = Excel(
            "us-englisch", "./data/sprachtabelle2.xlsx"
        )  # adjust path and Language
        d = ex.getTestData()
        tu = TestUnit(d)
        enc = Encoder(d, ex.lang)
        gu.output_box_2.config(
            text=f"selected lang:{ex.lang}, fetched {len(tu.testdata)} entries"
        )
    except:
        gu.output_box_2.config(text="could not open, bad path?")
        states["init"] = False

    # try:
    #     ardu = SerialCom('/dev/ttyUSB0', 115200)
    #     gu.output_box_1.config(text=f"Port: {ardu.port} openend")
    # except:
    #     gu.output_box_1.config(text="bad port, please restart")
    #     states['init'] = False

    ##

    if states["init"] is True:
        states["prepare"]()
        gu.button_handler(gu.button_1, "Validata", Validator(d, ex).run)
        gu.button_handler(gu.button_2, "Encode", enc.run)

    gu.runLoop()
