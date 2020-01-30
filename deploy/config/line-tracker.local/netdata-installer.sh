#!/usr/bin/env bash

sudo apt-get install netdata -y #installing netdata without asking for human permissions
IP=$(hostname -I | head -n1 | awk '{print $1;}') #getting RPI IP adress
echo your server located on "http://${IP}:19999" #Telling where sould go client to see netdata interface
