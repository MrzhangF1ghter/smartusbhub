import sys
sys.path.append('./..')
sys.path.append('../')
from smartusbhub import *
import time
import argparse
import pyqtgraph as pg
import numpy as np
import sys
from PyQt5 import QtWidgets, QtCore, QtSerialPort

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
    def __init__(self, hub, delay_interval=0.001, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hub = hub
        self.delay_interval = delay_interval
        self.channels = [1, 2, 3, 4]
        self.current = np.zeros((len(self.channels), 100))  # 初始化4个通道的电流数据，每通道100个点

        # 设置窗口
        self.setWindowTitle("Smart USB Hub Oscilloscope")
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # 创建4条曲线、按钮和电流标签
        self.plots = []
        self.curves = []
        self.current_labels = []
        self.buttons = []
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        
        for i in range(len(self.channels)):
            # 创建子布局来放置绘图和按钮
            row_layout = QtWidgets.QHBoxLayout()

            # 创建PlotWidget并添加到布局
            plot_widget = pg.PlotWidget()
            plot_widget.setYRange(0, 4000)  # 电流范围 0 - 5000 mV
            plot_widget.setLabel("left", f"Channel {self.channels[i]}")
            curve = plot_widget.plot(pen=pg.mkPen(color=colors[i], width=1))
            self.plots.append(plot_widget)
            self.curves.append(curve)

            label = pg.TextItem("", color=colors[i], anchor=(0, 1))
            plot_widget.addItem(label)
            self.current_labels.append(label)

            # 创建通道开关按钮
            button = QtWidgets.QPushButton(f"Channel {self.channels[i]}")
            button.setCheckable(True)
            button.setChecked(True)
            button.clicked.connect(lambda _, idx=i: self.toggle_channel(idx))
            self.buttons.append(button)

            # 设置样式表，使按钮在选中状态变为黄色
            button.setStyleSheet("""
                QPushButton {
                    background-color: darkgray;  /* 默认颜色 */
                }
                QPushButton:checked {
                    background-color: yellow;  /* 选中时的颜色 */
                }
            """)

            # 将绘图和按钮添加到布局
            row_layout.addWidget(button)
            row_layout.addWidget(plot_widget)
            self.layout.addLayout(row_layout)

        # 初始化通道状态
        self.initialize_channel_status()
        # 启动定时器，定时更新数据
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(int(self.delay_interval * 1000))

    def initialize_channel_status(self):
        """获取各通道的初始状态并设置复选框。"""
        for i, channel in enumerate(self.channels):
            status = self.hub.get_channel_status(channel)
            print(f"{channel} is {status}")
            if status is not None:
                # 设置复选框的状态
                self.buttons[i].setChecked(status == 1)
        
    def toggle_channel(self, channel_idx):
        # 根据按钮的状态控制通道的开关
        state = ON if self.buttons[channel_idx].isChecked() else OFF
        self.hub.control_channel(state, self.channels[channel_idx])

    def update_data(self):
        # 获取电流数据并更新曲线和标签
        for i, channel in enumerate(self.channels):
            new_current = self.hub.get_channel_current(channel) or 0  # 获取电流值
            self.current[i] = np.roll(self.current[i], -1)  # 左移一位
            self.current[i, -1] = new_current  # 更新最新值到数组末尾

            # 更新曲线数据
            self.curves[i].setData(self.current[i])

            # 更新电流标签，显示安培并保留两位小数
            current_in_amps = new_current/1000
            round(current_in_amps,2)
            self.current_labels[i].setText(f"{current_in_amps:.2f} A")
            self.current_labels[i].setPos(0, new_current-300)
            
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