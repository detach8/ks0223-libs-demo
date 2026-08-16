# Keyestudio KS0223 Smart Car Kit Libraries and Demo

Python libraries and interactive demos for the **Keyestudio KS0223 Smart
Car Kit** for elementary-level STEM education and hands-on robotics
learning.

## Libraries & Components

The core drivers and helper functions are organized inside the `lib/` directory:

| Component | Module | Status | Description |
| :--- | :--- | :--- | :--- |
| **Motor** | `lib/motor.py` | Ready | Motor movement and direction control |
| **Servo** | `lib/servo.py` | Ready | Servo motor angle control |
| **Line Tracker** | `lib/line_tracker.py` | Ready | Surface line tracking sensor |
| **Buzzer** | `lib/buzzer.py` | TODO | Audio feedback and tones |
| **IR Receiver** | `lib/ir_receiver.py` | TODO | Infrared remote control |
| **Matrix LCD** | `lib/matrix_lcd.py` | TODO | Matrix display output |
| **Ultrasound** | `lib/ultrasound.py` | TODO | Distance measurement sensor |
---

## Prerequisites

* **Hardware:** Keyestudio KS0223 Smart Car Kit powered by a Raspberry Pi (Raspberry Pi 4B or higher recommended for computer vision demos).
* **OS:** Raspberry Pi OS
* **Python:** Python 3.11+ (tested on 3.13)

## Setup & Installation

1. Switch to the working directory:

        cd ks0223-libs-demo

2. Create a new virtual environment that inherits system packages:

        python3 -m venv --system-site-packages venv

3. Activate the virtual environment:

        source venv/bin/activate

4. Install Python dependencies. (Note: A temporary directory is used below
because default Raspberry Pi installations often have insufficient space
in `/tmp`):

        mkdir ./tmp
        TMPDIR=./tmp pip install -r requirements.txt
        rmdir tmp

## Running Demos

NOTE: All demos require the virtual environment to be activated (`source venv/bin/activate`)

### Teddy bear chaser (chaser.py)

This demo uses computer vision to detect teddy bears and make the robot
chase after them.

* Prerequisite: Requires a Raspberry Pi 4B or higher.
* Model Setup: Download the `yolo26n.pt` model from https://platform.ultralytics.com/ultralytics/yolo26/yolo26n and place it directly in the project root directory.
* Run:

        python3 chaser.py

### TODO: Simple remote control (remote_control.py)

Allows you to drive the car remotely and control the servo pan/tilt
using the infrared (IR) remote controller.

* Run:

        python3 remote_control.py

### TODO: Line following (line_follow.py)

Makes the robot follow a black line path. (Tip: Modify the source code
if you want to follow a white line instead).

* Run:

        python3 line_follow.py

## Author

Justin Lee <tzlee@tzlee.com>

## License

Distributed under the MIT License. See LICENSE for more information.