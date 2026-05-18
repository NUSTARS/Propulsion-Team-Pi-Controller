import RPi.GPIO as GPIO


# Constants
CLOSED_ANGLE = 0
OPEN_ANGLE = 90
MIN_PULSE_WIDTH = 500
MAX_PULSE_WIDTH = 2500


# TODO: Pin numbers (placeholder is -1)
SERVO_NITROGEN_PURGE_PIN = -1
SERVO_NITROGEN_IN_PIN = -1


# Pin setup
# Set pin numbering to BCM (Broadcom)
GPIO.setmode(GPIO.BCM)


# TODO: Initialize pins
# Format: GPIO.setup(<pin number>, <GPIO.IN or GPIO.OUT>)

# PWM Initializations
pwm_1_nitrogen_purge = GPIO.PWM(SERVO_NITROGEN_PURGE_PIN, 50)
pwm_1_nitrogen_purge.start(0)
pwm_2_nitrogen_in = GPIO.PWM(SERVO_NITROGEN_IN_PIN, 50)
pwm_2_nitrogen_in.start(0)


try:
    # TODO: Main execution loop
    while True:
        # TODO: Read data

        # TODO: Act on data


except Exception as e:
    print("Error:", e)
finally:
    # Reset pins to default state after execution
    GPIO.cleanup()


# Sets angle through PWM of specified pin
def setAngle(angle: int, servo: GPIO.PWM) -> None:
    if (angle < 0):
        angle = 0
    elif (angle > 270):
        angle = 270
    pulse = ((angle * (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH)) / 270) + MIN_PULSE_WIDTH
    duty_cycle = (pulse / 20000) * 100
    servo.ChangeDutyCycle(duty_cycle)



# TODO: Sends data through tx
def sendData(buffer: int, size: int) -> None:
    pass


# TODO: Controls ball valves
def controlBallValves(input_data: int, valve_state: int) -> None:
    pass


