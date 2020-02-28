#! /usr/bin/env bash

cd /home/pi/config/src/server

if [ ! -d venv ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
fi
source venv/bin/activate
exec python3 app.py --config /home/pi/config/line-tracker.local/etc/robot-api/robot-api.toml
