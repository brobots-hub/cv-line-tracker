#! /usr/bin/env bash

systemctl --user reset-failed

systemd-run --user --unit build-ffmpeg -E NIX_PATH=$NIX_PATH \
    nix-build '<nixpkgs>' -A ffmpeg_server || true
    
journalctl --user-unit build-ffmpeg -f &
PID="$!"
while systemctl --user status build-ffmpeg 1>/dev/null 2>/dev/null; do
  sleep 1
done
kill $PID
fg || true
