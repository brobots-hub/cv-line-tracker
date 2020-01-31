from datetime import datetime

import flask
from flask import request

app = flask.Flask(__name__)


@app.route('/api/v1/healthcheck', methods=['GET'])
def healthcheck():
    return 'ok', 200


@app.route('/api/v1/motor', methods=['POST'])
def control_motors():
    power = request.form.get('power', default=0, type=int)
    duration = request.form.get('duration', default=0, type=int)

    # TODO

    return ''


@app.route('/api/v1/servo', methods=['POST'])
def control_servo():
    angle = request.form.get('angle', default=0, type=int)
    duration = request.form.get('duration', default=0, type=int)

    # TODO

    return ''


@app.route('/api/v1/debug/log', methods=['GET'])
def get_logs():
    timestamp = request.args.get('after', default='', type=str)

    if not timestamp:
        return '', 400

    timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

    # TODO

    return ''


@app.route('/api/v1/debug/clear_log', methods=['POST'])
def clear_logs():
    # TODO

    return ''


@app.errorhandler(404)
def page_not_found(e):
    return "The resource could not be found", 404


app.run('localhost', port=8080)
