from serial import Serial
import time

class SerialCom(Serial):
    def __init__(self, port, baudrate) -> None:
        super().__init__(port, baudrate=baudrate ,timeout=.1)
        self.recievedChar = b''

    def writeNum(self, num): # Arduino Code expects CRLF in order to return. There are better ways
        num = str(num)
        self.write(bytes(num + '\r\n', 'utf-8'))

    def readChar(self):
        c = self.readline()
        #print(f" recieved Char : {c.decode('UTF-8')}")
        return c.decode('UTF-8')



arduino = SerialCom('/dev/ttyUSB0',115200)
time.sleep(2)
arduino.num = '12' # Taking input from user
arduino.writeNum(995)
time.sleep(0.05)
arduino.readChar()



