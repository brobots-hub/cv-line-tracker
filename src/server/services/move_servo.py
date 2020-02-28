import logging
import multiprocessing
import time


def move_servo(angle, duration):
    """Move servo to specified angle for some duration.

    Parameters
    ----------
    angle: int
        Angle servo will move to.
    duration: int
        Duration (in ms) servo will stay turned for.
    """
    time.sleep(duration / 1000)
