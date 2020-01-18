#!/usr/bin/env bash

set -u
# set -x

IMG_URL="https://downloads.raspberrypi.org/raspbian/images/raspbian-2019-09-30/2019-09-26-raspbian-buster.zip"
HASH_URL="${URL}.sha256"
OS_NAME=$(basename "$IMG_URL")

GIT_BASH="/mnt/c/Program Files/Git/git-bash.exe"

hash="$(curl --silent "$HASH_URL")"
echo "Checking hash of OS. It may take some time..."
filehash="$(sha256sum $OS_NAME)"

if [ "$filehash" != "$hash" ]; then
    echo "Invalid hash"
    read -p "Are you sure? " -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$OS_NAME"
    fi
fi

if [ -f "$OS_NAME" ]; then
    echo "Using existing file"
else
    curl -L -O "$IMG_URL"
fi


drive="${1:-}"

if [ -z "$drive" ]; then
    echo 'You have to enter name of disk. Run as'
    echo '  ./flash.sh /dev/sdb'
    echo ' or whatever disk you have'
    "$GIT_BASH" -c 'for device in /dev/sd?; do echo; echo device $device; dd if=$device of=/dev/stdout bs=1K count=1 status=none | strings; done; read'
    exit 1
fi

echo "$drive"
read -p "Is that OK? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    "$GIT_BASH" -c "unzip -p $OS_NAME | dd if=/dev/stdin of=$drive bs=1M status=progress"
fi

echo
