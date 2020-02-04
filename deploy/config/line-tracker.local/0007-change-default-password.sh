#!/usr/bin/env bash
sudo sed -i 's/#PasswordAuthentication yes/#PasswordAuthentication no/g' /etc/ssh/sshd_config     #changing variable which responsile for ssh password authentication