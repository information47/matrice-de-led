#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
import requests
import json

def demo(n, block_orientation, rotate, inreverse):
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=n, block_orientation=block_orientation,
                     rotate=rotate, blocks_arranged_in_reverse_order=inreverse)
    print("Created device")
    
    i=0
    while i==0 :
        url = "https://api.openweathermap.org/data/2.5/weather?q=Gattieres&appid=f3e02c2c8f957149e700509a7af8b267&units=metric&lang=fr"
        meteoResponse = requests.get(url)
        data = json.loads(meteoResponse.text)
        
        temp = data['main']['temp']
        displayTemp = str(temp)

        weather = data['weather']['description']
        displayWeather = str(weather)

        j = 0
        while j < 5 :
            with canvas(device) as draw:
                text(draw, (0, 0), displayTemp, fill="white", font=proportional(SINCLAIR_FONT))
            time.sleep(3)

            
            show_message(device, displayWeather, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)
            j = j+1






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=4, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=-90, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=2, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')

    args = parser.parse_args()

    try:
        demo(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
    except KeyboardInterrupt:
        pass
