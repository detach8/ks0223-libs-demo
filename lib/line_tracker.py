import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # use BCM numbers

# Tracking pins config
TRACKING_PIN1 = 17
TRACKING_PIN2 = 18
TRACKING_PIN3 = 19

# Modes
MODE_DETECT_WHITE_LINE = 0 # White = 0
MODE_DETECT_BLACK_LINE = 1 # Black = 1

# Set GPIO pins to INPUT mode
GPIO.setup(TRACKING_PIN1, GPIO.IN)
GPIO.setup(TRACKING_PIN2, GPIO.IN)
GPIO.setup(TRACKING_PIN3, GPIO.IN)

def get_array():
    return (
        GPIO.input(TRACKING_PIN1),
        GPIO.input(TRACKING_PIN2),
        GPIO.input(TRACKING_PIN3),
    )

def get_tracking(mode):
    p = 0
    n = 0
    if mode == MODE_DETECT_BLACK_LINE:
        p = MODE_DETECT_BLACK_LINE
        n = MODE_DETECT_WHITE_LINE
    elif mode == MODE_DETECT_WHITE_LINE:
        p = MODE_DETECT_WHITE_LINE
        n = MODE_DETECT_BLACK_LINE
    else:
        print("Invalid line tracking mode")
        return
    
    track = get_array()
    print(track)

    if track == (p, p, p) or track == (n, p, n):
        return "STRAIGHT"
    elif track == (p, p, n):
        return "L"
    elif track == (n, p, p):
        return "R"
    elif track == (p, n, n):
        return "LL"
    elif track == (n, n, p):
        return "RR"
    else:
        return "STOP"
    
