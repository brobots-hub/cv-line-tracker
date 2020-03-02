#! /usr/bin/env bash

sudo cp -rf etc/avahi-daemon.conf /etc/avahi/avahi-daemon.conf
sudo systemctl restart avahi-daemon.service

export NAME=line-tracker
echo $NAME | sudo tee /etc/hostname
sudo hostname $NAME
sudo sed -i "s/raspberrypi/$NAME/g" /etc/hosts
