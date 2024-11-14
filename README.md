# SmartUSBHub python library
smartusbhub是一个能够通过串口控制的USB2.0 4口集线器。

使用前请先了解smartusbhub，详情请阅读[设备简介]()

详情请阅读项目wiki [wiki page](https://github.com/MrzhangF1ghter/smartusbhub/wiki)

> [!NOTE]
>
> 此smartusbhub python库只是用于测试用途，如果要集成到生产环境，建议自行实现通信控制，协议文档请查阅： [protocol documentation](https://github.com/MrzhangF1ghter/smartusbhub/wiki/protocol)

## 使用方法

[视频演示及教程](https://www.bilibili.com/video/BV1R5meY7EkQ/)

1. 把此代码仓库克隆到本地,假设你的工程名字为`my_project`  

   ```shell
   cd my_project
   git clone https://github.com/MrzhangF1ghter/smartusbhub.git
   ```

2. 设置python虚拟环境（推荐）
   `python -m venv venv`

3. 进入python虚拟环境

   - 对于Windows平台:

    `.\venv\Scripts\activate.bat`

   - 对于unix平台:

    `source ./venv/bin/activate`

4. 安装依赖库
    `pip install -r ./smartusbhub/requirements.txt`

5. 将随附的数据线接到设备短边侧的设备通信口USB-C，另外一端接到主机的USB端口上，连接后主机将会把设备识别成:

   - Windows平台:  `COMx`
   - Linux平台: `/dev/ttyACMx`
   - mac平台: `/dev/cu.usbmodemx`

6. 运行test.py demo

   `python smartusbhub/app/test.py -p COMx`

   **传入参数**:

   --port: 指定端口号 (e.g., /dev/ttyUSB0).

   该demo将会:

   - 控制各通道开/关，获取其状态并打印出来.

   - 展示如何组合控制通道。


## 集成到你的项目中

通过导入smartusbhub库即可即成到你的项目之中。

1. 按照前面的章节 *使用方法*配置: 步骤 1 到 5.

2. 导入`smartusbhub`库到你的工程.

   ```python
   import sys
   sys.path.append('./..')
   sys.path.append('../')
   from smartusbhub import *
   ```

4. 初始化`SmartUSBhub`实例:

   ```python
   hub = SmartUSBHub(port="/dev/cu.usbmodemxxx")
   ```

5. 通过以下方法控制设备

**方法:**

`control_channel(state, *channels)`: 打开或者关闭指定通道。

`get_channel_status(*channels)`: 获取指定通道的开关值。

`interlock_control(state, channel)`: 互锁控制，打开指定通道，其余通道关闭。

`get_channel_voltage(self, *channels)`: 获取指定通道的电压值 单位：毫伏。

`set_mode_normal() and set_mode_interlock()`: 设置设备模式为普通还是互锁模式（断电仍然保存）。

`get_mode()`: Retrieve the current mode of the device.: 获取设备当前模式为普通还是互锁模式。

`close()`: 关闭设备。

## demos

### 示波器

smartusbhub包含了一个示波器应用，该应用可以直观的查看每一个通道的电压值以及控制通道的开关。

```shell
python smartusbhub/app/oscilloscope.py -p /dev/cu.usbmodemxxx
```

![oscilloscope](./assets/oscilloscope.png)
