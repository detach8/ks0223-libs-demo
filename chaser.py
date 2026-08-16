import time, cv2, ultralytics
from picamera2 import Picamera2
import lib.motor as motor
import lib.servo as servo
import lib.line_tracker as tracker

MIN_ANGLE = 0
MAX_ANGLE = 180
PAN_STEP = 10
TILT_STEP = 10
MOVE_TIME = 0.3
MOVE_SPEED = 50

# Load the edge-optimized YOLO26 nano model
print("Loading YOLO model...")
model = ultralytics.YOLO("yolo26n.pt")

def clamp(angle):
    return max(MIN_ANGLE, min(MAX_ANGLE, angle))

def track():
    track = tracker.get_tracking(tracker.MODE_DETECT_WHITE_LINE)
    print("Line tracking:", track)

    if track == "STRAIGHT":
        motor.forward(20)
    elif track == "L" or track == "LL":
        motor.forward(25, -5)
    elif track == "R" or track == "RR":
        motor.forward(25, 5)
    else:
        motor.stop() 

    time.sleep(0.01)

def start():
    global MOVE_SPEED

    print("Initializing servos...")
    pan_angle = 83
    tilt_angle = 105
    pan = servo.setup(7)
    tilt = servo.setup(6)
    servo.rotate(pan, pan_angle)
    servo.rotate(tilt, tilt_angle)

    print("Initializing camera...")
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
    picam2.configure(config)
    picam2.start()

    frame_count = 0

    while True:
        # Capture frame as a NumPy array (RGB format)
        frame = picam2.capture_array()

        # Display the output
        cv2.imshow("Pi Camera", frame)

        if frame_count % 3 == 0:

            # YOLO expects BGR if you pass it directly to OpenCV for display later,
            # or you can convert colors:
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Run YOLO inference
            results = model(frame_bgr, imgsz=320, verbose=False)
            r = results[0]

            target_found = False

            # Loop through all detected objects in the frame
            if r.boxes is not None:
                for box in r.boxes:
                    class_id = int(box.cls[0])
                    class_name = r.names[class_id]

                    # Filter for 'teddy bear' class
                    if class_name == "teddy bear":
                        # Extract bounding box coordinates (xmin, ymin, xmax, ymax)
                        xmin, ymin, xmax, ymax = box.xyxy[0].tolist()

                        # Calculate center X and Y coordinates
                        center_x = int((xmin + xmax) / 2)
                        center_y = int((ymin + ymax) / 2)

                        # Calculate the size of the box
                        size_w = xmax - xmin
                        size_h = ymax - ymin
                        area = size_w * size_h

                        # Extract confidence score
                        confidence = float(box.conf[0])

                        # Print information
                        print(
                            f"Target -> Center: ({center_x}, {center_y}) |"
                            f" Area: {area} |"
                            f" Confidence: {confidence:.2f}"
                        )

                        if area < 256000 and confidence > 0.5:
                            if center_x < 220:
                                motor.rotate(30, motor.DIRECTION_LEFT)
                                time.sleep(0.1)
                                motor.stop()
                            elif center_x > 420:
                                motor.rotate(30, motor.DIRECTION_RIGHT)
                                time.sleep(0.1)
                                motor.stop()
                            else:
                                motor.forward(20)

                            target_found = True
                            
                        break

            # Reset frame counter
            frame_count = 0

        frame_count += 1

        if not target_found:
            motor.stop()

        key = cv2.waitKeyEx(1)

        # Press Q to Quit
        if key in (ord("q"), ord("Q")):
            break

    picam2.stop()
    cv2.destroyAllWindows()

def contro(key):
    # Speed settings
    if key == ord("1"):
        MOVE_SPEED = 10
    elif key == ord("2"):
        MOVE_SPEED = 20
    elif key == ord("3"):
        MOVE_SPEED = 30
    elif key == ord("4"):
        MOVE_SPEED = 40
    elif key == ord("5"):
        MOVE_SPEED = 50
    elif key == ord("6"):
        MOVE_SPEED = 60
    elif key == ord("7"):
        MOVE_SPEED = 70
    elif key == ord("8"):
        MOVE_SPEED = 80
    elif key == ord("9"):
        MOVE_SPEED = 90
    elif key == ord("0"):
        MOVE_SPEED = 100

    # Car controls — WASD
    elif key in (ord("w"), ord("W")):
        motor.forward(MOVE_SPEED)
    elif key in (ord("s"), ord("S")):
        motor.reverse(MOVE_SPEED)
    elif key in (ord("a"), ord("A")):
        motor.rotate(MOVE_SPEED, motor.DIRECTION_LEFT)
    elif key in (ord("d"), ord("D")):
        motor.rotate(MOVE_SPEED, motor.DIRECTION_RIGHT)

    # Camera servo controls — arrow keys
    elif key == 65361:
        pan_angle = clamp(pan_angle + PAN_STEP)
        servo.rotate(pan, pan_angle)

    elif key == 65363:
        pan_angle = clamp(pan_angle - PAN_STEP)
        servo.rotate(pan, pan_angle)

    elif key == 65362:
        tilt_angle = clamp(tilt_angle - TILT_STEP)
        servo.rotate(tilt, tilt_angle)

    elif key == 65364:
        tilt_angle = clamp(tilt_angle + TILT_STEP)
        servo.rotate(tilt, tilt_angle)
    # No key pressed
    elif key == -1:
        motor.stop()

start()