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
ON = 0x01
OFF = 0x00

class SmartUSBHub:
    def __init__(self, port=None, baudrate=115200, debug=False):
        """Initialize the SmartUSBHub instance with serial port settings."""
        self.debug = debug
        self.ser = None
        self.ser = self._open_serial_port(port, baudrate)

    def _open_serial_port(self, port, baudrate):
        """Attempt to open a specified or automatically detected serial port."""
        if not port:
            print("[INFO] No port specified, searching for /dev/cu.usbmodem* devices...")
            for device in glob.glob("/dev/cu.usbmodem*"):
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
            print("[ERROR] No available device found. Please specify a serial port.")
            return None
        else:
            try:
                ser = serial.Serial(port, baudrate, timeout=1)
                print(f"[DEBUG] Serial port {port} opened successfully at {baudrate} baud.")
                return ser
            except serial.SerialException as e:
                print(f"[ERROR] Failed to open serial port: {e}")
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
                print(f"[DEBUG] Received data: {' '.join(f'{byte:02X}' for byte in response)}")
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

    def interlock_control(self, channel):
        """Control a single channel in interlock mode."""
        channel_value = self._convert_channel(channel)
        response = self._send_command(CMD_INTERLOCK_CONTROL, channel_value, 0x01)
        if response:
            return response[3]
        return None

    def set_mode(self, mode):
        """Set device mode: 0 for normal, 1 for interlock."""
        response = self._send_command(CMD_SET_MODE, 0x00, mode)
        if response:
            return response[3]
        return None

    def get_mode(self):
        """Get current device mode (Interlock or Normal)."""
        response = self._send_command(CMD_GET_MODE, 0x00)
        if response:
            return "Interlock" if response[3] == 0x01 else "Normal"
        return None

    def close(self):
        """Close the serial connection if open."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            if self.debug:
                print("[DEBUG] Serial connection closed.")