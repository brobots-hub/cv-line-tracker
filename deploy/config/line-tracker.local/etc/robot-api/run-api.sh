#! /usr/bin/env bash

cd /home/pi/config/src/server

# if [ ! -d venv ]; then
#     python3 -m venv venv
#     source venv/bin/activate
#     pip install -r requirements.txt
#     deactivate
# fi
# source venv/bin/activate

export NIX_PATH=nixpkgs=/nix/var/nix/profiles/per-user/root/channels/nixpkgs:/nix/var/nix/profiles/per-user/root/channels
export HOME=/home/pi

/nix/var/nix/profiles/default/bin/nix run nixpkgs.pythonRemoteEnv -c \
  python app.py --config /home/pi/config/line-tracker.local/etc/robot-api/robot-api.toml
