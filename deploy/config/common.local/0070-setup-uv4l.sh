#! /usr/bin/env bash

if which uv4l 2>/dev/null; then :; else
    curl http://www.linux-projects.org/listing/uv4l_repo/lpkey.asc | sudo apt-key add -
    echo 'deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/stretch stretch main' | sudo tee -a /etc/apt/sources.list
    sudo apt-get update
    sudo apt-get -y install uv4l uv4l-server uv4l-raspicam
    # it pollutes environment with custom LD_PRELOAD. We'll readd it in service instead
    truncate -s0 /etc/environment
fi

sudo cp -rf etc/uv4l.service /etc/systemd/system/
sudo cp -rf etc/run-uv4l.sh /usr/local/bin/
sudo systemctl daemon-reload
sudo systemctl enable uv4l.service
sudo systemctl restart uv4l.service
