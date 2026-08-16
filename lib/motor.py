import RPi.GPIO as GPIO

GPIO.setwarnings(False) # Quell channel in use warnings
GPIO.setmode(GPIO.BCM)  # Use BCM numbers

# Motors config
MOTORS = {
    "RL": {"D1": 20, "D2": 21, "PWM": 0, "DIR": True},
    "FL": {"D1": 22, "D2": 23, "PWM": 1, "DIR": False},
    "FR": {"D1": 24, "D2": 25, "PWM": 12, "DIR": False},
    "RR": {"D1": 26, "D2": 27, "PWM": 13, "DIR": True},
}

# Config PWM frequency
PWM_FREQ = 1000 # 1khz

DIRECTION_RIGHT = 1
DIRECTION_LEFT = -1

# Setup PWMs and set GPIO pins to OUTPUT mode
pwms = {}
directions = {}
for motor in MOTORS:
    print("Initializing motor", motor)
    GPIO.setup(MOTORS[motor]["D1"], GPIO.OUT)
    GPIO.setup(MOTORS[motor]["D2"], GPIO.OUT)
    GPIO.setup(MOTORS[motor]["PWM"], GPIO.OUT)

    # Setup PWM
    pwm = GPIO.PWM(MOTORS[motor]["PWM"], PWM_FREQ)
    pwm.start(0) # Set inital duty cycle to 0
    pwms[motor] = pwm

    # Set initial direction to forward
    GPIO.output(MOTORS[motor]["D1"], GPIO.LOW if MOTORS[motor]["DIR"] else GPIO.HIGH)
    GPIO.output(MOTORS[motor]["D2"], GPIO.HIGH if MOTORS[motor]["DIR"] else GPIO.LOW)
    directions[motor] = True

def motor_forward(motor):
    global directions
    if not directions[motor]:
        GPIO.output(MOTORS[motor]["D1"], GPIO.LOW if MOTORS[motor]["DIR"] else GPIO.HIGH)
        GPIO.output(MOTORS[motor]["D2"], GPIO.HIGH if MOTORS[motor]["DIR"] else GPIO.LOW)
        directions[motor] = True

def motor_reverse(motor):
    global directions
    if directions[motor]:
        GPIO.output(MOTORS[motor]["D1"], GPIO.HIGH if MOTORS[motor]["DIR"] else GPIO.LOW)
        GPIO.output(MOTORS[motor]["D2"], GPIO.LOW if MOTORS[motor]["DIR"] else GPIO.HIGH)
        directions[motor] = False

def motor_speed(motor, speed):
    pwms[motor].ChangeDutyCycle(speed)

def limit_speed(speed):
    if (speed > 100):
        return 100
    if (speed < 0):
        return 0
    return speed

def forward(speed, turn = 0):
    motor_forward("FL")
    motor_forward("FR")
    motor_forward("RL")
    motor_forward("RR")
    motor_speed("FL", limit_speed(speed + turn))
    motor_speed("FR", limit_speed(speed - turn))
    motor_speed("RL", limit_speed(speed + turn))
    motor_speed("RR", limit_speed(speed - turn))

def reverse(speed, turn = 0):
    motor_reverse("FL")
    motor_reverse("FR")
    motor_reverse("RL")
    motor_reverse("RR")
    motor_speed("FL", limit_speed(speed + turn))
    motor_speed("FR", limit_speed(speed - turn))
    motor_speed("RL", limit_speed(speed + turn))
    motor_speed("RR", limit_speed(speed - turn))

def rotate(speed, direction):
    if direction == DIRECTION_RIGHT:
        motor_forward("FL")
        motor_reverse("FR")
        motor_forward("RL")
        motor_reverse("RR")
        motor_speed("FL", speed)
        motor_speed("FR", speed)
        motor_speed("RL", speed)
        motor_speed("RR", speed)
    if direction == DIRECTION_LEFT:
        motor_reverse("FL")
        motor_forward("FR")
        motor_reverse("RL")
        motor_forward("RR")
        motor_speed("FL", speed)
        motor_speed("FR", speed)
        motor_speed("RL", speed)
        motor_speed("RR", speed)

def stop():
    motor_speed("FL", 0)
    motor_speed("FR", 0)
    motor_speed("RL", 0)
    motor_speed("RR", 0)

stop()
