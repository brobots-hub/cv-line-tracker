#!/usr/bin/env bash

if grep -q "arm_64bit=1" /boot/config.txt
then
    echo "Already using 64-bit kernel"
    exit
else
    echo "arm_64bit=1" | sudo tee -a /boot/config.txt 
    echo "Switched to 64-bit kernel"
fi
