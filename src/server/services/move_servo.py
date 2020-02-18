import logging
import multiprocessing
import time


def move_servo(angle, duration):
    """Move servo and return it back without blocking main process

    Parameters
    ----------
    angle: int
        Angle servo will move to.
    duration: int
        Duration (in ms) servo will stay turned for.
    """
    logging.info('Set servo to %i degrees for %ims', angle, duration)

    move = multiprocessing.Process(
        target=_move_servo, args=(angle, duration))
    move.start()


def _move_servo(angle, duration):
    """Actually move servo to specified angle for some duration.

    Parameters
    ----------
    angle: int
        Angle servo will move to.
    duration: int
        Duration (in ms) servo will stay turned for.
    """
    time.sleep(duration)
