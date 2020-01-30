#!/usr/bin/env bash

sudo sed -i "s/start_x=0/start_x=1/g" /boot/config.txt
echo "* Camera is activated"
