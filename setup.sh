#!/usr/bin/bash

if cat /proc/cpuinfo | grep "Model" | head -1  | grep -q "Model		: Raspberry Pi 4";
then
sudo raspi-config nonint do_i2c 0
sudo apt install pip -y
sudo apt install libopenjp2-7 -y
sudo apt install i2c-tools -y
sudo pip3 install pillow
sudo pip3 install adafruit-circuitpython-ssd1306
sudo pip3 install Adafruit-Blinka
sudo mv reporter_service.service /etc/systemd/system/reporter_service.service
sudo chmod 775 /etc/systemd/system/reporter_service.service
sudo systemctl daemon-reload
sudo systemctl enable reporter_service.service
else
echo "This shell script only supports Raspberry Pi 4."
fi


