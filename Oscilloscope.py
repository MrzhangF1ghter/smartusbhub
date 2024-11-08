from smartusbhub import *
import time
import argparse
import pyqtgraph as pg
import numpy as np
import sys
from PyQt5 import QtWidgets, QtCore, QtSerialPort

class OscilloscopeApp(QtWidgets.QWidget):
    def __init__(self, hub, delay_interval=0.001, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hub = hub
        self.delay_interval = delay_interval
        self.channels = [1, 2, 3, 4]
        self.voltage = np.zeros((len(self.channels), 100))  # 初始化4个通道的电压数据，每通道100个点

        # 设置窗口
        self.setWindowTitle("Smart USB Hub Oscilloscope")
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # 创建4条曲线、按钮和电压标签
        self.plots = []
        self.curves = []
        self.voltage_labels = []
        self.buttons = []
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        
        for i in range(len(self.channels)):
            # 创建子布局来放置绘图和按钮
            row_layout = QtWidgets.QHBoxLayout()

            # 创建PlotWidget并添加到布局
            plot_widget = pg.PlotWidget()
            plot_widget.setYRange(0, 5000)  # 电压范围 0 - 5000 mV
            plot_widget.setLabel("left", f"Channel {self.channels[i]}")
            curve = plot_widget.plot(pen=pg.mkPen(color=colors[i], width=1))
            self.plots.append(plot_widget)
            self.curves.append(curve)

            # 创建电压标签
            label = pg.TextItem("", color=colors[i], anchor=(0, 1))
            plot_widget.addItem(label)
            self.voltage_labels.append(label)

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
        # 获取电压数据并更新曲线和标签
        for i, channel in enumerate(self.channels):
            new_voltage = self.hub.get_channel_voltage(channel) or 0  # 获取电压值
            self.voltage[i] = np.roll(self.voltage[i], -1)  # 左移一位
            self.voltage[i, -1] = new_voltage  # 更新最新值到数组末尾

            # 更新曲线数据
            self.curves[i].setData(self.voltage[i])

            # 更新电压标签，显示伏特并保留两位小数
            voltage_in_volts = new_voltage / 1000.0
            self.voltage_labels[i].setText(f"{voltage_in_volts:.2f} V")
            self.voltage_labels[i].setPos(0, new_voltage-300)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Smart USB Hub control program")
    parser.add_argument("-p", "--port", help="Specify serial port, e.g., /dev/ttyUSB0")
    args = parser.parse_args()

    # Initialize SmartUSBHub instance
    hub = SmartUSBHub(port=args.port)

    if hub.ser is None:
        print("[ERROR] Could not connect to the device. Please check the connection and try again.")
        return

    # Create and show the oscilloscope application
    app = QtWidgets.QApplication(sys.argv)
    oscilloscope = OscilloscopeApp(hub)
    oscilloscope.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()