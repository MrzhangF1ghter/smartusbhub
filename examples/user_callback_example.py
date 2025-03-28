# Description: user callback example of the SmartUSBHub
# copyright: (c) 2024 EmbeddedTec studio
# license: Apache-2.0
# version: 1.0
# author: EmbeddedTec studio
# email:embeddedtec@outlook.com

import sys
import time
sys.path.append('../')
from smartusbhub import *

def button_press_callback(channel, status):
    print("Button press detected on channel", channel, "with power status", status)

def main():
    hub = SmartUSBHub.scan_and_connect()# Scan and connect to the first SmartUSBHub found
    # hub = SmartUSBHub("/dev/cu.usbmodem132301") # Connect to a specific SmartUSBHub device
    if hub is None:
        print("No SmartUSBHub found")
        sys.exit(1)

    #register a callback function to handle the button press event
    hub.register_callback(CMD_GET_CHANNEL_POWER_STATUS, button_press_callback)
    while True:
        time.sleep(0.1)

if __name__ == "__main__":
    main()

