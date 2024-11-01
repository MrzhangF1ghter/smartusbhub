from smartusbhub import SmartUSBHub, ON, OFF
import time
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Smart USB Hub control program")
parser.add_argument("-p", "--port", help="Specify serial port, e.g., /dev/ttyUSB0")
args = parser.parse_args()

# Initialize SmartUSBHub instance
hub = SmartUSBHub(port=args.port)

if hub.ser is None:
    print("[ERROR] Could not connect to the device. Please check the connection and try again.")
else:
    # Retrieve current device mode
    current_mode = hub.get_mode()
    print(f"Current mode: {current_mode}")

    # Set device to normal mode
    hub.set_mode(0)  # 0 indicates normal mode; 1 indicates interlock mode
    print("Switched to normal mode")

    # Loop to toggle each channel ON and OFF with a delay
    channels = [1, 2, 3, 4]
    while True:
        for i in range(3):  # Repeat the toggle sequence 3 times for each channel
            for channel in channels:
                status = hub.get_channel_status(channel)
                flag = not status
                hub.control_channel(flag, channel)
                status = hub.get_channel_status(channel)
                print(f"Channel status after toggling: {status}")
                time.sleep(0.01)  # Delay to observe the channel being turned ON
    # Retrieve and display channel status after toggling
    status = hub.get_channel_status(1, 2, 3, 4)


    # Close the connection
    hub.close()