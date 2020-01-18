#!/usr/bin/env bash

set -u
# set -x

IMG_URL="https://downloads.raspberrypi.org/raspbian/images/raspbian-2019-09-30/2019-09-26-raspbian-buster.zip"
HASH_URL="${IMG_URL}.sha256"
OS_NAME=$(basename "$IMG_URL")

function isWSL() {
    uname -a | grep -q Microsoft
}

function die() {
    [ -n "${1:-}" ] && echo "$1"
    # wait for [Enter] when running git-bash from WSL
    [ -n "${SEPARATE_WINDOW:-}" ] && read
    exit 1
}

function checkAdmin() {
    #TODO git-bash
    if isWSL; then
        # TODO!!!
        ls ~root 1>&2 2>/dev/null || die "WSL shell must be 'Run as Administrator'"
    elif uname -a | grep -q Linux; then
        [[ $EUID > 0 ]] && die "This script must be run with 'sudo'"
    fi
}
checkAdmin

# this script can't run under WSL
GIT_BASH="/mnt/c/Program Files/Git/git-bash.exe"
isWSL && SEPARATE_WINDOW=yes exec "$GIT_BASH" "$0" "$@"

#------------------------------------------------------------------------------

function yesno() {
    local prompt="${1:-'[Y]es/[N]o?'}"
    read -p "$prompt" -n 1 -r
    [[ $REPLY =~ ^[Yy]$ ]] && return 0 || return 1
}

hash="$(curl --silent "$HASH_URL")"
echo "* Checking hash of OS. It may take some time..."
filehash="$(sha256sum $OS_NAME)"

if [ "$filehash" != "$hash" ]; then
    echo "Invalid hash"
    yesno "Should I redownload image?" \
        && rm -rf "$OS_NAME"
    echo
fi

if [ -f "$OS_NAME" ]; then
    echo "* Using existing file"
else
    curl -L -O "$IMG_URL"
fi


drive="${1:-}"

if [ -z "$drive" ]; then
    echo '* You have to enter name of disk. Run as'
    echo '  ./flash.sh /dev/sdb'
    echo ' or whatever disk you have. Here is list of disks with potential filesystem info:'
    devices="$(ls -d /dev/sd? /dev/mmcblk? 2>/dev/null)"
    for device in $devices; do
        echo
        echo "- device $device"
        dd if=$device of=/dev/stdout bs=1K count=1 status=none | strings
    done
    die
fi

yesno "Should I flash drive '$drive' ?" \
    && unzip -p $OS_NAME | dd if=/dev/stdin of=$drive bs=1M status=progress conv=fsync

echo
