# Description: control the dataline of each channel of the SmartUSBHub
# copyright: (c) 2024 EmbeddedTec studio
# license: Apache-2.0
# version: 1.0
# author: EmbeddedTec studio
# email:embeddedtec@outlook.com

import sys
import time
sys.path.append('../')
from smartusbhub import SmartUSBHub

def main():
    hub = SmartUSBHub.scan_and_connect()# Scan and connect to the first SmartUSBHub found
    # hub = SmartUSBHub("/dev/cu.usbmodem132301") # Connect to a specific SmartUSBHub device
    if hub is None:
        print("No SmartUSBHub found")
        sys.exit(1)

    device_info = hub.get_device_info()
    print("device info:", device_info)

    while True:
        # control channel data line
        print("\ndisconnect channel's data but keep power on:")
        if hub.get_channel_power_status(1) == 0:
            print("channel 1 power is off,turn on first")
            hub.set_channel_power(1, state=1)
            if(hub.get_channel_power_status(1) == 0):
                print("channel 1 power is still off")
                sys.exit(1)
        
        result = hub.set_channel_dataline(1,state=0)   
        if result:
            print("now channel 1 power is on and data is disconnected")
        else:
            print("channel 1 dataline disconnect failed")

        time.sleep(3)
        print("connect channel 1's data again")   
        result = hub.set_channel_dataline(1,state=1) 
        if result:
            print("channel 1 dataline connected")
        else:
            print("channel 1 dataline connect failed")
        
        # control multi channel data line
        print("disconnect multi channel's data but keep power on:")
        if hub.get_channel_power_status(1,3) == 0:
            print("channel 1,3 power is off,turn on first")
            hub.set_channel_power(1,3, state=1)
            if(hub.get_channel_power_status(1,3) == 0):
                print("channel 1,3 power is still off")
                sys.exit(1)
        
        result = hub.set_channel_dataline(1,3,state=0)   
        if result:
            print("now channel 1,3 power is on and data is disconnected")
        else:
            print("channel 1,3 dataline disconnect failed")

        time.sleep(3)
        print("connect channel 1,3's data again")   
        result = hub.set_channel_dataline(1,3,state=1) 
        if result:
            print("channel 1,3 dataline connected")
        else:
            print("channel 1,3 dataline connect failed")


if __name__ == "__main__":
    main()