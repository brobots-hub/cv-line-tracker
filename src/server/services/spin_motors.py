import logging
import multiprocessing
import time


def spin_motors(power, duration):
    """Spin motor for some duration

    Parameters
    ----------
    power: int
        Speed of motor.
    duration: int
        Duration (in ms) motors will spin for.
    """
    time.sleep(duration / 1000)
