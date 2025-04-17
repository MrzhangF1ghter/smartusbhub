# Description: basic settings and info of the SmartUSBHub
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
    
    print("Enable default power status on specific channels, and set power default to ON")
    hub.set_default_power_status(1,2,3,4,enable=1,status=1)
    default_power_status = hub.get_default_power_status(1,2,3,4)
    if default_power_status:
        for ch, info in default_power_status.items():
            print(f"Channel {ch} default power status is {'enable' if info['enabled'] else 'disable'}, default power is {'ON' if info['value'] else 'OFF'}")
    else:
        print("Failed to get default power status")

    print("Disable default power status on specific channels")
    hub.set_default_power_status(1,2,3,4,enable=0)
    default_power_status = hub.get_default_power_status(1,2,3,4)
    if default_power_status:
        for ch, info in default_power_status.items():
            print(f"Channel {ch} default power status is {'enable' if info['enabled'] else 'disable'}, default power is {'ON' if info['value'] else 'OFF'}")
    else:
        print("Failed to get default power status")

    print("Enable default dataline status on specific channels, and set dataline default to Disconnect")
    hub.set_default_dataline_status(1,2,3,4,enable=1,status=0)
    default_dataline_status = hub.get_default_dataline_status(1,2,3,4)
    if default_dataline_status:
        for ch, info in default_dataline_status.items():
            print(f"Channel {ch} default dataline status is {'enable' if info['enabled'] else 'disable'}, default dataline is {'Connect' if info['value'] else 'Disconnect'}")
    else:
        print("Failed to get default dataline status")

    print("Disable default dataline status on specific channels")
    hub.set_default_dataline_status(1,2,3,4,enable=0)
    default_dataline_status = hub.get_default_dataline_status(1,2,3,4)
    if default_dataline_status:
        for ch, info in default_dataline_status.items():
            print(f"Channel {ch} default dataline status is {'enable' if info['enabled'] else 'disable'}, default dataline is {'Connect' if info['value'] else 'Disconnect'}")
    else:
        print("Failed to get default dataline status")
        
    # print("set operate mode to interlock mode")
    # hub.set_operate_mode(1)
    # mode = hub.get_operate_mode()
    # if mode!=1 :
    #     print("set operate mode to interlock mode failed")
    # print("operate mode is interlock mode")
    # #print now you can ONLY control one channel power on at a time using set_channel_power_interlock
    # time.sleep(3)
    # print("change operate mode to normal mode")
    # hub.set_operate_mode(0)
    # mode = hub.get_operate_mode()
    # if mode!=0 :
    #     print("set operate mode to normal mode failed")
    # print("operate mode is normal mode")
    # #print now you can control multi channel power on at a time using set_channel_power
    # time.sleep(3)

    # # disable button control
    # print("\ndisable button control:")
    # hub.set_button_control(0)
    # button_control_status = hub.get_button_control_status()
    # print("button control status:", button_control_status)
    # print(("button control disabled,now you can't control the hub by button"))
    # time.sleep(3)
    # print("enable button control again:")
    # hub.set_button_control(1)
    # button_control_status = hub.get_button_control_status()
    # print("button control status:", button_control_status)
    # print("button control enabled,now you can control the hub by button")

    print("example finished")
    sys.exit(0)
    

if __name__ == "__main__":
    main()
