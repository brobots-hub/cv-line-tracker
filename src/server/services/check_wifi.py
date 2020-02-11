import subprocess


def check_wifi():
    rc = subprocess.run(['./server/services/wifi_strength.sh'],
                        stdout=subprocess.PIPE)

    return rc.stdout
