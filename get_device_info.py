#!/usr/bin/env python3
"""
获取小米设备信息的脚本
用于获取设备的IP地址和Token
"""

import sys
import subprocess
import json

def get_device_info():
    """获取小米设备信息"""
    print("=" * 60)
    print("小米设备信息获取工具")
    print("=" * 60)
    print()
    print("由于自动发现可能失败，请按以下步骤手动获取设备信息：")
    print()
    print("方法1：通过米家App获取（推荐）")
    print("-" * 40)
    print("1. 打开米家App")
    print("2. 找到你的小米智能显示器挂灯1s")
    print("3. 点击右上角 '...' -> '关于'")
    print("4. 记录下 IP地址")
    print()
    print("方法2：通过路由器获取IP")
    print("-" * 40)
    print("1. 登录路由器管理界面")
    print("2. 查看已连接设备列表")
    print("3. 找到小米挂灯的IP地址")
    print()
    print("方法3：获取Token（高级）")
    print("-" * 40)
    print("Token是设备的密钥，用于局域网控制")
    print("获取方法：")
    print("1. 安装米家App的旧版本（5.4.19或更早）")
    print("2. 登录小米账号")
    print("3. 在设备详情页可以看到Token")
    print("4. 或者使用第三方工具如 'miio' 获取")
    print()
    print("=" * 60)
    print("获取到信息后，请运行以下命令测试连接：")
    print()
    print("python3 test_device.py <IP地址> <Token>")
    print()
    print("例如：")
    print("python3 test_device.py 192.168.1.100 0123456789abcdef0123456789abcdef")
    print("=" * 60)

if __name__ == "__main__":
    get_device_info()
