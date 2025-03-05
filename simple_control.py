from smartusbhub import SmartUSBHub
import time

def main():
    # 尝试扫描并连接到 Smart USB Hub 设备
    hub = SmartUSBHub.scan_and_connect()
    
    if hub:
        print(f"Connected to {hub.name}")
        while True:
            hub.set_channel_power(1,2,3,4, state=1)
            time.sleep(0.5)
            hub.set_channel_power(1,2,3,4, state=0)
            time.sleep(0.5)
    else:
        print("No Smart USB Hub found.")

if __name__ == "__main__":
    main()