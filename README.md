# Status Reporter for Raspberry Pi 4 with I2C 1306 OLED

A script for printing performance status(e.g. CPU load, RAM usage, etc.) of Raspberry Pi 4 with I2C 1306 OLED.

## What Kind of Status are Reported?

- CPU temperature.
- CPU load.
- RAM usage.
- Total running time.

## Language Support

- Korean
- English

## Device Support

- Only Raspberry Pi 4 Model.

You can edit the install scripts for other devices, but I have only tested the RP4 model and cannot guarantee proper execution.

## How to Install

- Ubuntu, Raspberry Pi OS or something else using apt. 

#### Connecting Pins

VCC -> GPIO 1

SDL -> GPIO 3

SCL -> GPIO 5

GND -> GPIO 9

If you have connected other pins, you must edit I2C address in `reporter.py`. 

#### Script

```bash
sudo apt install git
cd ~
git clone https://github.com/altair823/reporter.git
cd reporter
```
If you want to start this script as soon as the device starts up and using `setup.sh` to setup automatically, you must clone whole repository to the `~` directory, which is `/home/pi` in Raspberry Pi. 

After closing other programs so that you can reboot, run `setup.sh`
```bash
./setup.sh
```
or
```bash
./setup.sh english
```

If you want to setup a korean script, type this command instead. 
```bash
./setup.sh korean
```

This will cause reboot the device. After that, the 1306 OLED display print status of RP4.

If you want to clone this repository to another directory and install it using `setup.sh`, you need to edit paths in `reporter_service_{language}.service`.