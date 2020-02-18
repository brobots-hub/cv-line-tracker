from gpiozero import PWMLED
from gpiozero import LED
from time import sleep

servo = PWMLED(17)
servo_min = 0.1
servo_max = 0.3

led1 = LED(5)
led2 = LED(6)

def back(delay=0.2):
  led1.on()
  led2.off()
  sleep(delay)
  led1.off()


def forward(delay=0.2):
  led2.on()
  led1.off()
  sleep(delay)
  led2.off()

def rotate(angle=0):
  center = (servo_max + servo_min) / 2
  amp = (servo_max - servo_min) / 2
  servo.value = center + angle*amp


