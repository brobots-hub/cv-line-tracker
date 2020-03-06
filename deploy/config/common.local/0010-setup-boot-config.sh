sudo cp -f etc/boot_config.txt /boot/config.txt

# make it performant
sudo sed -i 's/"ondemand"/"performance"/g' /etc/init.d/raspi-config
