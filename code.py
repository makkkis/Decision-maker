import board
import busio
import time
import random
import digitalio
import supervisor
from dfplayer_mini import DFRobotDFPlayerMini

# Initialize UART for DFPlayer Mini
uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=0.1)

# Initialize DFPlayer Mini
dfplayer = DFRobotDFPlayerMini(uart)

# Initialize button on pin D2
button = digitalio.DigitalInOut(board.D2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Enable pull-up resistor

# Assume there are 10 tracks on the SD card for random selection
total_tracks = 10

print("DFPlayer Mini initialized")

# Function to play a random track
def play_random_track():
    track_number = random.randint(1, total_tracks)
    print(f"Playing random track {track_number}")
    dfplayer.play(track_number)

#supervisor.disable_autoreload()

print("DFPlayer Mini Test Begin")

# Main loop
while True:
    # Check if button is pressed (low signal means pressed)
    if not button.value:
        print("Button pressed")
        play_random_track()
        # Wait until the button is released to avoid multiple triggers
        while not button.value:
            time.sleep(0.1)  # Debounce delay

    time.sleep(0.1)  # Small delay to avoid excessive CPU usage
