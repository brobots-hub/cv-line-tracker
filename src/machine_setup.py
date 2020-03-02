from gpiozero import PWMLED
from gpiozero import LED
from time import sleep
import curses

servo = PWMLED(17)
servo_min = 0.1
servo_max = 0.28

LEFT = +1
RIGHT = -1

#motor1 = PWMLED(5)
#motor2 = PWMLED(6)

motor1 = PWMLED(6)

def motor(speed=0.1, delay=0.2, eternal=False):
    motor1.value = abs(speed)
    if not eternal:
        sleep(delay)
        motor1.value = 0

# def motor(speed=0.1, delay=0.2, eternal=False):
#     if speed >= 0:
#         motor2.value = speed
#         motor1.value = 0
#     else:
#         motor1.value = abs(speed)
#         motor2.value = 0
#     if not eternal:
#         sleep(delay)
#         motor1.value = 0
#         motor2.value = 0

def rotate(angle=0):
  center = (servo_max + servo_min) / 2
  amp = (servo_max - servo_min) / 2
  servo.value = center + angle*amp

angle = 0.0
actions = {
        curses.KEY_UP:    lambda: motor(speed=0.4, eternal=True),
        curses.KEY_DOWN:  lambda: motor(speed=-0.4, eternal=True),
        curses.KEY_LEFT:  lambda: rotate(LEFT),
        curses.KEY_RIGHT: lambda: rotate(RIGHT),
}

def main(window):
    next_key = None
    while True:
        curses.halfdelay(1)
        if next_key is None:
            key = window.getch()
        else:
            key = next_key
            next_key = None
        if key != -1:
            # KEY PRESSED
            curses.halfdelay(3)
            action = actions.get(key)
            if action is not None:
                action()
            next_key = key
            while next_key == key:
                next_key = window.getch()
            # KEY RELEASED
            motor(speed=0, eternal=True)

def run_machine_v1():
    curses.wrapper(main)
