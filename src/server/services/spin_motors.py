import logging


def spin_motors(power, duration):
    logging.info('Spin motors for %ims at %i', duration, power)
