from datetime import datetime
import logging

import flask
from flask import request, jsonify, logging as flog
import argparse
import toml

from ProcessManager import ProcessManager
from services.move_servo import move_servo
from services.spin_motors import spin_motors
from services.logs_after import logs_after
from services.check_wifi import check_wifi

from gpiozero import PWMLED

servo = PWMLED(13)
servo_center=0.125
servo_span=0.045
servo_min = servo_center-servo_span
servo_max = servo_center+servo_span

LEFT = +1
RIGHT = -1

motor1 = PWMLED(6)

def motor(speed=0.1, delay=0.2, eternal=False):
    motor1.value = abs(speed)
    if not eternal:
        sleep(delay)
        motor1.value = 0

def rotate(angle=0):
  servo.value = servo_center + angle * servo_span


def process_args():
    import pathlib
    path_to_this = pathlib.Path(__file__).parent.absolute()

    parser = argparse.ArgumentParser(description='RaspberryPi control server.')
    parser.add_argument('--config',
                        help='path to config file', default=path_to_this / '../../config/development.toml')

    args = parser.parse_args()
    print(f'Using config file {args.config}')
    config = toml.load(args.config)
    return config


config = process_args()

app = flask.Flask(__name__)
flog.default_handler.setFormatter(logging.Formatter(config['log_format']))
logging.basicConfig(filename=config['log_file'],
                    format=config['log_format'],
                    level=logging.DEBUG)
print(f'Flask logger is redirected to {config["log_file"]}')

pm = ProcessManager()
pm.add_job('motor', spin_motors)
pm.add_job('servo', move_servo)


@app.route('/api/v1/healthcheck', methods=['GET'])
def healthcheck():
    return 'ok', 200


@app.route('/api/v1/wifistrength', methods=['GET'])
def wifi_strength():
    return check_wifi(), 200


@app.route('/api/v1/motor', methods=['POST'])
def control_motors():
    power = request.form.get('power', default=None, type=float)
    duration = request.form.get(
        'duration', default=config['motor_duration_default'], type=float)

    if power is None:
        logging.warn('Power is not provided')
        return 'power is not provided', 400

    try:
        motor(power, eternal=True)
        return 'ok', 200

    except Exception as e:
        logging.warn(
            'Function error output: %s; power: %i; duration: %ims;', e, power, duration)
        return 'error', 400


@app.route('/api/v1/servo', methods=['POST'])
def control_servo():
    angle = request.form.get('angle', default=0, type=float)
    duration = request.form.get(
        'duration', default=config['servo_duration_default'], type=float)

    if angle is None:
        logging.warn('Angle is not provided')
        return 'angle is not provided', 400

    try:
        servo.value = angle
        return 'nice', 200

    except Exception as e:
        logging.warn(
            'Function error output: %s; angle: %i; duration: %ims;', e, angle, duration)
        return 'error', 400


@app.route('/api/v1/debug/log', methods=['GET'])
def get_logs():
    timestamp = request.args.get('after', default='', type=str)

    if not timestamp:
        return 'invalid args', 400

    timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S,%f')
    logs = logs_after(timestamp)

    return jsonify({'logs': logs}), 200


@app.route('/api/v1/debug/clear_log', methods=['POST'])
def clear_logs():
    open(config['log_file'], 'w').close()

    return 'ok', 200


@app.errorhandler(404)
def page_not_found(e):
    return 'the resource could not be found', 404


app.run(host=config['host'], port=config['server_port'])

