#with serial.Serial('/dev/tty0', 115200, timeout=1) as ser:
import serial

ser = serial.Serial()
ser.baudrate = 19200
ser.port = 'COM1'
print(ser)
ser.open()
ser.is_open
ser.close()
ser.is_open