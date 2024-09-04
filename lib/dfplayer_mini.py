import time

DFPLAYER_RECEIVED_LENGTH = 10

class DFRobotDFPlayerMini:
    def __init__(self, uart):
        self._uart = uart
        self._sending = bytearray([0x7E, 0xFF, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEF])
        self._received = bytearray(DFPLAYER_RECEIVED_LENGTH)
        print("DFPlayer Mini initialized")

    def send_stack(self, command, argument=0):
        self._sending[3] = command
        self._sending[5] = (argument >> 8) & 0xFF
        self._sending[6] = argument & 0xFF
        checksum = self.calculate_checksum(self._sending)
        self._sending[7] = (checksum >> 8) & 0xFF
        self._sending[8] = checksum & 0xFF
        self._uart.write(self._sending)
        print(f"Command 0x{command:02X} sent with argument {argument}")

    def calculate_checksum(self, buffer):
        checksum = 0
        for i in range(1, 7):
            checksum += buffer[i]
        return 0xFFFF - checksum + 1

    def next(self):
        print("Sending next command")
        self.send_stack(0x01)

    def previous(self):
        print("Sending previous command")
        self.send_stack(0x02)

    def play(self, file_number=1):
        print(f"Sending play command for file {file_number}")
        self.send_stack(0x03, file_number)

    def volume_up(self):
        print("Sending volume up command")
        self.send_stack(0x04)

    def volume_down(self):
        print("Sending volume down command")
        self.send_stack(0x05)

    def volume(self, volume):
        print(f"Setting volume to {volume}")
        self.send_stack(0x06, volume)

    def available(self):
        if self._uart.in_waiting >= DFPLAYER_RECEIVED_LENGTH:
            self._received = self._uart.read(DFPLAYER_RECEIVED_LENGTH)
            print("Received data from DFPlayer Mini")
            return self.validate_stack()
        return False

    def validate_stack(self):
        if self._received[0] == 0x7E and self._received[9] == 0xEF:
            checksum = self.calculate_checksum(self._received)
            valid = (self._received[7] << 8 | self._received[8]) == checksum
            print(f"Checksum valid: {valid}")
            return valid
        print("Invalid data received")
        return False

    def read_command(self):
        return self._received[3]

    def read(self):
        return self._received[5] << 8 | self._received[6]
