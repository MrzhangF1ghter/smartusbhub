# Description: Python class to control Smart USB Hub with serial communication.
# copyright: (c) 2024 by zhangtec studio, embedded tec

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

# Get Channel Voltage
#     ch1_get_voltage     55 5A 03 01 00 04   55 5A 03 01 00 00 04
#     ch2_get_voltage     55 5A 03 02 00 05   55 5A 03 02 00 00 05 
#     ch3_get_voltage     55 5A 03 04 00 07   55 5A 03 04 00 00 07 
#     ch4_get_voltage     55 5A 03 08 00 0B   55 5A 03 08 00 00 0B 

# Get Channel Current
#     ch1_get_current     55 5A 04 01 00 05   55 5A 04 01 00 00 05
#     ch2_get_current     55 5A 04 02 00 06   55 5A 04 02 00 00 06
#     ch3_get_current     55 5A 04 04 00 08   55 5A 04 04 00 00 08
#     ch4_get_current     55 5A 04 08 00 0C   55 5A 04 08 00 00 0C

# Set Channel Dataline
#     ch1_set_data_on     55 5A 05 01 01 07   55 5A 05 01 01 07
#     ch1_set_data_off    55 5A 05 01 00 06   55 5A 05 01 00 06

#     ch2_set_data_on     55 5A 05 02 01 08   55 5A 05 02 01 08
#     ch2_set_data_off    55 5A 05 02 00 07   55 5A 05 02 00 07

#     ch3_set_data_on     55 5A 05 04 01 0A   55 5A 05 02 01 0A
#     ch3_set_data_off    55 5A 05 04 00 09   55 5A 05 02 00 09

#     ch4_set_data_on     55 5A 05 08 01 0E   55 5A 05 08 01 0E
#     ch4_set_data_off    55 5A 05 08 00 0D   55 5A 05 08 00 0D

# All Channel
#     ch_dataline_all_on  55 5A 05 0F 01 15   55 5A 05 0F 01 15  
#     ch_dataline_all_off 55 5A 05 0F 00 14   55 5A 05 0F 00 14 

# Get Channel Dataline
#     ch1_get_data_status 55 5A 08 01 00 09   55 5A 08 01 00 09[disconnect]   55 5A 08 01 01 0A[connected]
#     ch2_get_data_status 55 5A 08 02 00 0A   55 5A 08 02 00 0A[disconnect]   55 5A 08 02 01 0B[connected]
#     ch3_get_data_status 55 5A 08 04 00 0C   55 5A 08 04 00 0C[disconnect]   55 5A 08 04 01 0D[connected]
#     ch4_get_data_status 55 5A 08 08 00 10   55 5A 08 08 00 10[disconnect]   55 5A 08 08 01 11[connected]

#     All Channel
#     ch_all_get_dataline 55 5A 08 0F 00 17   

# Set Operate Mode
#     oper_mode_normal    55 5A 06 00 00 06   55 5A 06 00 00 06
#     oper_mode_interlock 55 5A 06 00 01 07   55 5A 06 00 01 07

# Get Operate Mode        55 5A 07 00 00 07
#     oper_mode_normal                        55 5A 07 00 00 07
#     oper_mode_interlock                     55 5A 07 00 01 08

# Get software version    55 5A FD 00 00 FD   55 5A FD 00 0F 0C //SW_VERSION
# Get hardware version    55 5A FE 00 00 FE   55 5A FE 00 03 01 //HW_VERSION
import os
import platform
import serial
import serial.tools.list_ports
import time
import glob
import threading

# Command definitions
CMD_GET_CHANNEL_POWER = 0x00
CMD_SET_CHANNEL_POWER = 0x01

CMD_INTERLOCK_CONTROL = 0x02

CMD_GET_CHANNEL_VOLTAGE = 0x03
CMD_GET_CHANNEL_CURRENT = 0x04

CMD_SET_CHANNEL_DATALINE = 0x05
CMD_GET_CHANNEL_DATALINE = 0x08

CMD_DISABLE_BUTTON_CONTROL = 0x09
CMD_QUERY_BUTTON_CONTROL = 0x0A

CMD_SET_OPERATE_MODE = 0x06
CMD_GET_OPERATE_MODE = 0x07
CMD_GET_FIRMWARE_VERSION = 0xFD
CMD_GET_HARDWARE_VERSION = 0xFE

# Channel value definitions
CHANNEL_1 = 0x01
CHANNEL_2 = 0x02
CHANNEL_3 = 0x04
CHANNEL_4 = 0x08

class SmartUSBHub:
    def __init__(self, port):
        self.ser = serial.Serial(port, 115200, timeout=1)
        self.debug = False
        self.stop_event = threading.Event()

        self.ack_events = {
            CMD_SET_CHANNEL_POWER: threading.Event(),
            CMD_GET_CHANNEL_POWER: threading.Event(),
            CMD_GET_CHANNEL_VOLTAGE: threading.Event(),
            CMD_GET_CHANNEL_CURRENT: threading.Event(),
            CMD_SET_CHANNEL_DATALINE: threading.Event(),
            CMD_GET_CHANNEL_DATALINE: threading.Event()
            # Add other commands if needed
        }
        self.channel_power_status = {}
        self.channel_voltages = {}
        self.channel_currents = {}
        self.channel_dataline = {}  # Store custom channel data

        self.protocol_thread = threading.Thread(target=self.protocol_task, args=(self.stop_event,), daemon=True)
        self.uart_recv_thread = threading.Thread(target=self.uart_recv_task, args=(self.stop_event,), daemon=True)
        self.protocol_thread.start()
        self.uart_recv_thread.start()

    @classmethod
    def scan_and_connect(cls):
        """Scan all serial ports, attempt connection, and verify if it's a Smart USB Hub."""
        for port_info in serial.tools.list_ports.comports():
            port_name = port_info.device
            try:
                hub = cls(port_name)
                if hub.check_operate_mode():
                    # Extract the relevant part of the port name
                    port_suffix = port_name.split('/')[-1]
                    hub.name = f"smarthub_id:{port_suffix}"
                    return hub
            except Exception as e:
                    print(f"Failed on port {port_name}: {e}")
        return None
    
    def check_operate_mode(self):
        """Send CMD_GET_OPERATE_MODE to see if the device responds correctly."""
        cmd_sum = (CMD_GET_OPERATE_MODE + 0) & 0xFF
        command = bytearray([0x55, 0x5A, CMD_GET_OPERATE_MODE, 0x00, 0x00, cmd_sum])
        self.ack_events[CMD_GET_OPERATE_MODE] = threading.Event()
        self.ack_events[CMD_GET_OPERATE_MODE].clear()
        self.ser.write(command)
        if self.debug:
            print(f"Sent CMD_GET_OPERATE_MODE: {command.hex()}")
        if self.ack_events[CMD_GET_OPERATE_MODE].wait(timeout=0.01):
            if self.debug:
                print("Device responded to CMD_GET_OPERATE_MODE.")
            return True
        return False
    
    def protocol_task(self, stop_event):
        while not stop_event.is_set():
            time.sleep(0.1)

    def parse_protocol_frame(self, data):
        # Ensure at least 6 bytes are present for older commands
        if len(data) < 6:
            return None

        frame_header1, frame_header2 = data[0], data[1]
        if frame_header1 != 0x55 or frame_header2 != 0x5A:
            return None

        cmd = data[2]
        channel = data[3]

        # New voltage/current frames have 7 bytes total (two bytes for value)
        if cmd in [CMD_GET_CHANNEL_VOLTAGE, CMD_GET_CHANNEL_CURRENT]:
            if len(data) < 7:
                return None
            value_hi = data[4]
            value_lo = data[5]
            checksum = data[6]
            if ((cmd + channel + value_hi + value_lo) & 0xFF) != checksum:
                return None
            # Combine two bytes into a single value
            value_combined = (value_hi << 8) | value_lo
            return (cmd, channel, value_combined, 7)
        else:
            value = data[4]
            checksum = data[5]
            if ((cmd + channel + value) & 0xFF) != checksum:
                return None
            return (cmd, channel, value, 6)

    def uart_recv_task(self, stop_event):
        buffer = bytearray()
        while not stop_event.is_set():
            if self.ser.in_waiting > 0:
                buffer.extend(self.ser.read(self.ser.in_waiting))
                # Try to parse frames of either 6 or 7 bytes
                while len(buffer) >= 6:
                    result = self.parse_protocol_frame(buffer)
                    if result is not None:
                        cmd, channel, value, length = result
                        if self.debug:
                            print(f"Parsed CMD: {cmd}, Channel: {channel}, Value: {value}")
                        if cmd == CMD_GET_CHANNEL_POWER:
                            self.handle_get_channel_power_status(channel, value)
                        elif cmd == CMD_GET_CHANNEL_VOLTAGE:
                            self.handle_get_channel_voltage(channel, value)
                        elif cmd == CMD_GET_CHANNEL_CURRENT:
                            self.handle_get_channel_current(channel, value)
                        elif cmd == CMD_SET_CHANNEL_DATALINE:
                            self.handle_set_channel_dataline(channel, value)
                        elif cmd == CMD_GET_CHANNEL_DATALINE:
                            self.handle_get_channel_dataline(channel, value)
                        elif cmd in self.ack_events:
                            self.ack_events[cmd].set()
                        del buffer[:length]
                    else:
                        buffer.pop(0)
            time.sleep(0.001)

    def _convert_channel(self, channel_mask):
        """Convert channel bitmask to corresponding channel numbers."""
        channels = []
        if channel_mask & CHANNEL_1:
            channels.append(1)
        if channel_mask & CHANNEL_2:
            channels.append(2)
        if channel_mask & CHANNEL_3:
            channels.append(3)
        if channel_mask & CHANNEL_4:
            channels.append(4)
        return channels
    
    def _send_packet(self, cmd, channels, data=None):
        """
        Create a command packet and send it via serial port.
        
        :param cmd: Command byte
        :param channels: List or tuple of channel numbers (1-4) to convert to mask
        :param data: List or tuple of additional data bytes, defaults to 0 if None
        :return: Bytearray containing the complete packet that was sent
        """
        # Convert channels to channel mask
        channel_mask = sum([1 << (ch - 1) for ch in channels])
        
        # Handle data parameter - use 0 if data is None
        if data is None:
            data = 0
            
        data = [channel_mask] + (data if isinstance(data, list) else [data])
        
        # Start with header bytes
        packet = bytearray([0x55, 0x5A, cmd])
        
        # Add data bytes
        packet.extend(data)
        
        # Calculate checksum (cmd + all data bytes) & 0xFF
        checksum = cmd
        for byte in data:
            checksum += byte
        checksum &= 0xFF
        
        # Add checksum to packet
        packet.append(checksum)
        
        # Send the packet
        self.ser.write(packet)
        
        if self.debug:
            print(f"Sent command: {packet.hex()}")
            
        return packet
        
    def handle_get_channel_power_status(self, channel, value):
        channels = self._convert_channel(channel)
        for ch in channels:
            self.channel_power_status[ch] = value
            if self.debug:
                print(f"Get Channel Power: ch{ch} = {value}")
        self.ack_events[CMD_GET_CHANNEL_POWER].set()

    def handle_get_channel_voltage(self, channel, value):
        ch_list = self._convert_channel(channel)
        for ch in ch_list:
            self.channel_voltages[ch] = value
            if self.debug:
                print(f"Get Channel Voltage: ch{ch} = {value}")
        self.ack_events[CMD_GET_CHANNEL_VOLTAGE].set()

    def handle_get_channel_current(self, channel, value):
        ch_list = self._convert_channel(channel)
        for ch in ch_list:
            self.channel_currents[ch] = value
            if self.debug:
                print(f"Get Channel Current: ch{ch} = {value}")
        self.ack_events[CMD_GET_CHANNEL_CURRENT].set()

    def handle_set_channel_dataline(self, channel, data_value):
        ch_list = self._convert_channel(channel)
        for ch in ch_list:
            self.channel_dataline[ch] = data_value
            if self.debug:
                print(f"Set Channel Data: ch{ch} = {data_value}")
        self.ack_events[CMD_SET_CHANNEL_DATALINE].set()

    def handle_get_channel_dataline(self, channel, data_value):
        ch_list = self._convert_channel(channel)
        for ch in ch_list:
            self.channel_dataline[ch] = data_value
            if self.debug:
                print(f"Get Channel Data: ch{ch} = {data_value}")
        self.ack_events[CMD_GET_CHANNEL_DATALINE].set()
    
    def set_channel_power_status(self, *channels, state):
        command = self._send_packet(CMD_SET_CHANNEL_POWER, channels, state)
        # Wait for acknowledgment
        ack_event = self.ack_events[CMD_SET_CHANNEL_POWER]
        ack_event.clear()
        if ack_event.wait(timeout=0.01):  # Timeout after 1 second
            if self.debug:
                print("set_channel_power_status ACK")
            return True
        else:
            if self.debug:
                print("set_channel_power_status No ACK!")
            return False
        
    def get_channel_power_status(self, *channels):
        command = self._send_packet(CMD_GET_CHANNEL_POWER, channels)
        # Wait for acknowledgment
        ack_event = self.ack_events[CMD_GET_CHANNEL_POWER]
        ack_event.clear()
        if ack_event.wait(timeout=0.01):  # Timeout after 1 second
            if self.debug:
                print("get_channel_power_status ACK")
            return self.channel_power_status
        else:
            if self.debug:
                print("get_channel_power_status No ACK!")
            return None

    def get_channel_voltage(self, *channels):
        channel_mask = sum([1 << (ch - 1) for ch in channels])
        cmd_sum = (CMD_GET_CHANNEL_VOLTAGE + channel_mask) & 0xFF
        command = bytearray([0x55, 0x5A, CMD_GET_CHANNEL_VOLTAGE, channel_mask, 0x00, cmd_sum])
        self.ack_events[CMD_GET_CHANNEL_VOLTAGE].clear()
        self.ser.write(command)
        if self.debug:
            print(f"Sent get_channel_voltage cmd: {command.hex()}")
        if self.ack_events[CMD_GET_CHANNEL_VOLTAGE].wait(timeout=0.01):
            return {ch: self.channel_voltages.get(ch) for ch in channels}
        return None

    def get_channel_current(self, *channels):
        channel_mask = sum([1 << (ch - 1) for ch in channels])
        cmd_sum = (CMD_GET_CHANNEL_CURRENT + channel_mask) & 0xFF
        command = bytearray([0x55, 0x5A, CMD_GET_CHANNEL_CURRENT, channel_mask, 0x00, cmd_sum])
        self.ack_events[CMD_GET_CHANNEL_CURRENT].clear()
        self.ser.write(command)
        if self.debug:
            print(f"Sent get_channel_current cmd: {command.hex()}")
        if self.ack_events[CMD_GET_CHANNEL_CURRENT].wait(timeout=0.01):
            return {ch: self.channel_currents.get(ch) for ch in channels}
        return None
    
    def set_channel_dataline(self, data_value, *channels,state):
        channel_mask = sum([1 << (ch - 1) for ch in channels])
        command = bytearray([0x55, 0x5A, CMD_SET_CHANNEL_DATALINE, channel_mask, state, (CMD_SET_CHANNEL_DATALINE + channel_mask + state) & 0xFF])
        self.ser.write(command)
        if self.debug:
            print(f"Sent command: {command.hex()}")
        # Wait for acknowledgment
        ack_event = self.ack_events[CMD_SET_CHANNEL_DATALINE]
        ack_event.clear()
        if ack_event.wait(timeout=0.01):  # Timeout after 1 second
            if self.debug:
                print("set_channel_dataline ack received")
            return True
        else:
            print("[Error]No set_channel_dataline ack received")
            if self.debug:
                print("No acknowledgment received")
            return False

    def get_channel_dataline_status(self, *channels):
        channel_mask = sum([1 << (ch - 1) for ch in channels])
        cmd_sum = (CMD_GET_CHANNEL_DATALINE + channel_mask) & 0xFF
        command = bytearray([0x55, 0x5A, CMD_GET_CHANNEL_DATALINE, channel_mask, 0x00, cmd_sum])
        self.ack_events[CMD_GET_CHANNEL_DATALINE].clear()
        self.ser.write(command)
        if self.debug:
            print(f"Sent get_channel_dataline_status cmd: {command.hex()}")
        if self.ack_events[CMD_GET_CHANNEL_DATALINE].wait(timeout=0.01):
            return {ch: self.channel_dataline.get(ch) for ch in channels}
        return None
