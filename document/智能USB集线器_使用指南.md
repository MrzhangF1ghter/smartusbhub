# 智能USB集线器 使用指南

文档版本：V1.8

## 简介

智能USB集线器（SmartUSBHub），是一款可以通过指令控制的USB集线器，具备普通集线器所不具备的指令控制端口功能。



## 功能

- **标准USB 2.0 数据传输**：采用MTT技术的USB 2.0 Hub芯片，每个端口均可达到480Mbps的USB2.0速率，可作为普通USB集线器使用。
- **按键控制：**每个通道均配独立的开关，可通过开关控制通道电源的打开或者关闭，且支持禁用按键控制，只通过指令控制。
- **可编程控制**：使用简单的指令控制集线器，配套python库、C库及demo、提供Windows、Ubuntu、macOS的上位机，快速验证。
- **电源控制**：每个通道均可通过按键或者指令控制其物理电源的通断，从而实现模拟设备插拔。
- **数据控制**：每个通道均可通过指令控制其数据信号的通断，从而实现继续为设备供电但断开其数据通路，实现不断电的模拟设备的插拔。

- **电压采集**：每个通道均支持独立电流采集，从而实现对设备的运行状态监控、低功耗测算等高级用途。

- **电流采集**：每个通道均支持独立的电流采集，从而实现对设备的运行状态监控（如：检测设备是否已经插入）、低功耗测算等高级用途。

- **互锁控制**：设备可设置为互锁模式，在该模式下，同一时刻只有一路通道可以打开，其余通道将自动关闭。

- **默认状态**：每个通道均可独立设置上电的电源、数据默认状态。

- **断电保存**：每个通道均可独立设置是否启用断电保存功能。
- **固件升级**：设备支持一键OTA，持续获得新功能支持。

  
## 应用

在以下领域广泛应用：

### **汽车研发**

- 测试机台控制：远程控制Jlink等调试器插拔。
- ECU调试：远程控制USB端口插拔。

### **手机研发**

- 驱动测试：远程控制充电口插拔。
- 软件开发：安卓ADB调试、Xcode调试。

### **芯片研发**

- 芯片功能验证：模拟物理插拔，验证USB IP功能。

### **物联网研发**

- 测试物联网模块功耗、通过电流判断运行是否正常。

### **集群管理**

- 树莓派集群集中管理（支持堆叠）。
- 充电管理。
- 服务器USB外设管理。

### **资产管理**

- 电子签章授权
- 加密狗授权
- 税务ukey授权

### 功耗分析

- 设备功耗监控
- 设备连接状态监控



## **设备接口**

- **设备控制端口** 1个：用于收发控制指令，另一端接到主机

- **辅助供电端口** 1个：当下游设备需要更高功率时，将外置供电电源连接至此端口

- **USB上行端口** 1个：用于连接USB主机的端口

- **USB下行端口** 4个：用于连接USB设备 

<img src="./assets/%E6%8E%A5%E7%BA%BF%E5%9B%BE.jpeg" alt="接线图" style="zoom:50%;" />

**[1]按键 x4：**

> **单击：**打开/关闭对应通道
>
> **长按：**[按键1] 3秒：切换工作模式：普通/互锁； 6秒：恢复出厂设置
>
> ​            [按键2] 3秒：启用/关闭上电恢复功能

**[2]通道指示灯 x4：**

> 亮：通道已打开
>
> 灭：通道已关闭

**[3]状态指示灯：**

> 慢闪：普通模式
>
> 快闪：互锁模式

**[4]辅助供电端口：**

> 当下游设备功率超过15W时，请将外置电源连接至该端口。
>
> 该口电源最大输入规格：50W（5V 10A）带过流保护。

**[5]设备通信口：**

> 该口用于收发控制指令，另一端接到主机。
>
> 最大输入规格：15W（5V 3A）带防倒灌、过压保护、过流保护。

**[6]USB2.0上行端口：**

> 该口具备供电与数据传输功能，可用于连接USB主机设备，如电脑
>
> 最大输入规格：15W（5V 3A）带防倒灌、过压保护、过流保护。

**[7]USB2.0下行端口 x4：**

> USB-A接口，具备供电数据传输功能，用于连接USB设备
>
> 每个口电源最大输出规格：20W（5V 4A）
>



> [!NOTE]
>
> **术语解释：**
>
> - **USB上行端口 (Upstream Port)：**
>
>   指向数据流传输的 **主机方向** 的 USB 端口。上行端口是 USB 设备（如集线器、外设）与 USB 主机（如电脑）连接的接口。它用于接收来自主机的指令或供电。
>
> - **USB 下行端口 (Downstream Port):**
>
>   指向数据流传输的 **设备方向** 的 USB 端口。下行端口是主机或 USB 集线器用来连接其他 USB 外设的接口。
>
> - **防倒灌(Backflow Prevention):**
>
>   在双电源电路中，使用防倒灌电路避免电源互相干扰。
>
> - **互锁(Interlock**):
>
>   互锁是一种安全或逻辑设计机制，确保系统中多个操作或设备之间的顺序和条件执行。



## **系统兼容性**

本设备使用标准USB CDC，免驱动。已验证以下系统版本：

- Windows 10、11 或更新版本。
- macOS 10.9 或更新版本。
- Linux 发行版，如Ubuntu。
- 其他X86、AMD64、ARM64架构兼容，如Apple Silicon平台、Windows on ARM平台。

> [!NOTE]
>
> 对于<u>Windows7</u>及之前版本的Windows操作系统，需安装驱动，驱动存放在为`windows7_xp_driver`文件夹中。




## **USB兼容性**

本设备遵循USB2.0协议，上行端口支持USB2.0高速和全速，下行端口支持USB2.0高速480Mbps、全速12Mbps和低速1.5Mbps，向下兼容USB1.1协议规范。支持高性能MTT模式（4个TT各对应1个端口，并发处理），为每个端口提供独立TT实现满带宽并发传输，总带宽是STT的4倍。

已验证过的常用设备有：

- 存储设备（U盘、移动硬盘）

- 安卓设备（定时充电、ADB调试）

- iOS设备（定时充电、Xcode调试）

- 加密狗、电子签章（互锁模式）

- 各类USB转串口桥

- J-Link

- DAP-Link

- ST-Link

- XDS110

- USB转CAN



> [!WARNING]
>
> 不支持快充协议，连接手机、平板设备的充电电流等同于直接接到电脑上。

------



## **控制说明**

> [!NOTE]
>
> 下文称智能USB集线器为**设备**。
>
> **设备通信参数：**
>
> - 波特率：115200 - 921600
> - 数据位：8
> - 校验位：无
> - 停止位：1
>
> **设备名称：**
>
> - Windows平台:  `COMx`
> - Linux平台: `/dev/ttyACMx`
> - mac平台: `/dev/cu.usbmodemx`



## 灯语

设备最左侧有一颗指示灯，灯语如下：

| 闪烁规律           | 含义         |
| ------------------ | ------------ |
| 0.5秒亮，0.5秒灭   | 普通模式     |
| 0.25秒亮，0.25秒灭 | 互锁模式     |
| 叠加熄灭           | 接收到数据帧 |



## 按键

设备有4个按键，分别对应4个USB-A通道的控制，以下按键有特殊功能：

| 操作              | 功能                                                    | 默认值   |
| ----------------- | ------------------------------------------------------- | -------- |
| 按键1 上电时按住  | 进入固件升级模式。                                      |          |
| 按键1 长按6秒以上 | 重置设备。                                              |          |
| 按键1 长按3秒以上 | 切换工作模式：普通/互锁，断电仍然有效。                 | 普通模式 |
| 按键2 长按3秒以上 | 启用/关闭通道状态保存功能，上电恢复各个通道原来的状态。 | 不保存   |




## 指令集

设备通过简易的请求-响应通信协议进行交互控制，有以下命令：

| 指令                          | CMD  | 说明                                                       |
| :---------------------------- | ---- | ---------------------------------------------------------- |
| 控制 通道电源                 | 0x01 | 控制指定通道电源的通断                                     |
| 查询 通道电源                 | 0x00 | 查询指定通道的电源通断状态                                 |
| 控制 通道电源互锁             | 0x02 | 同一时刻只有1路通道的电源处于打开状态                      |
| 查询 通道电压                 | 0x03 | 查询指定通道的VBUS电压值 单位：(mv)                        |
| 查询 通道电流                 | 0x04 | 查询指定通道的电流值 单位：(ma)                            |
| 控制 通道数据开关             | 0x05 | 控制通道的数据信号线（D+ D-）的通断                        |
| 查询 通道数据开关             | 0x08 | 查询通道的数据信号线（D+ D-）的通断                        |
| 设置 按键控制                 | 0x09 | 设置能否通过按键控制对应通道                               |
| 查询 按键控制状态             | 0x0A | 查询是否启用按键控制对应通道                               |
| 设置 指定通道上电默认电源状态 | 0x0B | 设置指定通道上电的默认的电源状态                           |
| 查询 指定通道上电默认电源状态 | 0x0C | 查询指定通道上电的默认的电源状态                           |
| 设置 指定通道上电默认数据状态 | 0x0D | 设置指定通道上电的默认的数据状态                           |
| 查询 指定通道上电默认数据状态 | 0x0E | 查询指定通道上电的默认数据开关状态                         |
| 设置 断电保存                 | 0x0F | 设置是否开启断电保存，若开启，则将自动恢复上次掉电前的状态 |
| 查询 断电保存                 | 0x10 | 查询设备断电保存功能是否开启                               |
| 设置 工作模式                 | 0x06 | 设置普通模式/互锁模式                                      |
| 查询 工作模式                 | 0x07 | 获取设备处于普通模式还是互锁模式下                         |
| 查询 固件版本信息             | 0xFD | 查询固件版本号                                             |
| 查询 硬件版本信息             | 0xFE | 查询硬件版本号                                             |

> [!IMPORTANT]
>
> 部分功能需要指定或更高的硬件版本号才可支持：

| 硬件版本   | 电压检测 | 电流检测 | 数据线开关 |
| ---------- | -------- | -------- | ---------- |
| V1.0至V1.2 | 不支持   | 不支持   | 不支持     |
| V1.2       | 支持     | 不支持   | 不支持     |
| V1.3及以上 | 支持     | 支持     | 支持       |

*自2024年12月起的订单，均为V1.3版本。*



## 协议格式

查询、控制、互锁、设置命令的协议格式如下：

| 帧头1 | 帧头2 | CMD              | 通道号                | 通道值      | 附加值          | SUM8 校验和 |
| ----- | ----- | ---------------- | --------------------- | ----------- | --------------- | ----------- |
| 0x55  | 0x5A  | [0x01 0x02 0x03] | [0x01 0x02 0x04 0x08] | [0x00 0x01] | *该字节视指令是否携带 | CMD+CH+data[...]  |



读取通道电压、电流的协议格式如下：

| 帧头1 | 帧头2 | CMD              | 通道号                | 数值 [15:8] | 数值 [7:0] | SUM8 校验和 |
| ----- | ----- | ---------------- | --------------------- | ----------- | ---------- | ----------- |
| 0x55  | 0x5A  | [0x01 0x02 0x03] | [0x01 0x02 0x04 0x08] | MSB         | LSB        | CMD+CH+VAL  |



## 命令示例

> [!NOTE]
>
> - 以下所有数据内容均为**16进制**。
> - 通道值的取值为`Channel_e`，<u>并非通道数字</u>，在控制和获取命令集中可用**位或**批量控制和获取；若设备处于互锁模式，<u>则只能使用互锁控制命令[0x02]，按位与无效</u>。
> - 发送的帧格式或错误命令将不会响应。
> - 按键按下时将会上报当前按下的通道状态[0x00]。
> - 在资料包中的uart_tool中，有串口助手便于快速上手。
> - 提供python控制库[smartusbhub]("https://github.com/MrzhangF1ghter/smartusbhub")

```c
typedef enum
{
    CH1 = 0x01,
    CH2 = 0x02,
    CH3 = 0x04,
    CH4 = 0x08, 
}Channel_e;
```



### 控制通道电源(CMD:0x01)

> [!NOTE]
>
> 若设备处于互锁模式下，则控制指令(CMD:0x01)无效，需要使用互锁控制命令(CMD:0x02)控制；
>
> 若处于互锁模式下，发送控制指令，将会返回指令无效帧：
>
> **指令无效：**
>
> ```
> 55 5A 01 FF FF FF 
> ```

#### 打开通道1电源

##### **命令：**

```
55 5A 01 01 01 03
```

##### 返回：

```
55 5A 01 01 01 03
```

#### 关闭通道1电源

##### **命令：**

```
55 5A 01 01 00 02
```

##### 返回：

```
55 5A 01 01 00 02
```

#### 打开通道2电源

##### **命令：**

```
55 5A 01 02 01 04
```

##### 返回：

```
55 5A 01 02 01 04
```

#### 关闭通道2电源

##### **命令：**

```
55 5A 01 02 00 03
```

##### 返回：

```
55 5A 01 02 00 03
```

#### 打开通道3电源

##### **命令：**

```
55 5A 01 04 01 06
```

##### 返回：

```
55 5A 01 04 01 06
```

#### 关闭通道3电源

##### **命令：**

```
55 5A 01 04 00 05
```

##### 返回：

```
55 5A 01 04 00 05
```

#### 打开通道4电源

##### **命令：**

```
55 5A 01 08 01 0A
```

##### 返回：

```
55 5A 01 08 01 0A
```

#### 关闭通道4电源

##### **命令：**

```
55 5A 01 08 00 09
```

##### 返回：

```
55 5A 01 08 00 09
```

#### 组合控制示例

#### 打开通道1和通道3电源

##### **命令：**

```
55 5A 01 05 01 07
```

##### 返回：

```
55 5A 01 05 01 07
```

#### 关闭通道1和通道3电源

##### **命令：**

```
55 5A 01 05 00 06
```

##### 返回：

```
55 5A 01 05 00 06
```

#### 打开所有通道电源

##### **命令：**

```
55 5A 01 0F 01 11
```

##### 返回：

```
55 5A 01 0F 01 11
```

#### 关闭所有通道电源

##### **命令：**

```
55 5A 01 0F 00 10
```

##### 返回：

```
55 5A 01 0F 00 10
```



### 获取通道电源开关值(CMD:0x00)

#### 获取通道1电源的开关值

##### **命令：**

```
55 5A 00 01 00 01
```

##### 返回：

如果通道1电源关闭：

```
55 5A 00 01 00 01
```

如果通道1电源打开：

```
55 5A 00 01 01 02
```

#### 获取通道2电源的开关值

##### **命令：**

```
55 5A 00 02 00 02
```

##### 返回：

如果通道2电源关闭：

```
55 5A 00 02 00 02
```

如果通道2电源打开：

```
55 5A 00 02 01 03
```

#### 获取通道3电源的开关值

##### **命令：**

```
55 5A 00 04 00 04
```

##### 返回：

如果通道3电源关闭：

```
55 5A 00 04 00 04
```

如果通道3电源打开：

```
55 5A 00 04 01 05
```

#### 获取通道4电源的开关值

##### **命令：**

```
55 5A 00 08 00 08
```

##### 返回：

如果通道4电源关闭：

```
55 5A 00 08 00 08
```

如果通道4电源打开：

```
55 5A 00 08 01 09
```

#### 组合控制示例：

#### 获取所有通道的电源开关值

##### **命令：**

```
55 5A 00 0F 00 0F
```

##### 返回：

```
55 5A 00 01 01 02 
55 5A 00 02 00 02 
55 5A 00 04 00 04 
55 5A 00 08 01 09 
```

通道1电源：打开

通道2电源：关闭 

通道3电源：关闭 

通道4电源：打开



### 控制通道数据(CMD:0x05)

设备可控制指定通道的数据信号（D+ D-）的通断，从而实现保持供电但数据断开的应用需求。

> [!NOTE]
>
> 1. 设备默认每个通道数据信号是连通的，除非用户发送控制通道数据开关指令(CMD:0x05)。
> 2. 如果启用断电保存，数据开关状态将记忆。

#### 打开通道1数据

##### **命令：**

```
55 5A 05 01 01 07
```

##### 返回：

```
55 5A 05 01 01 07
```

#### 关闭通道1数据

##### **命令：**

```
55 5A 05 01 00 06
```

##### 返回：

```
55 5A 05 01 00 06
```

#### 打开通道2数据

##### **命令：**

```
55 5A 05 02 01 08
```

##### 返回：

```
55 5A 05 02 01 08
```

#### 关闭通道2数据

##### **命令：**

```
55 5A 05 02 00 07
```

##### 返回：

```
55 5A 05 02 00 07
```

#### 打开通道3数据

##### **命令：**

```
55 5A 05 04 01 0A
```

##### 返回：

```
55 5A 05 04 01 0A
```

#### 关闭通道3数据

##### **命令：**

```
55 5A 05 04 00 09
```

##### 返回：

```
55 5A 05 04 00 09
```

#### 打开通道4数据

##### **命令：**

```
55 5A 05 08 01 0E
```

##### 返回：

```
55 5A 05 08 01 0E
```

#### 关闭通道4数据

##### **命令：**

```
55 5A 05 08 00 0D
```

##### 返回：

```
55 5A 05 08 00 0D
```

#### 组合控制示例：

#### 打开所有通道数据

##### **命令：**

```
55 5A 05 0F 01 15
```

##### 返回：

```
55 5A 05 0F 01 15
```

#### 关闭所有通道数据

##### **命令：**

```
55 5A 05 0F 00 14
```

##### 返回：

```
55 5A 05 0F 00 14
```



### 获取通道数据开关值(CMD:0x08)

#### 获取通道1数据的开关值

##### **命令：**

```
55 5A 08 01 00 09
```

##### 返回：

如果通道1数据关闭：

```
55 5A 08 01 00 09
```

如果通道1数据打开：

```
55 5A 08 01 01 0A
```

#### 获取通道2数据的开关值

##### **命令：**

```
55 5A 08 02 00 0A
```

##### 返回：

如果通道2数据关闭：

```
55 5A 08 02 00 0A
```

如果通道2数据打开：

```
55 5A 08 02 01 0B
```

#### 获取通道3数据的开关值

##### **命令：**

```
55 5A 08 04 00 0C
```

##### 返回：

如果通道3数据关闭：

```
55 5A 08 04 00 0C
```

如果通道3数据打开：

```
55 5A 08 04 01 0D
```

#### 获取通道4数据的开关值

##### **命令：**

```
55 5A 08 08 00 10
```

##### 返回：

如果通道4数据关闭：

```
55 5A 08 08 00 10
```

如果通道4数据打开：

```
55 5A 08 08 01 11
```

#### 组合控制示例：

#### 获取所有通道的数据开关值

##### **命令：**

```
55 5A 08 0F 00 17
```

##### 返回：

```
55 5A 08 01 01 0A
55 5A 08 02 01 0B
55 5A 08 04 01 0D
55 5A 08 08 01 11 
```

通道1数据：打开

通道2数据：打开 

通道3数据：打开 

通道4数据：打开



### 互锁控制(CMD:0x02)

#### 打开通道1电源，其余通道关闭

##### **命令：**

```
55 5A 02 01 01 04
```

##### 返回：

```
55 5A 02 01 01 04
```

#### 打开通道2电源，其余通道关闭

##### **命令：**

```
55 5A 02 02 01 05
```

##### 返回：

```
55 5A 02 02 01 05
```

#### 打开通道3电源，其余通道关闭

##### **命令：**

```
55 5A 02 04 01 07 
```

##### 返回：

```
55 5A 02 04 01 07 
```

#### 打开通道4电源，其余通道关闭

##### **命令：**

```
55 5A 02 08 01 0B
```

##### 返回：

```
55 5A 02 08 01 0B
```



#### 关闭所有通道

##### **命令：**

```
55 5A 02 0F 01 12
```

##### 返回：

```
55 5A 02 0F 01 12
```



### 获取通道电压(CMD:0x03)

设备可测量每一路通道输出端(VBUS)的电压值，可用于判断总线是否正常。

*电压分辨率目前为0.1V*

#### 查询通道1的电压值：

**命令：**

```
55 5A 03 01 00 04
```

##### 返回：

```
55 5A 03 01 13 56 6D
```

通道1电压值为：0x1356 = 4950mv (通道打开)

#### 查询通道2的电压值：

**命令：**

```
55 5A 03 02 00 05
```

##### 返回：

```
55 5A 03 02 00 0C 11 
```

通道2电压值为：0x000C = 12mv (通道关闭)

#### 查询通道3的电压值：

**命令：**

```
55 5A 03 04 00 07 
```

##### 返回：

```
55 5A 03 04 00 09 10
```

通道3电压值为：0x0009  = 9mv (通道关闭)

#### 查询通道4的电压值：

**命令：**

```
55 5A 03 08 00 0B  
```

##### 返回：

```
55 5A 03 08 00 08 13
```

通道4电压值为：0x0008  = 8mv (通道关闭)



### 获取通道电流(CMD:0x04)

设备可测量每一路通道的电流值，可用于判断设备工作状态。
*电流分辨率目前为0.1A*

#### 查询通道1的电流值：

**命令：**

```
55 5A 04 01 00 05  
```

##### 返回：

```
55 5A 04 01 01 29 2F
```

通道1电流值为：0x0129  = 297ma

#### 查询通道2的电流值：

**命令：**

```
55 5A 04 02 00 06  
```

##### 返回：

```
55 5A 04 02 00 00 06
```

通道2电流值为：0x0000  = 0ma 

#### 查询通道3的电流值：

**命令：**

```
55 5A 04 04 00 08  
```

##### 返回：

```
55 5A 04 04 00 00 08
```

通道3电流值为：0x0000  = 0ma 

#### 查询通道4的电流值：

**命令：**

```
55 5A 04 08 00 0C 
```

##### 返回：

```
55 5A 04 08 00 00 0C
```

通道4电流值为：0x0000  = 0ma 



### 禁用/启用按键控制(CMD:0x09)

> [!NOTE]
>
> 1. 设备默认能通过按键控制对应通道。
>
> 2. 该配置影响范围为所有按键及通道。
>
> 3. 长按功能不受影响。
>
> 4. 该指令断电仍然保存。

#### 禁用通过按键控制

##### **命令：**

```
55 5A 09 00 00 09
```

##### 返回：

```
55 5A 09 00 00 09
```

#### 启用通过按键控制

##### **命令：**

```
55 5A 09 00 01 0A
```

##### 返回：

```
55 5A 09 00 01 0A
```



### 查询按键控制状态(CMD:0x0A)

##### **命令：**

```
55 5A 0A 00 00 0A
```

##### 返回：

启用按键控制

```
55 5A 0A 00 01 0B
```

禁用按键控制

```
55 5A 0A 00 00 0A
```



### 设置指定通道上电的默认的电源状态(CMD:0x0B)

> [!NOTE]
>
> 在系统上电后的通道状态判断中，**默认通道状态优先级高于断电保存功能**。当默认通道状态功能开启时，即使断电保存功能也处于开启状态，系统上电后仍将按照默认通道状态决定各通道电源或数据的开启/关闭状态。
>
> 当**默认通道状态功能关闭**时，通道的上电状态将依据断电保存功能的设置决定。若断电保存功能也处于关闭状态（默认配置），则系统上电后**所有通道默认保持关闭状态**。



#### 设置通道1电源的默认值为打开


##### **命令：**

```
55 5A 0B 01 01 01 0E
```

##### 返回：

```
55 5A 0B 01 01 01 0E
```



#### 设置通道1电源的默认值为关闭


##### **命令：**

```
55 5A 0B 01 01 00 0D
```

##### 返回：

```
55 5A 0B 01 01 00 0D
```



#### 设置通道2电源的默认值为打开


##### **命令：**

```
55 5A 0B 02 01 01 0F
```

##### 返回：

```
55 5A 0B 02 01 01 0F
```



#### 设置通道2电源的默认值为关闭


##### **命令：**

```
55 5A 0B 02 01 00 0E
```

##### 返回：

```
55 5A 0B 02 01 00 0E
```



#### 设置通道3电源的默认值为打开


##### **命令：**

```
55 5A 0B 04 01 01 11
```

##### 返回：

```
55 5A 0B 04 01 01 11
```



#### 设置通道3电源的默认值为关闭


##### **命令：**

```
55 5A 0B 04 00 00 0F
```

##### 返回：

```
55 5A 0B 04 00 00 0F
```



#### 设置通道4电源的默认值为打开


##### **命令：**

```
55 5A 0B 08 01 01 15
```

##### 返回：

```
55 5A 0B 08 01 01 15
```



#### 设置通道4电源的默认值为关闭


##### **命令：**

```
55 5A 0B 08 01 00 14
```

##### 返回：

```
55 5A 0B 08 01 00 14
```



#### 设置所有通道电源的默认值为打开


##### **命令：**

```
55 5A 0B 0F 01 01 1C
```

##### 返回：

```
55 5A 0B 0F 01 01 1C
```



#### 设置所有通道电源的默认值为关闭


##### **命令：**

```
55 5A 0B 0F 01 00 1B
```

##### 返回：

```
55 5A 0B 0F 01 00 1B
```



#### 禁用通道1电源使用默认值


##### **命令：**

```
55 5A 0B 01 00 00 0C
```

##### 返回：

```
55 5A 0B 01 00 00 0C
```



#### 禁用通道2电源使用默认值


##### **命令：**

```
55 5A 0B 02 00 00 0D
```

##### 返回：

```
55 5A 0B 02 00 00 0D
```



#### 禁用通道3电源使用默认值


##### **命令：**

```
55 5A 0B 04 00 00 0F
```

##### 返回：

```
55 5A 0B 04 00 00 0F
```



#### 禁用通道4电源使用默认值


##### **命令：**

```
55 5A 0B 08 00 00 13
```

##### 返回：

```
55 5A 0B 08 00 00 13
```



#### 禁用所有通道电源使用默认值


##### **命令：**

```
55 5A 0B 0F 00 00 1A
```

##### 返回：

```
55 5A 0B 0F 00 00 1A
```



### 设置断电保存(CMD:0x0F)

> [!NOTE]
>
> 此功能可通过长按按键2开启或者关闭，开启后，将自动保存当前的通道状态，重新上电将会恢复所有通道断电之前的状态
> 



#### 启用断电保存


##### **命令：**

```
55 5A 0F 00 01 10
```

##### 返回：

```
55 5A 0F 00 01 10
```



#### 关闭断电保存


##### **命令：**

```
55 5A 0F 00 00 0F
```

##### 返回：

```
55 5A 0F 00 00 0F
```



### 查询断电保存状态(CMD:0x10)


##### **命令：**

```
55 5A 10 00 00 10
```

##### 返回：

断电保存启用

```
55 5A 10 00 01 11
```

断电保存禁用

```
55 5A 10 00 00 10
```



### 设置工作模式(CMD:0x06)

> [!NOTE]
>
> 设备两种工作模式：
>
> 1. 普通模式：该模式每个通道都可任意控制。
> 2. 互锁模式：该模式下各个通道为互斥状态，同一时刻只有一个通道打开。
>
> - 该指令断电仍然保存。
> - 可以通过长按`按键1`3秒以上切换工作模式，可通过指示灯状态确定当前工作模式。



#### 设置普通模式

##### **命令：**

```
55 5A 06 00 00 06
```

##### 返回：

```
55 5A 06 00 00 06
```

#### 设置互锁模式

##### **命令：**

```
55 5A 06 00 01 07
```

##### 返回：

```
55 5A 06 00 01 07
```



### 获取工作模式(CMD:0x07)

##### **命令：**

```
55 5A 07 00 00 07
```

##### 返回：

设备处于普通模式下：

```
55 5A 07 00 00 07
```

设备处于互锁模式下：

```
55 5A 07 00 01 08
```



### 获取固件版本(CMD:0xFD)

##### **命令：**

```
55 5A FD 00 00 FD
```

##### 返回：

```
55 5A FD 00 0F 0C
```

固件版本号：15



### 获取硬件版本(CMD:0xFE)

##### **命令：**

```
55 5A FE 00 00 FE
```

##### 返回：

```
55 5A FE 00 03 01
```

硬件版本号：3 / V1.3



### 笔记:

此页为空白页
