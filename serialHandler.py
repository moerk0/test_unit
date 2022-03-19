with serial.Serial('/dev/tty0', 115200, timeout=1) as ser:
    ser.is_open()