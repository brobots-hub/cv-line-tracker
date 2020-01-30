#!/usr/bin/env bash

bash <(curl -Ss https://my-netdata.io/kickstart.sh) --dont-wait #installing netdata without asking for human permissions
IP=$(hostname -I | head -n1 | awk '{print $1;}') #getting RPI IP adress
echo your server located on "http://${IP}:19999" #Telling where sould go client to see netdata interface