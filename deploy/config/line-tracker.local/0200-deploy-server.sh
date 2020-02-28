#! /usr/bin/env bash

# cp service file
# cp runner file
# cp configuration file
# enable service

sudo cp -rf etc/robot-api/robot-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable robot-api.service
sudo systemctl restart robot-api.service

