#!/usr/bin/env bash

if grep -q "CONF_SWAPSIZE=1024" /etc/dphys-swapfile
then
    echo "Already using 1GB swap"
    exit
else
    sudo sed -i "s/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=1024/g" /etc/dphys-swapfile
    echo "Moved to 1GB swap size"
fi
