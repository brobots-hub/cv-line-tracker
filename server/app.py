from datetime import datetime
import logging

import flask
from flask import request, jsonify, logging as flog

from services.move_servo import move_servo
from services.spin_motors import spin_motors
from services.logs_after import logs_after

log_format = '%(asctime)s %(levelname)s: %(message)s'

app = flask.Flask(__name__)
flog.default_handler.setFormatter(logging.Formatter(log_format))
logging.basicConfig(filename='/var/log/rpicontrol.log',
                    format=log_format,
                    level=logging.DEBUG)


@app.route('/api/v1/healthcheck', methods=['GET'])
def healthcheck():
    return 'ok', 200


@app.route('/api/v1/motor', methods=['POST'])
def control_motors():
    power = request.form.get('power', default=0, type=int)
    duration = request.form.get('duration', default=0, type=int)

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
    duration = request.form.get('duration', default=0, type=int)

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
    open('/var/log/rpicontrol.log', 'w').close()

    return 'ok', 200


@app.errorhandler(404)
def page_not_found(e):
    return 'The resource could not be found', 404


app.run('localhost', port=8080)
