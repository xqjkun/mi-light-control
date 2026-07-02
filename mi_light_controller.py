#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小米智能显示器挂灯控制器
通过 mijiaAPI 云端控制，无需IP和Token
"""

import sys
import os
import json

# 配置文件路径
CONFIG_FILE = os.path.expanduser("~/.mi_light_config.json")
# 日志文件
LOG_FILE = os.path.expanduser("~/.mi_light_control.log")


def load_config():
    """加载配置文件"""
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ 未找到配置文件: {CONFIG_FILE}")
        print("请先创建配置文件，参考 config.example.json")
        print()
        print("步骤：")
        print("1. 运行: /opt/homebrew/bin/python3.11 -m mijiaAPI login")
        print("2. 运行: /opt/homebrew/bin/python3.11 -m mijiaAPI -l")
        print("3. 找到你的设备DID号")
        print(f"4. 创建配置文件: {CONFIG_FILE}")
        sys.exit(1)

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        sys.exit(1)


def log(msg):
    """记录日志"""
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(line + '\n')
    except:
        pass


def control_light(action):
    """控制挂灯"""
    config = load_config()
    device_did = config.get("device_did")

    if not device_did:
        log("❌ 配置文件缺少 device_did")
        return False

    try:
        from mijiaAPI import mijiaAPI, mijiaDevice
    except ImportError:
        log("❌ 未安装 mijiaAPI，请运行: pip3 install mijiaAPI")
        return False

    try:
        api = mijiaAPI()
        api.login()

        device = mijiaDevice(did=device_did, api=api)

        if action == "on":
            device.on = True
            log("✅ 挂灯已打开")
        elif action == "off":
            device.on = False
            log("✅ 挂灯已关闭")
        else:
            log(f"❌ 未知操作: {action}")
            return False

        return True

    except Exception as e:
        log(f"❌ 控制失败: {e}")
        return False


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("on", "off"):
        print("用法: mi_light_controller.py <on|off>")
        sys.exit(1)

    action = sys.argv[1]
    success = control_light(action)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
