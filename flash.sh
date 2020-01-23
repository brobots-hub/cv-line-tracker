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
        /mnt/c/WINDOWS/system32/net.exe session 1>&2 2>/dev/null|| die "WSL shell must be 'Run as Administrator'"
    elif uname -a | grep -q Linux; then
        [[ $EUID > 0 ]] && die "This script must be run with 'sudo'"
    fi
}
checkAdmin

# this script can't run under WSL
GIT_BASH="/mnt/c/Program Files/Git/git-bash.exe"
# ugh. No easy way to pass envvar from WSL to git-bash
isWSL && exec "$GIT_BASH" -c "export SEPARATE_WINDOW=yes; export drive="${1:-}"; bash $0 \"\$@\"" "$@"

#------------------------------------------------------------------------------

trap '[ -n ${SEPARATE_WINDOW:-} ] && echo "Press any key to exit..." && read' EXIT

function yesno() {
    local prompt="${1:-'[Y]es/[N]o?'}"
    read -p "$prompt" -n 1 -r && echo
    [[ $REPLY =~ ^[Yy]$ ]] && return 0 || return 1
}

hash="$(curl --silent "$HASH_URL")"
echo "* Checking hash of OS. It may take some time..."
filehash="$(sha256sum -t $OS_NAME)"

if [ "$filehash" != "$hash" ]; then
    echo "Invalid hash"
    yesno "Should I redownload image?" \
        && rm -rf "$OS_NAME"
    echo
fi

if [ -f "$OS_NAME" ]; then
    echo "* Using existing file"
else
    trap 'exit 1' SIGINT # handle Ctrl-C correctly in a while true loop
    while true; do
        sleep 1
        curl -L -O -C - "$IMG_URL" && break
    done
fi

if [ -z "$drive" ]; then
    echo '* You have to enter name of disk. Run as'
    echo '  ./flash.sh /dev/sdb'
    echo ' or whatever disk you have. Here is list of disks with potential filesystem info:'
    devices="$(ls -d /dev/sd? /dev/mmcblk? 2>/dev/null)"
    for device in $devices; do
        echo
        echo "- device $device"
        dd if=$device bs=1K count=1 status=none | strings
    done
    die
fi

drive_was_flashed=

yesno "Should I flash drive '$drive' ?" \
    && unzip -p $OS_NAME | dd of=$drive bs=1M status=progress conv=fsync \
    || : drive_was_flashed=yes

echo

#----------

function bootstrap_ssh_part1() {
    echo "* Please eject MicroSD card and insert it back. Press ENTER when done"
    read

    boot_drive="$(ls ${drive}* | uniq | sed -n 2p)"

    yesno "* Detected Raspbian /boot as '$boot_drive'. Continue?" \
        || exit 0

    umount "$boot_drive" || echo "Not yet mounted"

    if [[ -f /proc/partitions ]]
    then
        boot_drive=$(cat /proc/partitions | grep $(basename $boot_drive) \
                        | grep -E -o '\w:' | awk '{print tolower($0)}' | cut -d: -f1)
        boot_mount="/$boot_drive"
    else
        boot_mount=$(mktemp -d)
        mount "$boot_drive" $boot_mount
        echo "* Drive is mounted to $boot_mount"
    fi

    function cleanup() {
        echo "* Cleaning up..."
        sync
        umount "$boot_drive"
        rmdir "$boot_mount"
        echo "  ...done"
    }

    touch "$boot_mount/ssh"
    cp -rf config/secret/wpa_supplicant.conf "$boot_mount/"

    echo "* Bootstrap done! Insert MicroSD into Raspberry and boot it up."

    cleanup
}

if [ -n "$drive_was_flashed" ]; then
    bootstrap_ssh_part1
else
    yesno "Initialize WiFi/SSH?" \
        && bootstrap_ssh_part1
fi

