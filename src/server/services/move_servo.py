import logging


def move_servo(angle, duration):
    logging.info('Set servo to %i degrees for %ims', angle, duration)
