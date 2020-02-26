#!/usr/bin/env bash

#set -x
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REMOTE_USER=pi
REMOTE_HOST=line-tracker.local
REMOTE_IP=
VERBOSE=
PRINT_ONLY=
DETECT_ONLY=
SSH_ONLY=
ONLY_SCRIPT=
DEPLOY_TARGET=/home/pi
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=60 -o ServerAliveCountMax=9999999"
if [[ "$TERM" =~ kitty ]]; then
  export TERM=xterm-color
fi
function die() {
    [ -n "${1:-}" ] && echo "$1"
    # wait for [Enter] when running git-bash from WSL
    exit 1
}

function usage {
    echo "Usage: ./deploy.sh [--verbose] [--user <user>] [--ip <ip>] [<host>]"
    echo "  <host>      - host to deploy to. Can be mDNS address. Default - '$REMOTE_HOST'"
    echo "  --ip <ip>   - IP of remote host. Default is detected from <host>"
    echo "  --ssh       - just SSH to remote host"
    echo "  --only <script path>  - run single script"
    echo "  --print-ip  - print IP of remote host"
    echo "  --detect-ip - detect IPs of rpi devices around"
    echo "  --user      - remote user. Default -'$REMOTE_USER'"
    echo "  --verobse   - be verbose"
    echo "  --help      - show this help"
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
        --print-ip )
            PRINT_ONLY=yes
            ;;
        --detect-ip )
            DETECT_ONLY=yes
            ;;
        --ssh )
            SSH_ONLY=yes
            ;;
        --verbose )
            VERBOSE=y
            ;;
        --only )
            shift
            ONLY_SCRIPT="$1"
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
    local IP="${REMOTE_IP:-$1}"
    if [[ $IP =~ 192.* || $IP =~ fe80:: ]]; then
        echo $IP
    elif [[ $IP =~ .*\.local ]]; then
        if isWSL; then
            powershell.exe "Resolve-DnsName $IP" | grep '192' | awk '{print $5}'
        else
            avahi-resolve -4 -n $IP | awk '{print $2}'
        fi
    else
        echo $IP
    fi
}

[ -n "$PRINT_ONLY" ] && die "$(getIP $REMOTE_HOST)"
[ -n "$DETECT_ONLY" ] && {
   arp -n | awk '/b8:27/ {print $1}'
   exit 0
}

function copyStuff() {
    local RPIIP=$(getIP $1)
    [ -n "$VERBOSE" ] && : verbose="-v" || verbose=""
    rsync -e "ssh $SSH_OPTS" $verbose -a --delete --no-owner \
        $DIR/config/common.local \
        $DIR/config/$1 \
        $DIR/../src \
        $REMOTE_USER@$RPIIP:$DEPLOY_TARGET/config/
    #rsync -e "ssh $SSH_OPTS" $verbose -a --delete --no-owner $DIR/config/$1 $REMOTE_USER@$RPIIP:$DEPLOY_TARGET/config/
    #rsync -e "ssh $SSH_OPTS" $verbose -a --delete --no-owner $DIR/../src $REMOTE_USER@$RPIIP:$DEPLOY_TARGET/src
}

echo "checking connection..."
IP="$(getIP $REMOTE_HOST)"

if [ -n "$SSH_ONLY" ]; then
    type mosh >/dev/null && {
      mosh --ssh "ssh -oBatchMode=yes $SSH_OPTS" $REMOTE_USER@$IP || {
	    ssh-copy-id $SSH_OPTS $REMOTE_USER@$IP
        exec ssh $SSH_OPTS $REMOTE_USER@$IP
      }
      exit 0
    }
    ssh -oBatchMode=yes $SSH_OPTS $REMOTE_USER@$IP || {
	    ssh-copy-id $SSH_OPTS $REMOTE_USER@$IP
        exec ssh $SSH_OPTS $REMOTE_USER@$IP
    }
    exit 0
else
  ssh -oBatchMode=yes $SSH_OPTS $REMOTE_USER@$IP sh -c 'echo'|| die "Please copy your public SSH key to remote machine!"
fi

echo "Copying to $REMOTE_HOST..."
copyStuff $REMOTE_HOST

echo -e "\nRunning scripts..."
ssh $SSH_OPTS $REMOTE_USER@$IP '
  set -u
  REMOTE_HOST='$REMOTE_HOST'
  DEPLOY_TARGET='$DEPLOY_TARGET'
  failed=()
  RED='"'"'\033[0;31m'"'"'
  GREEN='"'"'\033[0;32m'"'"'
  NC='"'"'\033[0m'"'"'
  for dep in common.local $REMOTE_HOST; do
      cd $DEPLOY_TARGET/config/$dep
      for script in '${ONLY_SCRIPT:-'$(ls -d *.sh)'}'; do
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
  done
  echo
  echo "------------"
  if [[ -n "${failed[@]}" ]]; then
    printf "${RED}Scripts failed${NC}:\n"
    echo "${failed[@]}"
  fi
'
