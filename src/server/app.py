from datetime import datetime
import logging

import flask
from flask import request, jsonify, logging as flog
import argparse
import toml

from services.move_servo import move_servo
from services.spin_motors import spin_motors
from services.logs_after import logs_after

def process_args(): 
    import pathlib
    path_to_this = pathlib.Path(__file__).parent.absolute()

    parser = argparse.ArgumentParser(description='RaspberryPi control server.')
    parser.add_argument('--config',
                        help='path to config file', default=path_to_this / '../../config/development.toml')

    args = parser.parse_args()
    print(f"Using config file {args.config}")
    config = toml.load(args.config)
    return config

config = process_args()

log_format = '%(asctime)s %(levelname)s: %(message)s'

app = flask.Flask(__name__)
flog.default_handler.setFormatter(logging.Formatter(log_format))
logging.basicConfig(filename=config["log_file"],
                    format=log_format,
                    level=logging.DEBUG)
print(f'Flask logger is redirected to {config["log_file"]}')


@app.route('/api/v1/healthcheck', methods=['GET'])
def healthcheck():
    return 'ok', 200


@app.route('/api/v1/motor', methods=['POST'])
def control_motors():
    power = request.form.get('power', default=0, type=int)
    duration = request.form.get('duration', default=config["motor_duration_default"], type=int)

    try:
        spin_motors(power, duration)
        logging.info('Spin motors for %i ms at power %i', duration, power)

        return 'ok', 200

    except:
        return 'Invalid args', 400

    return ''


@app.route('/api/v1/servo', methods=['POST'])
def control_servo():
    angle = request.form.get('angle', default=0, type=int)
    duration = request.form.get('duration', default=["servo_duration_default"], type=int)

    try:
        move_servo(angle, duration)
        logging.info('Set servo to %i degrees for %i', power, duration)

        return 'ok', 200

    except:
        return 'Invalid args', 400


@app.route('/api/v1/debug/log', methods=['GET'])
def get_logs():
    timestamp = request.args.get('after', default='', type=str)

    if not timestamp:
        return '', 400

    timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S,%f")
    logs = logs_after(timestamp)

    return jsonify({'logs': logs}), 200


@app.route('/api/v1/debug/clear_log', methods=['POST'])
def clear_logs():
    open(config["log_file"], 'w').close()

    return 'ok', 200


@app.errorhandler(404)
def page_not_found(e):
    return 'The resource could not be found', 404


app.run('localhost', port=config["server_port"])
