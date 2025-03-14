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
#     interlock_set_off   55 5A 02 0F 01 12   55 5A 02 0F 01 12

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

# button control
#     disable_buttons     55 5A 09 00 00 09   55 5A 09 00 00 09
#     enable_buttons      55 5A 09 00 01 0A   55 5A 09 00 01 0A

# get button control
#     get_buttons_status  55 5A 0A 00 00 0A   55 5A 0A 00 00 0A[disable]   55 5A 0A 00 01 0B[enable]

# Get software version    55 5A FD 00 00 FD   55 5A FD 00 0F 0C //SW_VERSION
# Get hardware version    55 5A FE 00 00 FE   55 5A FE 00 03 01 //HW_VERSION

import serial
import serial.tools.list_ports
import time
import threading
import signal
import sys
import logging
import colorlog

# Command definitions
CMD_GET_CHANNEL_POWER_STATUS = 0x00
CMD_SET_CHANNEL_POWER = 0x01

CMD_SET_CHANNEL_POWER_INTERLOCK = 0x02

CMD_GET_CHANNEL_VOLTAGE = 0x03
CMD_GET_CHANNEL_CURRENT = 0x04

CMD_SET_CHANNEL_DATALINE = 0x05
CMD_GET_CHANNEL_DATALINE_STATUS = 0x08

CMD_SET_BUTTON_CONTROL = 0x09
CMD_GET_BUTTON_CONTROL_STATUS = 0x0A

CMD_SET_OPERATE_MODE = 0x06
CMD_GET_OPERATE_MODE = 0x07
CMD_GET_FIRMWARE_VERSION = 0xFD
CMD_GET_HARDWARE_VERSION = 0xFE

# Channel value definitions
CHANNEL_1 = 0x01
CHANNEL_2 = 0x02
CHANNEL_3 = 0x04
CHANNEL_4 = 0x08

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# # Create file handler which logs even debug messages
# fh = logging.FileHandler('smartusbhub.log')
# fh.setLevel(logging.DEBUG)

# Create console handler with a higher log level
ch = colorlog.StreamHandler()

# # Create formatter and add it to the handlers
# file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(file_formatter)

console_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "white",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)
ch.setFormatter(console_formatter)

# Add the handlers to the logger
# logger.addHandler(fh)
logger.addHandler(ch)

class SmartUSBHub:
    """
    Represents a Smart USB Hub device, providing methods to control power, data lines, and more.
    """

    def __init__(self, port):
        """
        Initializes the Smart USB Hub.

        Args:
            port (str): The serial port name to connect to the device.
        """
        self.port = port
        self.ser = serial.Serial(port, 115200,timeout = 0.5)
        self.com_timeout = 0.5  
        logger.info(f"SmartUSBHub initialized on port {self.port}")

        self.ack_events = {
            CMD_GET_OPERATE_MODE: threading.Event(),
            CMD_SET_CHANNEL_POWER: threading.Event(),
            CMD_GET_CHANNEL_POWER_STATUS: threading.Event(),
            CMD_SET_CHANNEL_POWER_INTERLOCK: threading.Event(),
            CMD_GET_CHANNEL_VOLTAGE: threading.Event(),
            CMD_GET_CHANNEL_CURRENT: threading.Event(),
            CMD_SET_CHANNEL_DATALINE: threading.Event(),
            CMD_GET_CHANNEL_DATALINE_STATUS: threading.Event(),
            CMD_SET_BUTTON_CONTROL: threading.Event(),
            CMD_GET_BUTTON_CONTROL_STATUS: threading.Event(),
            CMD_GET_FIRMWARE_VERSION: threading.Event(),
            CMD_GET_HARDWARE_VERSION: threading.Event(),
        }
        
        self.hardware_version = None
        self.firmware_version = None
        self.operate_mode = None
        self.button_control_state = None


        self.channel_power_status = {}
        self.channel_dataline_status = {}
        self.channel_voltages = {}
        self.channel_currents = {}

        self._start()
        
        self.hardware_version = self.get_hardware_version()
        self.firmware_version =  self.get_firmware_version()
        self.operate_mode = self.get_operate_mode()
        self.button_control_state = self.get_button_control_status()

        if self.operate_mode is None:
            logger.error("Failed to get operate mode.")
            sys.exit(1)
            
        logger.info(f"Hardware version: V1.{self.hardware_version}")
        logger.info(f"Firmware version: V1.{self.firmware_version}")
        logger.info(f"Operate mode: {'normal' if self.operate_mode == 0 else 'interlock'}")
        logger.info(f"button control: {'enable' if self.button_control_state == 1 else 'disabled'}")

    @classmethod
    def scan_and_connect(cls):
        """
        Searches for available Smart USB Hub devices and connects to the first valid one.

        Returns:
            SmartUSBHub or None: An instance of SmartUSBHub if found, otherwise None.
        """
        for port_info in serial.tools.list_ports.comports():
            port_name = port_info.device
            logger.debug(f"Trying to connect to port {port_name}")
            if port_info.vid == 0x1A86 and port_info.pid == 0xfe0c:
                hub = cls(port_name)
                port_suffix = port_name.split("/")[-1]
                hub.name = f"smarthub_id:{port_suffix}"
                return hub

        logger.error("No Smart USB Hub found.")
        return None

    def _start(self):
        """
        Starts the UART receive thread and sets up signal handling.
        """
        self.stop_event = threading.Event()
        signal.signal(signal.SIGINT, self._signal_handler)
        self.uart_recv_thread = threading.Thread(target=self._uart_recv_task)
        self.uart_recv_thread.start()
        print("SmartUSBHub started.")
    

    def _signal_handler(self, sig, frame):
        """
        Handles termination signals to cleanly shut down the UART thread and close the serial port.

        Args:
            sig (int): Signal number.
            frame (frame object): Current stack frame.
        """
        self.stop_event.set()
        self.uart_recv_thread.join(timeout=1)
        if self.ser and self.ser.is_open:
            self.ser.flush()
            self.ser.close()
        sys.exit(0)

    def _parse_protocol_frame(self, data):
        """
        Processes a raw data frame from the device and delivers it to the correct handler.

        Args:
            data (bytes): Raw bytes read from the device.

        Returns:
            tuple or None: Parsed command, channel, value, and length if valid, otherwise None.
        """

        logger.debug(f"Received data: {data.hex()}")

        if len(data) < 6:
            return None
        frame_header1, frame_header2 = data[0], data[1]
        if frame_header1 != 0x55 or frame_header2 != 0x5A:
            return None

        cmd = data[2]
        channel = data[3]

        # voltage/current frames have 7 bytes total (two bytes for value)
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

    def _uart_recv_task(self):
        """
        Continuously reads from the UART and processes incoming data frames.
        """
        buffer = bytearray()
        while not self.stop_event.is_set():
            if self.ser.in_waiting > 0:
                buffer.extend(self.ser.read(self.ser.in_waiting))
                # Try to parse frames of either 6 or 7 bytes
                while len(buffer) >= 6:
                    result = self._parse_protocol_frame(buffer)
                    if result is not None:
                        cmd, channel, value, length = result
                        logger.debug(
                            f"Parsed CMD: {cmd:#04x}, Channel: {channel:#04x}, Value: {value:#04x}"
                        )
                        if cmd == CMD_SET_CHANNEL_POWER:
                            self._handle_set_channel_power_status(channel, value)
                        if cmd == CMD_GET_CHANNEL_POWER_STATUS:
                            self._handle_get_channel_power_status(channel, value)
                        if cmd == CMD_SET_CHANNEL_POWER_INTERLOCK:
                            self._handle_power_interlock_control()
                        elif cmd == CMD_GET_CHANNEL_VOLTAGE:
                            self._handle_get_channel_voltage(channel, value)
                        elif cmd == CMD_GET_CHANNEL_CURRENT:
                            self._handle_get_channel_current(channel, value)
                        elif cmd == CMD_SET_CHANNEL_DATALINE:
                            self._handle_set_channel_dataline(channel, value)
                        elif cmd == CMD_GET_CHANNEL_DATALINE_STATUS:
                            self._handle_get_channel_dataline(channel, value)
                        elif cmd == CMD_GET_BUTTON_CONTROL_STATUS:
                            self._handle_get_button_control(value)
                        elif cmd == CMD_SET_BUTTON_CONTROL:
                            self._handle_set_button_control(value)
                        elif cmd == CMD_GET_OPERATE_MODE:
                            self._handle_get_operate_mode(value)
                        elif cmd == CMD_SET_OPERATE_MODE:
                            self._handle_set_operate_mode(value)
                        elif cmd == CMD_GET_FIRMWARE_VERSION:
                            self._handle_firmware_version(value)
                        elif cmd == CMD_GET_HARDWARE_VERSION:
                            self._handle_hardware_version(value)

                        # if cmd in self.ack_events:
                        #     self.ack_events[cmd].set()

                        del buffer[:length]
                    else:
                        buffer.pop(0)
            time.sleep(0.001)

    def _convert_channel(self, channel_mask):
        """
        Converts a channel bitmask into a list of individual channel numbers.

        Args:
            channel_mask (int): Bitmask representing which channels are included.

        Returns:
            list: A list of channel numbers (1, 2, 3, 4).
        """
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
        Builds and sends a packet to the device.

        Args:
            cmd (int): Command byte.
            channels (list[int]): List of channel numbers to include in the packet.
            data (list[int] or None): Extra data bytes to include.

        Returns:
            bytearray: The packet that was sent to the device.
        """
        if channels is None:
            channel_mask = 0
        else:
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
        if self.ser and self.ser.is_open:
            self.ser.write(packet)

        logger.debug(f"Sent command: {packet.hex()}")

        return packet

    def _handle_set_operate_mode(self, data_value):
        # Handles the response for setting the operate mode.
        self.ack_events[CMD_SET_OPERATE_MODE].set()

    def _handle_get_operate_mode(self, data_value):
        # Handles the response for getting the operate mode.
        self.operate_mode = data_value
        self.ack_events[CMD_GET_OPERATE_MODE].set()

    def _handle_set_channel_power_status(self, channel, value):
        # Handles the response for setting the power status of the channel(s).
        self.ack_events[CMD_SET_CHANNEL_POWER].set()

    def _handle_get_channel_power_status(self, channel, value):
        # Updates stored power status for the specified channel(s).
        channels = self._convert_channel(channel)
        for ch in channels:
            self.channel_power_status[ch] = value
            logger.debug(f"Get Channel Power: ch{ch} = {value}")
        self.ack_events[CMD_GET_CHANNEL_POWER_STATUS].set()

    def _handle_power_interlock_control(self):
        self.ack_events[CMD_SET_CHANNEL_POWER_INTERLOCK].set()
        
    def _handle_get_channel_voltage(self, channel, value):
        # Updates stored voltage value for the specified channel(s).
        ch_list = self._convert_channel(channel)
        for ch in ch_list:
            self.channel_voltages[ch] = value
            logger.debug(f"Get Channel Voltage: ch{ch} = {value}")
        self.ack_events[CMD_GET_CHANNEL_VOLTAGE].set()

    def _handle_get_channel_current(self, channel, value):
        # Updates stored current value for the specified channel(s).
        ch_list = self._convert_channel(channel)
        for ch in ch_list:
            self.channel_currents[ch] = value
            logger.debug(f"Get Channel Current: ch{ch} = {value}")
        self.ack_events[CMD_GET_CHANNEL_CURRENT].set()

    def _handle_set_channel_dataline(self, channel, data_value):
        # Updates stored dataline status after a set command is received.
        channels = self._convert_channel(channel)
        for ch in channels:
            self.channel_dataline_status[ch] = data_value
            logger.debug(f"Set Channel Dataline: ch{ch} = {data_value}")
        self.ack_events[CMD_SET_CHANNEL_DATALINE].set()
        
    def _handle_get_channel_dataline(self, channel, data_value):
        # Updates stored dataline status after a get command is received.
        ch_list = self._convert_channel(channel)
        for ch in ch_list:
            self.channel_dataline_status[ch] = data_value
            logger.debug(f"Get Channel Dataline: ch{ch} = {data_value}")
        self.ack_events[CMD_GET_CHANNEL_DATALINE_STATUS].set()

    def _handle_get_button_control(self, data_value):
        # Updates stored button control state.
        self.button_control_state = data_value
        self.ack_events[CMD_GET_BUTTON_CONTROL_STATUS].set()

    def _handle_set_button_control(self, data_value):
        # Handles the response for setting the button control state.
        self.ack_events[CMD_SET_BUTTON_CONTROL].set()

    def _handle_firmware_version(self, data_value):
        # Updates stored firmware version.
        self.firmware_version = data_value
        self.ack_events[CMD_GET_FIRMWARE_VERSION].set()

    def _handle_hardware_version(self, data_value):
        # Updates stored hardware version.
        self.hardware_version = data_value
        self.ack_events[CMD_GET_HARDWARE_VERSION].set()

    def set_operate_mode(self, mode):
        """
        Set the device's operating mode.

        Args:
            mode (int): The desired operating mode.
        """
        self._send_packet(CMD_SET_OPERATE_MODE, None, mode)
        ack_event = self.ack_events[CMD_SET_OPERATE_MODE]
        ack_event.clear()
        if ack_event.wait(self.com_timeout):
            logger.debug("set_operate_mode ACK")
        else:
            logger.error("set_operate_mode No ACK!")

    def get_operate_mode(self):#@TODO: need to fix return none?
        """
        Sends a command to verify the current operating mode of the device.

        Returns:
            bool: True if the device responds in the expected mode, otherwise False.
        """
        command = self._send_packet(CMD_GET_OPERATE_MODE, None, None)
        # Wait for acknowledgment
        ack_event = self.ack_events[CMD_GET_OPERATE_MODE]
        ack_event.clear()
        if ack_event.wait(self.com_timeout):  
            logger.debug("get_operate_mode ACK")
            logger.debug(f"operate_mode: {self.operate_mode}")
            if self.operate_mode is None:
                logger.warning("get_operate_mode No ACK!")
            return self.operate_mode
        else:
            self.operate_mode = None
            logger.warning("get_operate_mode No ACK!")
            return None

    def set_channel_power(self, *channels, state):
        """
        Sends a command to set the power state of specified channels.

        Args:
            *channels (int): Channels to control.
            state (int): 1 to enable power, 0 to disable.
        """
        command = self._send_packet(CMD_SET_CHANNEL_POWER, channels, state)
        # Wait for acknowledgment
        ack_event = self.ack_events[CMD_SET_CHANNEL_POWER]
        ack_event.clear()
        if ack_event.wait(self.com_timeout):  
            logger.debug("set_channel_power ACK")
            return True
        else:
            logger.error("set_channel_power No ACK!")
            return False

    def get_channel_power_status(self, *channels):
        """
        Requests the power status of specified channels.

        Args:
            *channels (int): Channels to query.

        Returns:
            dict or int or None: A dictionary with channel numbers as keys and power states as values if multiple channels are queried,
                                 the power state of the single channel if only one channel is queried,
                                 or None if timed out.
        """
        command = self._send_packet(CMD_GET_CHANNEL_POWER_STATUS, channels)
        # Wait for acknowledgment
        ack_event = self.ack_events[CMD_GET_CHANNEL_POWER_STATUS]
        ack_event.clear()
        if ack_event.wait(self.com_timeout):  
            logger.debug("get_channel_power_status ACK")

            if len(channels) == 1:
                return self.channel_power_status.get(channels[0], None)
            logger.info(f"get_channel_power_status: {self.channel_power_status}")
            return self.channel_power_status
        else:
            logger.error("get_channel_power_status No ACK!")
            return None

    def set_channel_power_interlock(self,channel):
        """
        Sets the interlock mode for a specified channel or all channels.

        Args:
            channel (int or None): The channel to set. If None, all channels will be turn off.

        Returns:
            bool: True if the command was acknowledged, False otherwise.
        """
        if channel is None:
            # If channel is None, set interlock mode for all channels
            self._send_packet(CMD_SET_CHANNEL_POWER_INTERLOCK, None,0)
        else:
            channels = [channel]
            self._send_packet(CMD_SET_CHANNEL_POWER_INTERLOCK, channels,1)

        ack_event = self.ack_events[CMD_SET_CHANNEL_POWER_INTERLOCK]
        ack_event.clear()
        if ack_event.wait(timeout=0.1):  
            logger.debug("set_channel_power_interlock ACK")
            return True
        else:
            logger.error("set_channel_power_interlock No ACK!")
            return False
        
    def get_channel_voltage(self, channel):
        """
        Returns the voltage of a single channel.

        Args:
            channel (int): The channel to query.

        Returns:
            int or None: Voltage reading for the channel, or None if timed out.
        """
        if isinstance(channel, (list, tuple)):
            raise ValueError("get_channel_voltage only supports a single channel")

        command = self._send_packet(CMD_GET_CHANNEL_VOLTAGE, [channel])
        ack_event = self.ack_events[CMD_GET_CHANNEL_VOLTAGE]
        ack_event.clear()
        if ack_event.wait(self.com_timeout):
            logger.debug("get_channel_voltage ACK")
            return self.channel_voltages.get(channel)
        else:
            logger.error("get_channel_voltage No ACK!")
            return None

    def get_channel_current(self, channel):
        """
        Returns the current reading of a single channel.

        Args:
            channel (int): The channel to query.

        Returns:
            int or None: Current reading for the channel, or None if timed out.
        """
        if isinstance(channel, (list, tuple)):
            raise ValueError("get_channel_voltage only supports a single channel")

        command = self._send_packet(CMD_GET_CHANNEL_CURRENT, [channel])
        ack_event = self.ack_events[CMD_GET_CHANNEL_CURRENT]
        ack_event.clear()
        if ack_event.wait(self.com_timeout):
            logger.debug("get_channel_current ACK")
            return self.channel_currents.get(channel)
        else:
            logger.error("get_channel_current No ACK!")
            return None

    def set_channel_dataline(self, data_value, *channels, state):
        """
        Sends a command to set the data line state of specific channels.

        Args:
            data_value (int): New data line state.
            *channels (int): Channels to update.
            state (int): 1 to enable data line, 0 to disable.
        """
        command = self._send_packet(CMD_SET_CHANNEL_DATALINE, channels, state)
        # Wait for acknowledgment
        ack_event = self.ack_events[CMD_SET_CHANNEL_DATALINE]
        ack_event.clear()
        if ack_event.wait(self.com_timeout):  
            logger.debug("set_channel_dataline ACK")
            return True
        else:
            logger.error("set_channel_dataline No ACK!")
            return False

    def get_channel_dataline_status(self, *channels):
        """
        Requests the data line status for specified channels.

        Args:
            *channels (int): Channels to query.

        Returns:
            dict or None: A dictionary with channel numbers as keys and data line states as values, or None if timed out.
        """
        command = self._send_packet(CMD_GET_CHANNEL_DATALINE_STATUS, channels)
        # Wait for acknowledgment
        ack_event = self.ack_events[CMD_GET_CHANNEL_DATALINE_STATUS]
        ack_event.clear()
        if ack_event.wait(self.com_timeout):  
            logger.debug("get_channel_dataline_status ACK")
            return self.channel_dataline_status
        else:
            logger.error("get_channel_dataline_status No ACK!")
            return None

    def set_button_control(self, enable: bool):
        """
        Enable or disable the hub's physical buttons.

        Args:
            enable (bool): True to enable buttons, False to disable.
        """
        data_val = 1 if enable else 0

        self._send_packet(CMD_SET_BUTTON_CONTROL, None, data_val)
        ack_event = self.ack_events[CMD_SET_BUTTON_CONTROL]
        ack_event.clear()
        if ack_event.wait(self.com_timeout):
            logger.debug("set_button_control ACK")
            return self.button_control_state
        else:
            logger.error("set_button_control No ACK!")

    def get_button_control_status(self):
        """
        Query whether the hub's physical buttons are enabled or disabled.

        Returns:
            int or None: 1 if enabled, 0 if disabled, or None if no response.
        """
        self._send_packet(CMD_GET_BUTTON_CONTROL_STATUS, None, None)
        ack_event = self.ack_events[CMD_GET_BUTTON_CONTROL_STATUS]
        ack_event.clear()
        if ack_event.wait(self.com_timeout):
            logger.debug("get_button_control_status ACK")
            return self.button_control_state
        else:
            logger.error("get_button_control_status No ACK!")
            return None

    def get_firmware_version(self):
        """
        Query the device's firmware version.

        Returns:
            int or None: The firmware version, or None if no response.
        """
        self._send_packet(CMD_GET_FIRMWARE_VERSION, None, None)
        ack_event = self.ack_events[CMD_GET_FIRMWARE_VERSION]
        ack_event.clear()
        if ack_event.wait(self.com_timeout):
            logger.debug("get_firmware_version ACK")
            return self.firmware_version
        else:
            logger.error("get_firmware_version No ACK!")
            return None

    def get_hardware_version(self):
        """
        Query the device's hardware version.

        Returns:
            int or None: The hardware version, or None if no response.
        """
        self._send_packet(CMD_GET_HARDWARE_VERSION, None, None)
        ack_event = self.ack_events[CMD_GET_HARDWARE_VERSION]
        ack_event.clear()
        if ack_event.wait(self.com_timeout):
            logger.debug("get_hardware_version ACK")
            return self.hardware_version
        else:
            logger.error("get_hardware_version No ACK!")
            return None
