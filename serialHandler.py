import serial


ser = serial.Serial()

ser.baudrate = 115200
ser.port = '/dev/ttyACM0'
ser.open()
print(ser.is_open)