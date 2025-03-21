import sys
sys.path.append('../')
from smartusbhub import SmartUSBHub
import time
import argparse
import pyqtgraph as pg
import numpy as np
import sys
from PyQt5 import QtWidgets, QtCore, QtSerialPort

#pack app: pyinstaller --hidden-import=smartusbhub --paths=.. oscilloscope.py --onedir

class SerialPortSelector(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Serial Port")
        self.setLayout(QtWidgets.QVBoxLayout())
        self.port_combobox = QtWidgets.QComboBox()
        self.ok_button = QtWidgets.QPushButton("OK")

        # List available serial ports with filtering
        self.ports = QtSerialPort.QSerialPortInfo.availablePorts()
        for port in self.ports:
            port_name = port.portName()
            # Filter for macOS/Linux specific patterns
            if sys.platform in ["linux", "darwin"] and not (port_name.startswith("cu.usbmodem") or port_name.startswith("cu.ttyACM")):
                continue
            self.port_combobox.addItem(port_name)

        # Add widgets to the layout
        self.layout().addWidget(self.port_combobox)
        self.layout().addWidget(self.ok_button)
        self.ok_button.clicked.connect(self.accept)

    def get_selected_port(self):
        return self.port_combobox.currentText()
    
class OscilloscopeApp(QtWidgets.QWidget):
    def __init__(self, hub, delay_interval=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hub = hub
        self.delay_interval = delay_interval
        self.channels = [1, 2, 3, 4]
        self.data = {
            'current': np.zeros((len(self.channels), 100)),
            'voltage': np.zeros((len(self.channels), 100))
        }
        # 设置window title
        self.setWindowTitle("Smart USB Hub Oscilloscope")
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.plots = []
        self.curves = {'voltage': [],'current': []}
        self.labels = {'voltage': [],'current': []}
        self.buttons = []
        self.checkboxes = {'voltage': [],'current': []}
        colors = {'voltage': (255, 255, 0),'current': (218, 0, 102)}
        
        for i in range(len(self.channels)):
            # Create sub-layout for each channel
            row_layout = QtWidgets.QHBoxLayout()

            # Create PlotWidget and add to layout
            plot_widget = pg.PlotWidget()
            plot_widget.setYRange(0, 5500)  # 电压范围 0 - 5500 mV
            plot_widget.setLabel("left", f"Channel {self.channels[i]}")

            # Create label
            label = pg.TextItem("", color=colors['voltage'], anchor=(0, 1))
            plot_widget.addItem(label)
            self.labels['voltage'].append(label)

            label = pg.TextItem("", color=colors['current'], anchor=(0, 1))
            plot_widget.addItem(label)
            self.labels['current'].append(label)

            self.plots.append(plot_widget)

            # Create curves
            for key in ['voltage', 'current']:
                curve = plot_widget.plot(pen=pg.mkPen(color=colors[key], width=1))
                self.curves[key].append(curve)

            # Create a vertical layout for checkboxes
            checkbox_layout = QtWidgets.QVBoxLayout()
            checkbox_layout.insertSpacing(0,50)

            # Create button for channels toggle
            button = QtWidgets.QPushButton(f"Channel {self.channels[i]}")
            button.setCheckable(True)
            button.setChecked(True)
            button.clicked.connect(lambda _, idx=i: self.toggle_channel(idx))
            self.buttons.append(button)
            checkbox_layout.addWidget(button)

            # Create checkboxes for toggling visibility
            for key in ['voltage', 'current']:
                checkbox = QtWidgets.QCheckBox(f"{key.capitalize()}")
                checkbox.setChecked(True)
                checkbox.stateChanged.connect(lambda _, idx=i, k=key: self.toggle_curve(idx, k))
                self.checkboxes[key].append(checkbox)
                checkbox_layout.addWidget(checkbox)

            row_layout.addLayout(checkbox_layout)
            row_layout.addWidget(plot_widget)
            self.layout.addLayout(row_layout)

        # get channels status
        self.get_channels_status()
        # enable timer for data update
        self.timer = QtCore.QTimer()
        self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(int(self.delay_interval))


    def on_connection_lost(self):
        """Handle device disconnection."""
        if not hasattr(self, 'alert_box') or self.alert_box is None:
            self.alert_box = QtWidgets.QMessageBox(self)
            self.alert_box.setIcon(QtWidgets.QMessageBox.Warning)
            self.alert_box.setWindowTitle("Connection Lost!")
            self.alert_box.setText("Connection Lost. Please check the connection and try again.")
            self.alert_box.setStandardButtons(QtWidgets.QMessageBox.Close)
            self.alert_box.button(QtWidgets.QMessageBox.Close).clicked.connect(self.close_application)
            self.alert_box.show()

    def on_connection_restored(self):
        """Handle device reconnection."""
        if hasattr(self, 'alert_box') and self.alert_box is not None:
            self.alert_box.close()
            self.alert_box = None

    def close_application(self):
        """Handle application close action."""
        QtWidgets.QApplication.quit()

    def get_channels_status(self):
        # Get the status of each channel and update the buttons
        for i, channel in enumerate(self.channels):
            status = self.hub.get_channel_power_status(channel)

            if status:
                print(f"Channel {channel} is on")
            else:
                print(f"Channel {channel} is off")

            if status is not None:
                self.buttons[i].setChecked(status == 1)
    
    def toggle_curve(self, channel_idx, data_type):
        # Toggle the visibility of the selected curve
        visible = self.checkboxes[data_type][channel_idx].isChecked()
        self.curves[data_type][channel_idx].setVisible(visible)
        self.labels[data_type][channel_idx].setVisible(visible)

    def toggle_channel(self, channel_idx):
        # Toggle the state of the selected channel
        state = 1 if self.buttons[channel_idx].isChecked() else 0
        self.hub.set_channel_power(self.channels[channel_idx],state=state)
        self.get_channels_status()

    def update_data(self):
        if self.hub.is_connected() is False:
            self.on_connection_lost()
            return
        # get voltage data and update curve and label
        for i, channel in enumerate(self.channels):
            # Fetch new data
            new_voltage = self.hub.get_channel_voltage(channel) or 0
            # Update data arrays
            self.data['voltage'][i]= np.roll(self.data['voltage'][i], -1)
            self.data['voltage'][i, -1] = new_voltage
            # Update curves
            self.curves['voltage'][i].setData(self.data['voltage'][i])

            # Fetch new data
            new_current = self.hub.get_channel_current(channel) or 0
            # Update data arrays
            self.data['current'][i] = np.roll(self.data['current'][i], -1)
            self.data['current'][i, -1] = new_current
            # Update curves
            self.curves['current'][i].setData(self.data['current'][i])

            # update voltage label
            voltage_in_volts = new_voltage / 1000.0
            self.labels['voltage'][i].setText(f"{voltage_in_volts:.3f} V")
            self.labels['voltage'][i].setPos(0, new_voltage-300)

            # update current label
            current_in_ma = new_current / 1000.0
            self.labels['current'][i].setText(f"{current_in_ma:.3f} A")
            self.labels['current'][i].setPos(0, new_current-300)

def main():
    # Create and show the oscilloscope application
    app = QtWidgets.QApplication(sys.argv)

    # Show serial port selector
    selector = SerialPortSelector()
    if selector.exec_() == QtWidgets.QDialog.Accepted:
        selected_port = selector.get_selected_port()

        # Add '/dev/' prefix for Linux/macOS if not already included
        if not selected_port.startswith("/dev/") and (sys.platform == "linux" or sys.platform == "darwin"):
            selected_port = f"/dev/{selected_port}"

        print(f"Selected port: {selected_port}")

        # Initialize SmartUSBHub instance
        try:
            hub = SmartUSBHub(port=selected_port)

            if hub.ser is None:
                raise ConnectionError("Could not connect to the device. Please check the connection and try again.")
        except Exception as e:
            print(f"[ERROR] {e}")
            QtWidgets.QMessageBox.critical(None, "Connection Error", str(e))
            return
    else:
        print("No port selected. Exiting...")
        return

    # Start the oscilloscope application
    oscilloscope = OscilloscopeApp(hub)
    oscilloscope.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()