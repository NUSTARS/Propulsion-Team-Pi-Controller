import RPi.GPIO as GPIO
import threading
import time


# Constants
CLOSED_ANGLE = 0
OPEN_ANGLE = 180


main_polling_thread = threading.Thread(target=mainPollingThread, args=None)


# Pin setup
# Set pin numbering to BCM (Broadcom)
GPIO.setmode(GPIO.BCM)
# TODO: Initialize pins
# Format: GPIO.setup(<pin number>, <GPIO.IN or GPIO.OUT>)


main_polling_thread.start()


# TODO: Main thread to check input status
def mainPollingThread() -> None:
    try:
        # Main execution loop
        while True:
            pass
        
    except KeyboardInterrupt:
        # Reset pins to default state after execution
        GPIO.cleanup()


# TODO: Sets angle through PWM of specified pin
def setAngle(angle: int, servo_num: int) -> None:
    pass


# TODO: Sends data through tx
def sendData(buffer: int, size: int) -> None:
    pass


# TODO: Controls ball valves
def controlBallValves(input_data: int, valve_state: int) -> None:
    pass


