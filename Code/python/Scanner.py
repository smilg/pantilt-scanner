from SerialDevice import SerialDevice

class Scanner:
    def __init__(self, max_angle=170) -> None:
        self.dev = SerialDevice()
        self._ready = False
        self.max_angle = max_angle
        self.pan_angle = None
        self.tilt_angle = None
        self.center()

    @property
    def ready(self) -> bool:
        return self._ready
    
    def _read_until_ready(self) -> list:
        '''
        Reads data from the scanner until it is ready for a new instruction. Any data read is
        returned as a list of lines.

        Returns:
            list: the lines of data received before 'ready'
        '''
        data = []
        # loop if not ready or data waiting in input buffer
        while not self._ready or self.dev.ser.in_waiting:
            # read data from the input buffer, add it to the list if it isn't 'ready'
            line = self.dev.read()
            if line.strip() == 'ready':
                self._ready = True
            # don't add empty strings to the list
            elif line.strip() != '':
                data.append(line)
        return data

    def pan(self, angle: int) -> None:
        '''
        Instructs the scanner to pan to an angle, then waits for a ready signal.

        Args:
            angle (int): the angle to pan to.
        '''
        # don't send a command if the angle is invalid
        if angle >= 0 and angle <= self.max_angle:
            self.dev.write("PAN|{}".format(angle))
            self._ready = False
            self.pan_angle = angle      # keep track of the new angle
            self._read_until_ready()

    def tilt(self, angle: int) -> None:
        '''
        Instructs the scanner to tilt to an angle, then waits for a ready signal.

        Args:
            angle (int): the angle to tilt to.
        '''
        # don't send a command if the angle is invalid
        if angle >= 0 and angle <= self.max_angle:
            self.dev.write("TILT|{}".format(angle))
            self._ready = False
            self.tilt_angle = angle     # keep track of the new angle
            self._read_until_ready()

    def read_sensor(self) -> tuple:
        '''
        Instructs the scanner to send a sensor reading then waits for the reading and a ready signal. The data is then
        cleaned and returned as a tuple.

        This function assumes the data is sent as 3 separate lines consisting of the axis and coordinate. For example,
        a sensor reading of 445 at pan angle 10 tilt angle 35 should be sent as:
        X10
        Y35
        Z445

        Returns:
            tuple: (int: pan angle, int: tilt angle, int: sensor reading)
        '''
        self.dev.write("READSENSOR")    # send the instruction
        self._ready = False
        received = self._read_until_ready()
        # format the received data according to the expected form shown in the method docstring
        cleaned_data = [data.strip() for data in received if data.strip()[0] in ('X', 'Y', 'Z')]
        return tuple(val for val in cleaned_data)

    def center(self) -> None:
        '''
        Instructs the scanner to move to its center point, then checks the input buffer until it is empty and the
        scanner is ready for instruction.
        '''
        self.pan_angle = self.max_angle/2
        self.tilt_angle = self.max_angle/2
        self.pan(self.pan_angle)
        self.tilt(self.tilt_angle)
        self._read_until_ready()
