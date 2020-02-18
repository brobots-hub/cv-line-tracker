import logging
import multiprocessing
import time


def spin_motors(power, duration):
    """Spin motor without blocking main process

    Parameters
    ----------
    power: int
        Speed of motor.
    duration: int
        Duration (in ms) servo will stay turned for.
    """
    logging.info('Spin motors for %ims at %i', duration, power)

    move = multiprocessing.Process(
        target=_spin_motors, args=(power, duration))
    move.start()


def _spin_motors(power, duration):
    """Actually spin motor for some duration

    Parameters
    ----------
    power: int
        Speed of motor.
    duration: int
        Duration (in ms) servo will stay turned for.
    """
    time.sleep(duration)
