from smartusbhub import SmartUSBHub
import time
import sys

def main():
    hub = SmartUSBHub.scan_and_connect() # Scan and connect to the first SmartUSBHub found
    if hub is None:
        print("No SmartUSBHub found")
        sys.exit(1)
    print("SmartUSBHub found")
    
# control channel power one bye one
    print("\ncontrol channel power one by one:")
    for i in range(1, 5):
        print("turn on channel", i)
        hub.set_channel_power(i, state=1)
        if(hub.get_channel_power_status(i)):
            print("channel", i, "is on")
        else:
            print("channel", i, "still off")
            sys.exit(1)
        time.sleep(0.5)
        print("turn off channel", i)
        hub.set_channel_power(i, state=0)
        if(hub.get_channel_power_status(i)==0):
            print("channel", i, "is off")
        else:
            print("channel", i, "still on")
            sys.exit(1)
        time.sleep(0.5)
    

# control multi channel power at once @TODO: need to fix,don't use now!
    # print("control multi channel power at once:")
    # while True:
    #     print("turn on channel 1,3")
    #     hub.set_channel_power(1,3, state=1)
    #     channel_status = hub.get_channel_power_status(1,3)
    #     if channel_status is not None:
    #         if channel_status.get(1) and channel_status.get(3):
    #             print("channel 1,3 are on")
    #         else:
    #             if channel_status.get(1) is 0:
    #                 print("channel 1 still off")
    #             if channel_status.get(3) is 0:
    #                 print("channel 3 still off")
    #             sys.exit(1)
    #     else:
    #         print("Failed to get channel status")
    #         sys.exit(1)

    #     time.sleep(1)

    #     print("turn off channel 1,3:")
    #     hub.set_channel_power(1,3, state=0)
    #     channel_status = hub.get_channel_power_status(1,3)
    #     if channel_status is not None:
    #         if channel_status.get(1) is 0 and channel_status.get(3) is 0:
    #             print("channel 1,3 are off")
    #         else:
    #             if channel_status.get(1) == 1:
    #                 print("channel 1 still on")
    #             if channel_status.get(3) == 1:
    #                 print("channel 3 still on")
    #             sys.exit(1)
    #     else:
    #         print("Failed to get channel status")
    #         sys.exit(1)

    #     time.sleep(1)

# interlock control
    print("interlock power control")
    start_time = time.time()
    while time.time() - start_time < 5:
        for i in range(1, 5):
            hub.set_channel_power_interlock(i)
            print("interlock control,turn on channel", i)
            time.sleep(0.5)
    hub.set_channel_power_interlock(None)

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

# control multi channel data line @TODO: need to fix,don't use now!
    # print("disconnect multi channel's data but keep power on:")
    # if hub.get_channel_power_status(1,3) == 0:
    #     print("channel 1,3 power is off,turn on first")
    #     hub.set_channel_power(1,3, state=1)
    #     if(hub.get_channel_power_status(1,3) == 0):
    #         print("channel 1,3 power is still off")
    #         sys.exit(1)
    
    # result = hub.set_channel_dataline(1,3,state=0)   
    # if result:
    #     print("now channel 1,3 power is on and data is disconnected")
    # else:
    #     print("channel 1,3 dataline disconnect failed")

    # time.sleep(3)
    # print("connect channel 1,3's data again")   
    # result = hub.set_channel_dataline(1,3,state=1) 
    # if result:
    #     print("channel 1,3 dataline connected")
    # else:
    #     print("channel 1,3 dataline connect failed")

# get channel voltage
    print("\nget channel voltage:")
    start_time = time.time()
    while time.time() - start_time < 5:
        for i in range(1, 5):
            voltage = hub.get_channel_voltage(i)
            if voltage is not None:
                print(f"channel {i} voltage is {voltage / 1000.0:.2f} V")
            else:
                print("Failed to get channel", i, "voltage")
            time.sleep(0.1)
        print("\n")

# get channel current
    print("\nget channel current:")
    start_time = time.time()
    while time.time() - start_time < 5:
        for i in range(1, 5):
            current = hub.get_channel_current(i)
            if current is not None:
                print(f"channel {i} current is {current / 1000.0:.2f} A")
            else:
                print("Failed to get channel", i, "current")
            time.sleep(0.1)
        print("\n")

if __name__ == "__main__":
    main()