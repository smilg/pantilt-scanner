from SerialDevice import SerialDevice

dev = SerialDevice()
busy = False

while True:
    while dev.ser.in_waiting:
        line = dev.read()
        if 'ready' in line:
            busy = False
        if len(line) > 0:
            print(line, end='')
    if not dev.ser.out_waiting and not busy:
        cmd = input('enter command: ')
        if cmd != '':
            dev.write(cmd)
            busy = True
