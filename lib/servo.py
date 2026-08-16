import RPi.GPIO as GPIO
import time

MIN_ANGLE = 0
MAX_ANGLE = 180

GPIO.setwarnings(False) # Quell channel in use warnings
GPIO.setmode(GPIO.BCM)  # Use BCM numbers

def setup(pin = 5):
    GPIO.setup(pin, GPIO.OUT)
    print("Setup pin", pin, "with PWM")
    pwm = GPIO.PWM(pin, 50)
    pwm.start(7.5)
    return pwm
    
def rotate(pwm, angle):
    duty = 2.5 + _clamp(angle) / 18.0
    print("Duty cycle", duty)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.3)
    pwm.ChangeDutyCycle(0)

def _clamp(angle):
    return max(MIN_ANGLE, min(MAX_ANGLE, angle))