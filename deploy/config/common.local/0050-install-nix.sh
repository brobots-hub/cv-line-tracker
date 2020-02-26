#! /usr/bin/env bash

# if nix is installed, do nothing
nix-env --version && exit 0 || true

yes | sh <(curl https://nixos.org/nix/install) --daemon && (
# we have to PREPEND, not APPEND, because of https://stackoverflow.com/questions/216202/why-does-an-ssh-remote-command-get-fewer-environment-variables-then-when-run-man
sudo sed -i.old '1s;^;source /etc/profile.d/nix.sh\n;' /etc/bash.bashrc
sudo -i nix-channel --update # as of time of writing this issue was not yet resolved https://github.com/NixOS/nix/issues/2733
sudo mount --bind -o ro,bind /nix/store /nix/store
)


