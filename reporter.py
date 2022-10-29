
import os
from sys import argv
import time
from datetime import datetime
from configparser import ConfigParser

from psutil import Process

import board
import busio
import adafruit_ssd1306

#import psutil

from PIL import Image, ImageDraw, ImageFont

start_time = datetime.now()

def get_cpu_temp():
    raw_temp = os.popen("vcgencmd measure_temp").readline()
    return raw_temp.replace("temp=","").replace("'C\n","")


def get_cpu_load_top():
    return(str(os.popen("top -b -n1 | grep -Po '[0-9.]+ id' | awk '{print 100-$1}'").readline().strip()))


def get_cpu_load_mpstat():
    return(str(os.popen("mpstat | tail -1 | awk '{print 100-$NF}'").readline().strip()))


def get_ram_usage():
    #return(str(round(psutil.Process(os.getpid()).memory_info()[0] /2.**30, 2)))
    # (tot_m, used_m, free_m) = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    # return "{:0.2f}".format(used_m / tot_m)
    p = psutil.Process()
    rss = p.memory_info().rss / 2 ** 20 # Bytes to MB
    return "{rss: 10.5f}"


def get_total_time():
    duration = datetime.now() - start_time
    sec = duration.total_seconds()
    hour = sec // 3600
    min = sec % 3600 // 60
    sec = sec % 60
    return('{:02}:{:02}:{:02}'.format(int(hour), int(min), int(sec)))

# Raspberry Pi pin configuration:
RST = 25
# Note the following are only used with SPI:
DC = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
i2c = busio.I2C(board.SCL, board.SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize library.
disp.fill(0)
disp.show()

config = ConfigParser()
cpu_temp = ""
cpu_load = ""
ram_usage = ""
uptime = ""
language = ""
if len(argv) < 1:
    language = "english"
else:
    language = argv[1].lower()
if language == "korean" or language == "ko":
    language = "korean"
elif language == "english" or language == "en":
    language = "english"

cpu_temp = config[language]["cpu_temp"]
cpu_load = config[language]["cpu_load"]
ram_usage = config[language]["ram_usage"]
uptime = config[language]["uptime"]

while(True):
    image = Image.new('1', (128, 64))
    font = ImageFont.truetype('NanumBarunGothicBold.ttf', size=12)
    draw = ImageDraw.Draw(image)

    text = cpu_temp + ': ' + get_cpu_temp() + '\'C\n' + \
        cpu_load + ': ' + get_cpu_load_top() + '%\n' + \
        ram_usage + ': ' + get_ram_usage() + '%\n' + \
        uptime + ': ' + get_total_time()
    draw.text(
        (4, 2),
        text,
        font=font,
        fill=255,
    )
    disp.image(image)
    disp.show()
    time.sleep(1)
