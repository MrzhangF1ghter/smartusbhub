from smartusbhub import SmartUSBHub
import time
import sys
import os

def main():
    # 尝试扫描并连接到 Smart USB Hub 设备
    hub = SmartUSBHub.scan_and_connect()
    
    if hub:
        print(f"Connected to {hub.name}")
        # get firmware version
        firmware_version = hub.get_firmware_version()
        print(f"firmware_version: {firmware_version}")

        # get hardware version
        hardware_version = hub.get_hardware_version()
        print(f"hardware_version: {hardware_version}")
        
        # get operation mode
        operation_mode = hub.get_operate_mode()
        print(f"operation_mode: {operation_mode}")

        # get button status
        button_status = hub.get_button_control()
        print(f"button_status: {button_status}")

        try:
            while True:
                
                # power_status = hub.get_channel_power_status(1,2,3,4)
                # if power_status:
                #     print(f"power_status ch1: {power_status.get(1)}, ch2: {power_status.get(2)}, ch3: {power_status.get(3)}, ch4: {power_status.get(4)}")

                # # Flip the power state of each channel
                # if power_status:
                #     for ch in range(1, 5):
                #         current_state = power_status.get(ch, 0)
                #         new_state = 0 if current_state else 1
                #         hub.set_channel_power_status(ch, state=new_state)
                #         if hub.debug:
                #             print(f"Set channel {ch} to {'ON' if new_state else 'OFF'}")

                # dataline_status = hub.get_channel_dataline_status(1,2,3,4)
                # if dataline_status:
                #     print(f"dataline_status ch1: {dataline_status.get(1)}, ch2: {dataline_status.get(2)}, ch3: {dataline_status.get(3)}, ch4: {dataline_status.get(4)}")
                # else:
                #     print("dataline_status is None")

                voltage_readings = {}
                for ch in [1, 2, 3, 4]:
                    reading = hub.get_channel_voltage(ch)
                    # reading 可能是 None，需做相应判断
                    voltage_readings[ch] = reading

                # print("Voltage readings:")
                # for ch, val in voltage_readings.items():
                #     print(f"  ch{ch}: {val}")
                
                current_readings = {}
                for ch in [1, 2, 3, 4]:
                    reading = hub.get_channel_current(ch)
                    current_readings[ch] = reading

                # print("Current readings:")
                # for ch, val in current_readings.items():
                #     print(f"  ch{ch}: {val}")


                time.sleep(0.01)

        except KeyboardInterrupt:
            print("Exiting program...")
            hub.disconnect()

    else:
        print("No Smart USB Hub found.")

if __name__ == "__main__":
    main()