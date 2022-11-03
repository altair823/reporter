
import os
from sys import argv
import time
from datetime import datetime
from configparser import ConfigParser

from psutil import Process

import board
import busio
import adafruit_ssd1306

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
    p = Process()
    rss = p.memory_info().rss / 2 ** 20
    return "{:0.1f}".format(rss)


def get_total_time():
    duration = datetime.now() - start_time
    sec = duration.total_seconds()
    hour = sec // 3600
    min = sec % 3600 // 60
    sec = sec % 60
    return('{:02}:{:02}:{:02}'.format(int(hour), int(min), int(sec)))

# 128x64 display with hardware I2C:
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

display.fill(0)
display.show()

config = ConfigParser()
config.read('languages.conf')
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
    display.image(image)
    display.show()
    time.sleep(1)
