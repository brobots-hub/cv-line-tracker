function yesno() {
    local prompt="${1:-'[Y]es/[N]o?'}"
    read -p "$prompt" -n 1 -r && echo
    [[ $REPLY =~ ^[Yy]$ ]] && return 0 || return 1
}

echo "Do you want to reboot? (recommended)"
yesno && sudo reboot || :
