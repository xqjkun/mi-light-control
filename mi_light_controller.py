#!/opt/homebrew/bin/python3.11
# -*- coding: utf-8 -*-
"""
小米智能显示器挂灯1S 控制器
通过 mijiaAPI 云端控制，无需IP和Token
"""

import sys
import os

# 设备DID（从设备列表中获取）
DEVICE_DID = "874303445"
# 认证文件路径
AUTH_FILE = os.path.expanduser("~/.config/mijia-api/auth.json")
# 日志文件
LOG_FILE = os.path.expanduser("~/.mi_light_control.log")


def log(msg):
    """记录日志"""
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(line + '\n')
    except:
        pass


def control_light(action):
    """控制挂灯"""
    try:
        from mijiaAPI import mijiaAPI, mijiaDevice
    except ImportError:
        log("❌ 未安装 mijiaAPI，请运行: pip3 install mijiaAPI")
        return False

    if not os.path.exists(AUTH_FILE):
        log(f"❌ 未找到认证文件: {AUTH_FILE}")
        log("请先运行: /opt/homebrew/bin/python3.11 -m mijiaAPI login")
        return False

    try:
        api = mijiaAPI()
        api.login()

        device = mijiaDevice(did=DEVICE_DID, api=api)

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
