
import os
import time
from datetime import datetime

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
    (tot_m, used_m, free_m) = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    return "{:0.2f}".format(used_m / tot_m)


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


while(True):
    image = Image.new('1', (128, 64))
    font = ImageFont.truetype('NanumBarunGothicBold.ttf', size=12)
    draw = ImageDraw.Draw(image)

    text = 'CPU 온도: ' + get_cpu_temp() + '\'C\n' + \
        'CPU 로드: ' + get_cpu_load_top() + '%\n' + \
        '메모리 사용량: ' + get_ram_usage() + '%\n' + \
        '가동 시간: ' + get_total_time()
    draw.text(
        (4, 2),
        text,
        font=font,
        fill=255,
    )
    disp.image(image)
    disp.show()
    time.sleep(1)
