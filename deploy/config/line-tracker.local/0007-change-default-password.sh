#!/usr/bin/env bash

sudo sed -i 's/#PasswordAuthentication .*/PasswordAuthentication no/g' /etc/ssh/sshd_config     #changing variable which responsible for ssh password authentication