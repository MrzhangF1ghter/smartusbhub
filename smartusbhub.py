# [Protocol Example]

# Single Channel ON/OFF   send                ack                
#     ch1_on              55 5A 01 01 01 03   55 5A 01 01 01 03 
#     ch2_on              55 5A 01 02 01 04   55 5A 01 02 01 04 
#     ch3_on              55 5A 01 04 01 06   55 5A 01 04 01 06 
#     ch4_on              55 5A 01 08 01 0A   55 5A 01 08 01 0A 
#     ch1_off             55 5A 01 01 00 02   55 5A 01 01 00 02 
#     ch2_off             55 5A 01 02 00 03   55 5A 01 02 00 03 
#     ch3_off             55 5A 01 04 00 05   55 5A 01 04 00 05 
#     ch4_off             55 5A 01 08 00 09   55 5A 01 08 00 09 

# All Channel
#     ch_all_on           55 5A 01 0F 01 11   55 5A 01 0F 01 11  
#     ch_all_off          55 5A 01 0F 00 10   55 5A 01 0F 00 10 

# Combine Channel
#     ch_13_on            55 5A 01 05 01 07   55 5A 01 05 01 07 
#     ch_13_off           55 5A 01 05 00 06   55 5A 01 05 00 06 
#     ch_24_on            55 5A 01 0A 01 0C   55 5A 01 0A 01 0C 
#     ch_24_off           55 5A 01 0A 00 0B   55 5A 01 0A 00 0B 

# Get digital level
#     ch1_get_level       55 5A 00 01 00 01   55 5A 00 01 00 01 [OFF]     55 5A 00 01 01 02 [ON]
#     ch2_get_level       55 5A 00 02 00 02   55 5A 00 02 00 02 [OFF]     55 5A 00 02 01 03 [ON]
#     ch3_get_level       55 5A 00 04 00 04   55 5A 00 04 00 04 [OFF]     55 5A 00 04 01 05 [ON]
#     ch4_get_level       55 5A 00 08 00 08   55 5A 00 08 00 08 [OFF]     55 5A 00 08 01 09 [ON]
#     ch_all_get_level    55 5A 00 0F 00 0F   55 5A 00 01 00 01 55 5A 00 02 00 02 55 5A 00 04 00 04 55 5A 00 08 00 08 

# Initerlock mode
#     interlock_set_ch1   55 5A 02 01 01 04   55 5A 02 01 01 04 
#     interlock_set_ch2   55 5A 02 02 01 05   55 5A 02 02 01 05
#     interlock_set_ch3   55 5A 02 04 01 07   55 5A 02 04 01 07
#     interlock_set_ch4   55 5A 02 08 01 0B   55 5A 02 08 01 0B

#     oper_mode_normal    55 5A 06 00 00 06   55 5A 06 00 00 06
#     oper_mode_interlock 55 5A 06 00 01 07   55 5A 06 00 01 07

# Get Operate Mode        55 5A 07 00 00 07
#     oper_mode_normal                        55 5A 07 00 00 07
#     oper_mode_interlock                     55 5A 07 00 01 08

import os
import platform
import serial
import time
import glob

# Command constants
CMD_GET_CHANNEL_STATUS = 0x00
CMD_CONTROL_CHANNEL = 0x01
CMD_INTERLOCK_CONTROL = 0x02
CMD_SET_MODE = 0x06
CMD_GET_MODE = 0x07

# Channel value definitions
CHANNEL_1 = 0x01
CHANNEL_2 = 0x02
CHANNEL_3 = 0x04
CHANNEL_4 = 0x08

# ON/OFF state constants
ON              = 0x01
OFF             = 0x00
MODE_NORMAL     = 0x00
MODE_INTERLOCK  = 0x01

class SmartUSBHub:
    def __init__(self, port=None, baudrate=115200, debug=False, max_retries=3):
        """Initialize the SmartUSBHub instance with serial port settings."""
        self.debug = debug
        self.max_retries = max_retries
        self.ser = self._open_serial_port(port, baudrate)

    def _open_serial_port(self, port, baudrate):
        """Attempt to open a specified or automatically detected serial port with retries."""
        retries = 0

        # Determine the device path based on OS
        if os.name == 'nt':  # Windows
            device_pattern = "COM*"
        elif platform.system() == 'Darwin':  # macOS
            device_pattern = "/dev/cu.usbmodem*"
        else:  # Linux and others
            device_pattern = "/dev/ttyACM*"


        while retries < self.max_retries:
            if not port:
                print(f"[INFO] No port specified, searching for {device_pattern} devices...")
                for device in glob.glob(device_pattern):
                    print(f"[INFO] Device found: {device}")
                    try:
                        ser = serial.Serial(device, baudrate, timeout=1)
                        # Use temporary serial object to check device response
                        if self._send_command(CMD_GET_MODE, 0x00, ser=ser) is not None:
                            print(f"[INFO] Connected to device at: {device}")
                            return ser
                        ser.close()  # Close if no valid response
                    except serial.SerialException as e:
                        print(f"[ERROR] Could not open device {device}: {e}")
            else:
                try:
                    ser = serial.Serial(port, baudrate, timeout=1)
                    print(f"[DEBUG] Serial port {port} opened successfully at {baudrate} baud.")
                    return ser
                except serial.SerialException as e:
                    print(f"[ERROR] Failed to open serial port: {e}")
            
            retries += 1
            print(f"[ERROR] Attempt {retries}/{self.max_retries} failed. Retrying...")
            time.sleep(1)

        print("[ERROR] No available device found. Please specify a serial port or check the device.")
        return None

    def _send_command(self, cmd, channel, value=0x00, ser=None):
        """Send a command to the device and read the response."""
        ser = ser or self.ser
        if not ser:
            print("[ERROR] Serial port is not open. Cannot send command.")
            return None

        # Construct command frame
        frame = [0x55, 0x5A, cmd, channel, value]
        checksum = (cmd + channel + value) & 0xFF
        frame.append(checksum)
        
        # Send data and print debug info
        try:
            ser.write(bytearray(frame))
            if self.debug:
                print(f"[DEBUG] Sent data: {' '.join(f'{byte:02X}' for byte in frame)}")
            time.sleep(0.001)  # Wait to ensure device has time to respond
        except serial.SerialException as e:
            print(f"[ERROR] Failed to send data: {e}")
            return None

        # Read device response and print debug info
        try:
            response = ser.read(6)
            if self.debug:
                print(f"[DEBUG] Recv data: {' '.join(f'{byte:02X}' for byte in response)}")
            if len(response) == 6:
                return response
            else:
                print("[ERROR] Incomplete data received, device may not be responding.")
                return None
        except serial.SerialException as e:
            print(f"[ERROR] Failed to read data: {e}")
            return None

    def _convert_channel(self, *channels):
        """Convert channel numbers (1, 2, 3, 4) to corresponding bitmask values."""
        channel_map = {1: CHANNEL_1, 2: CHANNEL_2, 3: CHANNEL_3, 4: CHANNEL_4}
        channel_value = 0x00
        for ch in channels:
            channel_value |= channel_map.get(ch, 0x00)
        return channel_value

    def get_channel_status(self, *channels):
        """Get the ON/OFF status of specified channels."""
        channel_value = self._convert_channel(*channels)
        response = self._send_command(CMD_GET_CHANNEL_STATUS, channel_value)
        if response:
            return response[4]
        return None

    def control_channel(self, state, *channels):
        """Turn specified channels ON or OFF based on state."""
        if state not in [ON, OFF]:
            print("[ERROR] Invalid state, use ON or OFF.")
            return None

        channel_value = self._convert_channel(*channels)
        response = self._send_command(CMD_CONTROL_CHANNEL, channel_value, state)
        if response:
            return response[3]
        return None

    def interlock_control(self, state, channel):
        """Control a single channel in interlock mode."""
        if state not in [ON, OFF]:
            print("[ERROR] Invalid state, use ON or OFF.")

        channel_value = self._convert_channel(channel)
        response = self._send_command(CMD_INTERLOCK_CONTROL, channel_value, state)
        if response:
            return response[3]
        return None

    def interlock_control_all_off(self):
        response = self._send_command(CMD_INTERLOCK_CONTROL, 0, 0)
        if response:
            return response[3]
        return None
    
    def set_mode_normal(self):
        """Set device to normal mode."""
        response = self._send_command(CMD_SET_MODE, 0x00, 0x00)
        if response:
            print("[INFO] Device set to Normal mode.")
        else:
            print("[ERROR] Failed to set mode to Normal.")

    def set_mode_interlock(self):
        """Set device to interlock mode."""
        response = self._send_command(CMD_SET_MODE, 0x00, 0x01)
        if response:
            print("[INFO] Device set to Interlock mode.")
        else:
            print("[ERROR] Failed to set mode to Interlock.")

    def get_mode(self):
        """Get current device mode (Interlock or Normal)."""
        response = self._send_command(CMD_GET_MODE, 0x00)
        if response:
            return MODE_INTERLOCK if response[4] == 0x01 else MODE_NORMAL
        return None

    def close(self):
        """Close the serial connection if open."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            if self.debug:
                print("[DEBUG] Serial connection closed.")