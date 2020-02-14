#!/usr/bin/env bash

if grep -q "start_x" /boot/config.txt
then
    sudo sed -i "s/start_x=0/start_x=1/g" /boot/config.txt
else
    echo -en "start_x=1\ngpu_mem=128" | sudo tee -a /boot/config.txt
fi
echo "* Camera is activated"
