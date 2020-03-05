#! /usr/bin/env bash
export PATH=/nix/var/nix/profiles/default/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

rm -rf /dev/video*
uv4l --driver raspicam --encoding h264 \
    --framerate 10 --vflip --hflip --width 320 --height 240 \
    --frame-buffer 2 --enable-server on --device-name video0 \
    --profile high --server-option '--port=8088' -f -k -v 6 

