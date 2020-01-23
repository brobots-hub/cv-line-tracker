#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REMOTE_USER=pi
REMOTE_HOST=line-tracker.local
REMOTE_IP=
VERBOSE=

function usage {
    echo "Usage: ./deploy.sh [--verbose] [--user <user>] [--ip <ip>] [<host>]"
    echo "  <host>   - host to deploy to. Can be mDNS address. Default - '$REMOTE_HOST'"
    echo "  --ip     - IP of remote host. Default is detected from <host>"
    echo "  --user   - remote user. Default -'$REMOTE_USER'"
    echo "  --verobse- be verbose"
    echo "  --help   - show this help"
}

while [ "$1" != "" ]; do
    case $1 in
        --user )
            shift
            REMOTE_USER="$1"
            ;;
        --ip )
            shift
            REMOTE_IP="$1"
            ;;
        --verbose )
            VERBOSE=y
            ;;
        -h | --help )
            usage
            exit
            ;;
        * )
            REMOTE_HOST="$1"
            ;;
    esac
    shift
done

[ ! -d "$DIR/config/$REMOTE_HOST" ] && echo "Host $REMOTE_HOST has no configuration files" && exit 1

set -u

function isWSL() {
    uname -a | grep -q Microsoft
}

function getIP() {
    if [ -n "$REMOTE_IP" ]; then
        echo $REMOTE_IP
    elif [[ $1 =~ 192.* ]]; then
        echo $1
    elif [[ $1 =~ .*\.local ]]; then
        if isWSL; then
            powershell.exe "Resolve-DnsName $1" | grep '192' | awk '{print $5}'
        else
            avahi-resolve -n $1 | cut -d\  -f1
        fi
    else
        echo $1
    fi
}

function copyStuff() {
    local RPIIP=$(getIP $1)
    [ -n "$VERBOSE" ] && : verbose="-v" || verbose=""
    rsync $verbose -a --no-owner $DIR/config/$1 $REMOTE_USER@$RPIIP:config
    rsync $verbose -a --no-owner $DIR/../src $REMOTE_USER@$RPIIP:src
}

echo "Copying to $REMOTE_HOST..."
copyStuff $REMOTE_HOST
ssh $REMOTE_USER@$(getIP $REMOTE_HOST) '
  set -u
  failed=()
  RED='"'"'\033[0;31m'"'"'
  GREEN='"'"'\033[0;32m'"'"'
  NC='"'"'\033[0m'"'"'
  cd ~/config/'$REMOTE_HOST'
  for script in $(ls -d *.sh); do
    echo
    echo -e "* ${GREEN}Running $script${NC}..."
    echo
    if stdbuf -oL bash $script ; then
        :
    else
        echo -e "${RED}failed${NC}"
        failed+=( "$script" )
    fi
    sleep 0.1 # stderr can mix with stdout without this
  done
  echo
  echo "------------"
  if [[ -n "${failed[@]}" ]]; then
    printf "${RED}Scripts failed${NC}:\n"
    echo "${failed[@]}"
  fi
'