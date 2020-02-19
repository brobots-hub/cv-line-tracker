#! /usr/bin/env bash

sudo rm -rf /dev/video* && sudo pkill uv4l

uv4l --driver raspicam --encoding h264 \
    --framerate 10 --vflip --hflip --width 320 --height 240 \
    --frame-buffer 2 --enable-server on --device-name video0 \
    --profile high --server-option '--port=8088'

