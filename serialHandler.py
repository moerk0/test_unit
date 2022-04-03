from serial import Serial

class SerialCom(Serial):
    def __init__(self, port, baudrate) -> None:
        super().__init__(port, baudrate=baudrate ,timeout=.1)
        self.num = None
        self.recievedChar = b''

    def writeNum(self): # Arduino Code expects CRLF in order to return. There are better ways
        self.write(bytes(self.num + '\r\n', 'utf-8'))

    def readChar(self):
        self.recievedChar = self.readline()
        print(f" recieved Char : {self.recievedChar.decode('UTF-8')}")



# arduino = SerialCom('/dev/ttyUSB0',115200)
# time.sleep(2)
# arduino.num = '12' # Taking input from user
# arduino.writeNum()
# time.sleep(0.05)
# arduino.readChar()



