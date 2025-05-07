# SmartUSBHub python library

文档版本：V1.91

[TOC]

## 简介

smartusbhub是一个能够通过串口控制的USB2.0 4口集线器。

使用前请先了解smartusbhub，详情请阅读[智能USB集线器_使用指南](https://github.com/MrzhangF1ghter/smartusbhub/blob/main/document/智能USB集线器_使用指南.md)

> [!NOTE]
>
> 此smartusbhub python库只是用于测试用途，如果要集成到生产环境，建议自行实现通信控制。
>
> 协议文档请查阅： [智能USB集线器_使用指南 协议章节](https://github.com/MrzhangF1ghter/smartusbhub/blob/main/document/智能USB集线器_使用指南.md)
>
> 最简单的控制demo：[simple_serial.py](./examples/simple_serial.py)



## 环境部署

### 获取最新的库

把此代码仓库克隆到本地,假设你的工程名字为`my_project`  

```shell
cd my_project
git clone https://github.com/MrzhangF1ghter/smartusbhub.git
```

库目录结构如下：

```shell
.
├── README.md					# 文档
├── examples					# 例程
├── apps							# 已经编译好的例程
├── requirements.txt	# 安装依赖
└── smartusbhub.py 		# 功能源码
```



### 设置虚拟环境

设置python虚拟环境（推荐）
`python -m venv venv`

1. 进入python虚拟环境

   - 对于Windows平台:

    `.\venv\Scripts\activate.bat`

   - 对于unix平台:

    `source ./venv/bin/activate`

2. 安装依赖库
    `pip install -r requirements.txt`

3. 将随附的USB差分信号线开关接到设备短边侧的<u>设备通信口</u>USB-C，另外一端接到主机的USB端口上，连接后主机将会把设备识别成:

   - Windows平台:  `COMx`
   - Linux平台: `/dev/ttyACMx`
   - mac平台: `/dev/cu.usbmodemx`

> [!NOTE]
>
> 若要数据传输，除了连接<u>设备通信口</u>，还需要连接<u>数据上行口</u>。



### 运行例程

`smartusbhub python library`库包含多个例程，其存放在`examples`目录下，目前有以下例子：

- `power_control_example`：展示如何控制指定通道的电源
- `dataline_control_example`：展示如何控制指定通道的USB差分信号线开关通断（保持电源供电）
- `voltage_monitor_example`：展示如何获取指定通道的电压值
- `current_monitor_example`：展示如何获取指定通道的电流值
- `setting_example`:展示如何配置设置项
- `user_callback_example`：展示如何添加用户回调
- `oscilloscope`：一个简单的GUI示波器，可控制通道电源开关、电压及电流采集

![oscilloscope](./assets/oscilloscope.png)

<center>图：示波器demo</center>



若要运行demo，请执行以下指令：

- 激活虚拟环境：

  - Linux/macOS用户：

    ```
     source ./venv/bin/activate
    ```

  - Windows 用户：

    ```shell
    .\venv\Scripts\activate.bat
    ```

- 进入examples文件夹：

  ```
  cd ./examples/
  ```

- 运行demo，例如：

  ```shell
  python oscilloscope.py
  ```

  

### 集成到你的项目中

通过导入smartusbhub库即可即成到你的项目之中。

1. 按照前面的章节 *使用方法*配置: 步骤 1 到 5.

2. 导入`smartusbhub`库到你的工程.

   ```python
   import sys
   sys.path.append('../')
   from smartusbhub import SmartUSBHub
   ```

3. 初始化`SmartUSBhub`实例:

   - 通过自动扫描连接设备：

     ```python
     hub = SmartUSBHub.scan_and_connect()
     ```

   - 通过指定串口号连接设备：

     ```python
     hub = SmartUSBHub("串口路径")
     例子：
     hub = SmartUSBHub("/dev/cu.usbmodem132301")
     ```



## **用户接口**

### 设备连接

#### `scan_and_connect()`

- **描述**: 扫描可用的 Smart USB Hub 设备，并连接到第一个有效设备。
- **返回值**:
  
  - SmartUSBHub 实例（如果找到设备），否则返回 `None`。
  
- **示例**:
  
  ```python
  hub = SmartUSBHub.scan_and_connect()
  ```

#### `connect(port)`

- **描述**: 连接到指定的Smart USB Hub 设备。

- **参数:**

  - [port](str): 要连接的串口名称。

- **示例:**

  ```python
  hub.connect("/dev/cu.usbmodem132301")
  ```



### 设备断开链接

#### `disconnect()`

- **描述**:断开当前的Smart USB Hub 设备。

- **示例:**

  ```python
  hub.disconnect()
  ```



### 控制通道电源开关

#### `set_channel_power(*channels, state)`

- **描述**: 设置指定通道的电源状态。
- **参数**:
  - `*channels` (int): 要控制的通道。
  - state (int): `1` 开启电源，`0` 关闭电源。

- **返回值**:

  - bool: 如果命令设置成功返回 `True`，否则返回 `False`。

- **示例**:

  ```python
  hub.set_channel_power(1, 2, state=1)
  ```



### 获取通道电源状态

#### `get_channel_power_status(*channels)`

- **描述**: 查询指定通道的电源状态。
- **参数**:
  
  - `*channels` (int): 要查询的通道，可变参数形式，范围 1~4。
- **返回值**:
  - `dict` 或 `int` 或 `None`: 如果查询多个通道，返回包含通道状态的字典；如果查询单个通道，返回该通道的状态；若超时则返回 `None`。
- **示例**:
  ```python
  status = hub.get_channel_power_status(1, 2)
  ```



### 控制通道电源互锁

#### `set_channel_power_interlock(channel)`

- **描述**: 设置指定通道或所有通道的互锁模式。
- **参数**:
  
  - channel (int 或 `None`): 要设置的通道。如果为 `None`，则关闭所有通道。
  
- **返回值**:
  
  - bool: 如果命令设置成功返回 `True`，否则返回 `False`。
  
- **示例**:
  
  ```python
  hub.set_channel_power_interlock(1)
  ```



### 控制通道USB差分信号线开关

#### `set_channel_dataline(*channels, state)`

- **描述**: 设置指定通道的USB差分信号线开关状态。

- **参数**:
  - `*channels` (int): 要更新的通道，可变参数形式，范围 1~4。
  - state (int): `1` 连通 D+ D-的物理连接， `0` 断开D+ D-的物理连接。

- **返回值**:
  
  - bool: 如果命令设置成功返回 `True`，否则返回 `False`。

- **示例**:
  
  连通 通道1 的数据信号
  
  ```python
  hub.set_channel_dataline(1,state=1)
  ```
  
  
### 获取通道USB差分信号线开关状态
#### `get_channel_dataline_status(*channels)`
- **描述**: 查询指定通道的USB差分信号线开关状态。

- **参数**:
  - `*channels` (int): 要查询的通道，可变参数形式，范围 1~4。
  
- **返回值**:
  - `dict` 或 `None`: 包含通道状态的字典，若超时则返回 `None`。
  
- **示例**:
  
  获取 通道2 的数据信号连接状态
  
  ```python
  status = hub.get_channel_dataline_status(1, 2)
  ```



### 获取通道电压

#### `get_channel_voltage(channel)`

- **描述**: 查询单个通道的电压。
- **参数**:
  - channel (int): 要查询的通道。

- **返回值**:
  - `int` 或 `None`: 通道的电压值(mV)，若超时则返回 `None`。
- **示例**:
  
  获取 通道1 的 电压值
  
  ```python
  voltage = hub.get_channel_voltage(1)
  ```
  



### 获取通道电流

#### `get_channel_current(channel)`

- **描述**: 查询单个通道的电流。
- **参数**:
  - channel (int): 要查询的通道。

- **返回值**:
  
  - `int` 或 `None`: 通道的电流值(mA)，若超时则返回 `None`。
- **示例**:
  
  获取 通道1 的 电流值
  
  ```python
  current = hub.get_channel_current(1)
  ```



### 设置通道电源的上电默认状态

#### `set_default_power_status(*channels,enable,status)`

- **描述**: 设置指定通道的上电默认电源状态。

- **参数**:

  - `*channels` (int): 要设置的通道，可变参数形式，范围 1~4。
  - enable (int): `1` 启用默认状态， `0` 禁用默认状态。
  - status (int): 1 默认打开电源，0 默认关闭电源

- **示例**:

  通道1、2、3、4上电默认打开

  ```python
  hub.set_default_dataline_status(1,2,3,4,enable=1,status=0)
  ```

  通道1、2、3、4上电不使用默认值

  ```python
  hub.set_default_dataline_status(1,2,3,4,enable=0)
  ```



### 获取通道电源的上电默认状态

#### `get_default_power_status(self,*channels)`

- **描述**: 查询一个或多个通道电源的默认上电状态

- **参数**:

  - `*channels` (int): 要查询的通道，可变参数形式，范围 1~4。

- **返回值**:

  - `dict` 或 `None`:  {通道号: {"enabled": 是否启用, "value": 状态}}，其中 enabled 为 0（禁用）或 1（启用），value 为 0（默认关闭）或 1（默认开启）。
  - 若超时则返回 `None`。

- **示例**:

  获取通道1、2、3、4的电源上电默认状态

  ```python
  hub.get_default_power_status(1,2,3,4)
  ```

  返回：

  ```python
  {1: {'enabled': 0, 'value': 0}, 2: {'enabled': 0, 'value': 0}, 3: {'enabled': 0, 'value': 0}, 4: {'enabled': 0, 'value': 0}}
  ```



### 设置通道USB差分信号线开关的上电默认状态

#### `set_default_power_status(*channels,enable,status)`

- **描述**: 设置指定通道的上电默认电源状态。

- **参数**:

  - `*channels` (int): 要设置的通道，可变参数形式，范围 1~4。
  - enable (int): `1` 启用默认状态， `0` 禁用默认状态。
  - status (int): 1 默认打开电源，0 默认关闭电源

- **返回值**:

  - bool: 如果命令设置成功返回 `True`，否则返回 `False`。
  
- **示例**:

  通道1、2、3、4上电默认打开

  ```python
  hub.set_default_dataline_status(1,2,3,4,enable=1,status=0)
  ```




### 获取通道USB差分信号线开关的上电默认状态

#### `get_default_dataline_status(self,*channels)`

- **描述**: 查询一个或多个通道USB差分信号线开关的上电默认状态

- **参数**:

  - `*channels` (int): 要查询的通道，可变参数形式，范围 1~4。

- **返回值**:

  - `dict` 或 `None`:  {通道号: {"enabled": 是否启用, "value": 状态}}，其中 enabled 为 0（禁用）或 1（启用），value 为 0（默认关闭）或 1（默认开启）。
  - 若超时则返回 `None`。

- **示例**:

  获取通道1、2、3、4的USB差分信号线开关的上电默认状态

  ```python
  hub.get_default_dataline_status(1,2,3,4)
  ```

  返回：

  ```python
  {1: {'enabled': 0, 'value': 1}, 2: {'enabled': 0, 'value': 1}, 3: {'enabled': 0, 'value': 1}, 4: {'enabled': 0, 'value': 1}}
  ```



### 设置按钮控制

#### `set_button_control(enable)`

- **描述**: 启用或禁用集线器的物理按钮。

- **参数**:
  - enable (bool): `True` 启用按钮，`False` 禁用按钮。

- **返回值**:
  
  - bool: 如果命令设置成功返回 `True`，否则返回 `False`。
  
- **示例**:

  设置按钮为启用

  ```python
  hub.set_button_control(True)
  ```



### 获取按钮控制状态

#### `get_button_control_status()`

- **描述**: 查询集线器的物理按钮是否启用。
- **返回值**:
  - `int` 或 `None`: `1` 表示启用，`0` 表示禁用，若无响应则返回 `None`。
- **示例**:
  
  查询按钮是否启用
  
  ```python
  status = hub.get_button_control_status()
  ```



### 设置设备的操作模式

#### `set_operate_mode(mode)`

- **描述**: 设置设备的操作模式。
- **参数**:
  
  - mode (int): 操作模式（`0` 为普通模式，`1` 为互锁模式）。
  
- **返回值**:
  - bool: 如果命令设置成功返回 `True`，否则返回 `False`。
  

- **注意:**
  - 互锁模式下，控制只能用互锁指令。

- **示例**:

  设置设备为普通模式

  ```python
  hub.set_operate_mode(0)
  ```




### 获取设备的操作模式

#### `get_operate_mode()`

- **描述**: 查询设备的当前操作模式。

- **返回值**:
  - `int` 或 `None`: 当前操作模式，若无响应则返回 `None`。
  
- **示例**:
  
  查询设备操作模式
  
  ```python
  mode = hub.get_operate_mode()
  ```



### 获取设备信息

#### `get_device_info()`

- **描述**: 获取集线器的 ID、硬件版本、固件版本、操作模式和按钮控制状态。
- **返回值**:
  - `dict`: 包含设备信息的字典。
- **示例**:
  ```python
  info = hub.get_device_info()
  print(info)
  ```



### 获取固件版本

#### `get_firmware_version()`

- **描述**: 查询设备的固件版本。
- **返回值**:
  - `int` 或 `None`: 固件版本，若无响应则返回 `None`。
- **示例**:
  ```python
  firmware_version = hub.get_firmware_version()
  ```



### 获取硬件版本

#### `get_hardware_version()`

- **描述**: 查询设备的硬件版本。
- **返回值**:
  - `int` 或 `None`: 硬件版本，若无响应则返回 `None`。
- **示例**:
  ```python
  hardware_version = hub.get_hardware_version()
  ```



### 注册用户回调

#### `register_callback(cmd, callback)`

- **描述**: 为指定的命令注册一个用户回调函数。当设备返回该命令的应答时，回调函数会被触发。

- **参数**:

  - cmd (int): 要注册回调的命令。
  - callback (function): 当命令的 ACK 被接收到时执行的回调函数。回调函数应接受两个参数：
    - channel (int): 触发回调的通道编号。
    - status (int): 通道的状态值。

- **返回值:**

  - 无返回值。

- **注意事项**:

  - 如果 cmd 不在支持的命令列表中，将记录警告日志，并不会注册回调。
  - 回调函数的签名应与设备返回的数据结构匹配。

  | CMD宏                           | 含义                          |
  | :------------------------------ | :---------------------------- |
  | CMD_GET_CHANNEL_POWER_STATUS    | 获取通道电源开关值            |
  | CMD_SET_CHANNEL_POWER           | 控制通道电源                  |
  | CMD_SET_CHANNEL_POWER_INTERLOCK | 控制通道电源互锁              |
  | CMD_SET_CHANNEL_DATALINE        | 控制通道USB差分信号线开关     |
  | CMD_GET_CHANNEL_DATALINE_STATUS | 获取通道USB差分信号线开关状态 |
  | CMD_GET_CHANNEL_VOLTAGE         | 获取通道电压                  |
  | CMD_GET_CHANNEL_CURRENT         | 获取通道电流                  |
  | CMD_SET_BUTTON_CONTROL          | 启用/禁用 按键控制            |
  | CMD_GET_BUTTON_CONTROL_STATUS   | 获取按键控制状态              |
  | CMD_SET_DEFAULT_POWER_STATUS    | 设置通道默认电源状态          |
  | CMD_GET_DEFAULT_POWER_STATUS    | 获取通道默认电源状态          |
  | CMD_SET_DEFAULT_DATALINE_STATUS | 设置通道默认数据连接状态      |
  | CMD_GET_DEFAULT_DATALINE_STATUS | 获取通道默认数据连接状态      |
  | CMD_SET_AUTO_RESTORE            | 启用/禁用 断电保存            |
  | CMD_GET_AUTO_RESTORE_STATUS     | 获取断电保存是否启用          |
  | CMD_SET_OPERATE_MODE            | 设置设备工作模式 普通/互锁    |
  | CMD_GET_OPERATE_MODE            | 获取设备工作模式              |
  | CMD_FACTORY_RESET               | 恢复出厂设置                  |
  | CMD_GET_FIRMWARE_VERSION        | 获取固件版本号                |
  | CMD_GET_HARDWARE_VERSION        | 获取硬件版本号                |

- **示例**:

  设置按键回调，当按键按下时，产生回调

  ```python
  def button_press_callback(channel, status):
      print("Button press detected on channel", channel, "with power status", status)
  
  hub.register_callback(CMD_GET_CHANNEL_POWER_STATUS, button_press_callback)
  ```

