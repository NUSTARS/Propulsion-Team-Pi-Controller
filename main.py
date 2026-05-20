import RPi.GPIO as GPIO
import serial
from time import sleep


# Constants
CLOSED_ANGLE = 0
OPEN_ANGLE = 90
MIN_PULSE_WIDTH = 500
MAX_PULSE_WIDTH = 2500


# TODO: Pin numbers (placeholder is -1)
SOLENOID_ETHANOL_PIN = -1
SOLENOID_OXYGEN_PIN = -1
SERVO_NITROGEN_PURGE_PIN = -1
SERVO_NITROGEN_IN_PIN = -1
SPARK_PLUG_PIN = -1


# Pin setup
# Set pin numbering to BCM (Broadcom)
GPIO.setmode(GPIO.BCM)


# TODO: Initialize pins
# Format: GPIO.setup(<pin number>, <GPIO.IN or GPIO.OUT>)

# PWM Initializations
pwm_nitrogen_purge = GPIO.PWM(SERVO_NITROGEN_PURGE_PIN, 50)
pwm_nitrogen_purge.start(0)
pwm_nitrogen_in = GPIO.PWM(SERVO_NITROGEN_IN_PIN, 50)
pwm_nitrogen_in.start(0)
pwm_spark_plug = GPIO.PWM(SPARK_PLUG_PIN, 50)
pwm_spark_plug.start(0)

# Initial states
solenoid_state = 0x0
servo_state = 0x0
spark_plug_state = 0x0

# Serial communication setup
ser = serial.Serial('/dev/ttyS0', 9600, timeout=0)


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


def setSolenoids(received_data: bytes, state: int) -> int:
    # Only update when value is updated
    if ((received_data[0] & 0b00000001) != (state & 0b00000001)): # Check 1st bit
        # Set ethanol solenoid valve state (0 for closed, 1 for open)
        state ^= 0b00000001 # Toggle 1st bit
        GPIO.output(SOLENOID_ETHANOL_PIN, GPIO.HIGH if (received_data[0] & 0b00000001) else GPIO.LOW)
    if ((received_data[0] & 0b00000010) != (state & 0b00000010)): # Check 2nd bit
        # Set oxygen solenoid valve state (0 for closed, 1 for open)
        state ^= 0b00000010 # Toggle 2nd bit
        GPIO.output(SOLENOID_OXYGEN_PIN, GPIO.HIGH if (received_data[0] & 0b00000010) else GPIO.LOW)
    return state


def setBallvalves(received_data: bytes, state: int) -> int:
    # Only update when value is updated
    if ((received_data[0] & 0b00000100) != (state & 0b00000100)): # Check 3rd bit
        # Set nitrogen purge valve state (0 for closed, 1 for open)
        state ^= 0b00000100 # Toggle 3rd bit
        setAngle(OPEN_ANGLE if (received_data[0] & 0b00000100) else CLOSED_ANGLE, pwm_nitrogen_purge)
    if ((received_data[0] & 0b00001000) != (state & 0b00001000)): # Check 4th bit
        # Set nitrogen in valve state (0 for closed, 1 for open)
        state ^= 0b00001000 # Toggle 4th bit
        setAngle(OPEN_ANGLE if (received_data[0] & 0b00001000) else CLOSED_ANGLE, pwm_nitrogen_in)
    return state


def setSparkPlug(received_data: bytes, state: int) -> int:
    # Only update when value is updated
    if ((received_data[0] & 0b00010000) != (state & 0b00010000)): # Check 5th bit
        # Set spark plug state (0 for off, 1 for on)
        state ^= 0b00010000 # Toggle 5th bit
        # TODO: Start PWM to turn on spark plug
        if (received_data[0] & 0b00010000):
            pass
        else:
            pass
    return state


try:
    # Main execution loop
    while True:
        # Check if data to read
        if ser.in_waiting > 0:
            # Read data from UART
            received_data = ser.read(1) # 8 bits
            sleep(0.03) # Delay to ensure data is fully received
            # necessary? data_left = ser.in_waiting()
            # necessary? received_data += ser.read(data_left) # Read remaining data
            print(received_data) # Debug: Print received data
            ser.write(received_data) # Echo back received data?

            # Act on data
            # 1st bit: Ethanol solenoid valve state (0 for closed, 1 for open)
            # 2nd bit: Oxygen solenoid valve state (0 for closed, 1 for open)
            # 3rd bit: Nitrogen purge valve state (0 for closed, 1 for open)
            # 4th bit: Nitrogen in valve state (0 for closed, 1 for open)
            # 5th bit: Spark plug state (0 for off, 1 for on)

            # Set solenoid states based on received data (1st and 2nd bits)
            solenoid_state = setSolenoids(received_data, solenoid_state)

            # Set ball valve states based on received data (3rd and 4th bits)
            servo_state = setBallvalves(received_data, servo_state)
            
            # Set spark plug state based on received data (5th bit)
            spark_plug_state = setSparkPlug(received_data, spark_plug_state)

        sleep(0.01) # Delay to prevent CPU overuse

        

except Exception as e:
    print("Error:", e)
finally:
    # Reset pins to default state after execution
    GPIO.cleanup()



