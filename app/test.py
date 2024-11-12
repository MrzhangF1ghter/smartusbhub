import sys
sys.path.append('./..')
sys.path.append('../')
from smartusbhub import *
import time
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Smart USB Hub control program")
parser.add_argument("-p", "--port", help="Specify serial port, e.g., /dev/ttyUSB0")
args = parser.parse_args()

# Initialize SmartUSBHub instance
hub = SmartUSBHub(port=args.port)

delay_interval = 1
channels = [1, 2, 3, 4]

if hub.ser is None:
    print("[ERROR] Could not connect to the device. Please check the connection and try again.")
else:
    while True:
        # Retrieve current device mode
        current_mode = hub.get_mode()
        print(f"device mode: {'normal' if current_mode == MODE_NORMAL else 'interlock'}")
        # Set device to normal mode
        if(current_mode!=MODE_NORMAL):
            hub.set_mode_normal()

        # Loop to toggle each channel ON and OFF with a delay
        for channel in channels:
            #control channel
            hub.control_channel(ON, channel)
            print(f"Turn on  Channel {channel}")
            #get current channel status
            status = hub.get_channel_status(channel)
            print(f"Channel {channel} is {'on' if status == 1 else 'off'}")

            time.sleep(delay_interval)

            hub.control_channel(OFF, channel)
            print(f"Turn off Channel {channel}")

            status = hub.get_channel_status(channel)
            print(f"Channel {channel} is {'on' if status == 1 else 'off'}")

            time.sleep(delay_interval)

        # multi channel control
        hub.control_channel(ON,1,3)
        print("Turn on  Channel 1 and 3")
        #get channel status
        status = hub.get_channel_status(1)
        print(f"Channel 1 is {'ON' if status == ON else 'OFF'}")
        status = hub.get_channel_status(3)
        print(f"Channel 3 is {'ON' if status == ON else 'OFF'}")
        time.sleep(delay_interval)

        hub.control_channel(OFF,1,3)
        print("Turn off Channel 1 and 3")
        #get channel status
        status = hub.get_channel_status(1)
        print(f"Channel 1 is {'ON' if status == ON else 'OFF'}")
        status = hub.get_channel_status(3)
        print(f"Channel 3 is {'ON' if status == ON else 'OFF'}")
        time.sleep(delay_interval)

        hub.control_channel(ON,2,4)
        print("Turn on  Channel 2 and 4")
        #get channel status
        status = hub.get_channel_status(2)
        print(f"Channel 2 is {'ON' if status == ON else 'OFF'}")
        status = hub.get_channel_status(4)
        print(f"Channel 4 is {'ON' if status == ON else 'OFF'}")
        time.sleep(delay_interval)

        hub.control_channel(OFF,2,4)
        print("Turn off Channel 2 and 4")
        #get channel status
        status = hub.get_channel_status(2)
        print(f"Channel 2 is {'ON' if status == ON else 'OFF'}")
        status = hub.get_channel_status(4)
        print(f"Channel 4 is {'ON' if status == ON else 'OFF'}")
        time.sleep(delay_interval)

        #turn on channels
        for channel in channels:
            #control channel
            hub.control_channel(ON, channel)
            print(f"Turn on  Channel {channel}")
            #get current channel status
            status = hub.get_channel_status(channel)
            print(f"Channel {channel} is {'on' if status == 1 else 'off'}")
            time.sleep(delay_interval)
        
        # # Set device to interlock mode
        # current_mode = hub.get_mode()
        # print(f"device mode: {'normal' if current_mode == MODE_NORMAL else 'interlock'}")
        # if(current_mode!=MODE_INTERLOCK):
        #     hub.set_mode_interlock()
    
        for channel in channels:
            #control channel
            hub.interlock_control(ON,channel)
            print(f"Turn on  Channel {channel}")
            #get current channel status
            status = hub.get_channel_status(channel)
            print(f"Channel {channel} is {'on' if status == 1 else 'off'}")
            time.sleep(delay_interval)

        hub.interlock_control_all_off()

    # Close the connection
    hub.close()