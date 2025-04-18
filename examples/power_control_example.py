# Description: control the power of each channel of the SmartUSBHub
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
    hub_list = SmartUSBHub.scan_available_ports()# Scan all available ports
    print("available device:", hub_list)

    hub = SmartUSBHub.scan_and_connect()# Scan and connect to the first SmartUSBHub found
    # hub = SmartUSBHub("/dev/cu.usbmodem132301") # Connect to a specific SmartUSBHub device
    if hub is None:
        print("No SmartUSBHub found")
        sys.exit(1)

    device_info = hub.get_device_info()
    print("device info:", device_info)

    interval = 0.1

    while True:
        print("\ncontrol channel power one by one:")

        print("turn on channels 1")
        hub.set_channel_power(1, state=1)
        time.sleep(interval)

        print("turn on channels 2")
        hub.set_channel_power(2, state=1)
        time.sleep(interval)

        print("turn on channels 3")
        hub.set_channel_power(3, state=1)
        time.sleep(interval)

        print("turn on channels 4")
        hub.set_channel_power(4, state=1)
        time.sleep(interval) 

        print("turn off channels 1")
        hub.set_channel_power(1, state=0)
        time.sleep(interval)

        print("turn off channels 2")
        hub.set_channel_power(2, state=0)
        time.sleep(interval)

        print("turn off channels 3")
        hub.set_channel_power(3, state=0)
        time.sleep(interval)

        print("turn off channels 4")
        hub.set_channel_power(4, state=0)
        time.sleep(interval)
        
        print("\ncontrol multi channel power at once:")
        print("turn on channels 1,3")
        hub.set_channel_power(1, 3, state=1)
        time.sleep(interval)

        print("turn off channels 1,3")
        hub.set_channel_power(1, 3, state=0)
        time.sleep(interval)


        print("\ncontrol channel power one by one with status check:")
        state = 1
        for i in range(1, 5):
            print(f"turn on channel", i)
            hub.set_channel_power(i, state=1)
            if hub.get_channel_power_status(i) == 1:
                print(f"channel {i} is on")
            else:
                print(f"channel {i} still off")
                raise Exception(f"channel {i} still off")
            time.sleep(interval)

        for i in range(1, 5):
            print(f"turn on channel", i)
            hub.set_channel_power(i, state=0)
            if hub.get_channel_power_status(i) == 0:
                print(f"channel {i} is off")
            else:
                print(f"channel {i} still on")
                raise Exception(f"channel {i} still on")
            time.sleep(interval)

        print("\ncontrol multi channel power at once with status check:")
        state = 1
        for i in (1,2):
            
            hub.set_channel_power(1, 3, state=state)
            channel_status = hub.get_channel_power_status(1, 3)
            if channel_status is not None:
                if (channel_status.get(1) == state) and (channel_status.get(3) == state):
                    print(f"channel 1,3 are {'on' if state == 1 else 'off'}")
                else:
                    print(f"Failed to set channel status. Current channel status: {channel_status}")
                    raise Exception(f"Failed to set channel 1,3 to {'on' if state == 1 else 'off'}")
            else:
                print(f"Failed to set channel status. Current channel status: {channel_status}")
                raise Exception("Failed to get channel status")
            # Toggle state
            state = 0 if state == 1 else 1
            time.sleep(interval)

        # interlock control
        print("interlock power control")
        start_time = time.time()
        while time.time() - start_time < 5:
            for i in range(1, 5):
                hub.set_channel_power_interlock(i)
                print("interlock control,turn on channel", i)
                time.sleep(0.5)
        hub.set_channel_power_interlock(None)
        
if __name__ == "__main__":
    main()
