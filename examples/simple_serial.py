# Description: a very simple serial communication example to control the power of each channel of the SmartUSBHub
# copyright: (c) 2024 EmbeddedTec studio
# license: Apache-2.0
# version: 1.0
# author: EmbeddedTec studio
# email:embeddedtec@outlook.com

import serial
import time

serial_port = "/dev/cu.usbmodem413101"  # 替换为你的实际串口
baud_rate = 115200  # 波特率

# 命令
get_mode_cmd = "55 5A 07 00 00 07" #查询工作模式命令
ch1_on_cmd = "55 5A 01 01 01 03"  # 通道1 开命令
ch1_off_cmd = "55 5A 01 01 00 02"  # 通道1 关命令

def hex_str_to_bytes(hex_str):
    """
    将十六进制字符串转换为字节数组。
    """
    return bytes.fromhex(hex_str)

def bytes_to_hex_str(byte_data):
    """
    将字节数组转换为十六进制字符串。
    """
    return " ".join(f"{b:02X}" for b in byte_data)

try:
    # 打开串口
    s = serial.Serial(serial_port, baudrate=baud_rate, timeout=1)
    # 检查并关闭之前的连接
    if s.is_open:
        s.close()
    s.open()

    print("串口已打开")

    # 发送计数器
    send_count = 0
    current_cmd = ch1_off_cmd  # 初始状态：发送关命令

    while True:
        # 转换命令为字节
        byte_cmd = hex_str_to_bytes(current_cmd)

        # 发送命令
        bytes_written = s.write(byte_cmd)
        send_count += 1  # 每发送一次计数器加 1

        # 接收应答
        response = s.read(len(byte_cmd))  # 假设应答长度与发送命令长度一致
        if response:
            response_str = bytes_to_hex_str(response)
            if response_str == current_cmd:  # 校验应答数据
                status = f"发送 {send_count}: {current_cmd} | 应答成功: {response_str}"
            else:
                status = f"发送 {send_count}: {current_cmd} | 应答失败: {response_str}"
                raise ValueError(f"应答校验失败！发送: {current_cmd}，接收: {response_str}")
        else:
            status = f"发送 {send_count}: {current_cmd} | 未接收到应答数据"

        # 在同一行打印状态并刷新
        print(f"\r{status}", end="", flush=True)

        # 切换命令
        current_cmd = ch1_on_cmd if current_cmd == ch1_off_cmd else ch1_off_cmd

        # 每隔 10ms 发送一次
        time.sleep(0.01)

except serial.SerialException as e:
    print(f"\n串口错误: {e}")
except ValueError as e:
    print(f"\n错误: {e}")
    print("程序退出")
except KeyboardInterrupt:
    print("\n程序被中断")
except Exception as e:
    print(f"\n其他错误: {e}")
finally:
    # 关闭串口
    if 's' in locals() and s.is_open:
        s.close()
        print("\n串口已关闭")