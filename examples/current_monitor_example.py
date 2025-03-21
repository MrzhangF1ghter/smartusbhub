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
        current = []
        for i in range(1, 5):
            voltage = hub.get_channel_current(i)
            if voltage is not None:
                current.append(f"{voltage / 1000.0:.2f} A")
            else:
                current.append("N/A")
        print(" | ".join([f"Channel {i}: {a}" for i, a in enumerate(current, start=1)]))
        time.sleep(0.01)


if __name__ == "__main__":
    main()