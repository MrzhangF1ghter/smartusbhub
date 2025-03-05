from smartusbhub import SmartUSBHub
import time

def main():
    # 尝试扫描并连接到 Smart USB Hub 设备
    hub = SmartUSBHub.scan_and_connect()
    
    if hub:
        print(f"Connected to {hub.name}")
        while True:
            power_status = hub.get_channel_power_status(1,2,3,4)
            if power_status:
                print(f"power_status ch1: {power_status.get(1)}, ch2: {power_status.get(2)}, ch3: {power_status.get(3)}, ch4: {power_status.get(4)}")

            # Flip the power state of each channel
            if power_status:
                for ch in range(1, 5):
                    current_state = power_status.get(ch, 0)
                    new_state = 0 if current_state else 1
                    hub.set_channel_power(ch, state=new_state)
                    if hub.debug:
                        print(f"Set channel {ch} to {'ON' if new_state else 'OFF'}")

            time.sleep(0.01)
    else:
        print("No Smart USB Hub found.")

if __name__ == "__main__":
    main()