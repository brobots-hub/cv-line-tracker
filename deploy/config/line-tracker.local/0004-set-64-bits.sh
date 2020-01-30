#!/usr/bin/env bash

if grep "arm_64bit=1" /boot/config.txt
then
    exit
else
    echo "arm_64bit=1" | sudo tee -a /boot/config.txt 
fi
exit