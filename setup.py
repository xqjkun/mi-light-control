#!/usr/bin/env python3
"""
小米智能显示器挂灯1s 自动化设置脚本
用于配置设备信息和安装自动化服务
"""

import json
import os
import sys
import subprocess

CONFIG_FILE = os.path.expanduser("~/.mi_light_config.json")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_user_input():
    """获取用户输入"""
    print("=" * 60)
    print("小米智能显示器挂灯1s 自动化设置")
    print("=" * 60)
    print()
    
    # 获取IP地址
    while True:
        ip = input("请输入挂灯的IP地址: ").strip()
        if ip:
            # 简单验证IP格式
            parts = ip.split('.')
            if len(parts) == 4 and all(0 <= int(p) <= 255 for p in parts):
                break
            else:
                print("❌ IP地址格式错误，请重新输入")
        else:
            print("❌ IP地址不能为空")
    
    # 获取Token
    while True:
        token = input("请输入挂灯的Token (32位十六进制): ").strip()
        if token and len(token) == 32:
            # 验证是否为十六进制
            try:
                int(token, 16)
                break
            except ValueError:
                print("❌ Token必须是十六进制字符串")
        else:
            print("❌ Token长度必须为32位")
    
    return ip, token

def save_config(ip, token):
    """保存配置文件"""
    config = {
        'ip': ip,
        'token': token
    }
    
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ 配置已保存到: {CONFIG_FILE}")
        return True
    except Exception as e:
        print(f"❌ 保存配置失败: {e}")
        return False

def test_connection(ip, token):
    """测试设备连接"""
    print()
    print("正在测试设备连接...")
    
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/python3.11", "-m", "miio", "device", "info",
             "--ip", ip, "--token", token],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ 设备连接成功！")
            return True
        else:
            print("❌ 设备连接失败")
            print(f"错误: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 连接超时")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def setup_sleepwatcher():
    """配置sleepwatcher"""
    print()
    print("配置sleepwatcher...")
    
    # 创建睡眠脚本
    sleep_script = os.path.expanduser("~/.sleep")
    wakeup_script = os.path.expanduser("~/.wakeup")
    
    # 复制脚本到用户目录
    try:
        # 复制睡眠脚本
        subprocess.run(["cp", os.path.join(SCRIPT_DIR, "sleep_script.sh"), sleep_script], check=True)
        subprocess.run(["chmod", "+x", sleep_script], check=True)
        
        # 复制唤醒脚本
        subprocess.run(["cp", os.path.join(SCRIPT_DIR, "wakeup_script.sh"), wakeup_script], check=True)
        subprocess.run(["chmod", "+x", wakeup_script], check=True)
        
        print("✅ 睡眠/唤醒脚本已配置")
        return True
    except Exception as e:
        print(f"❌ 配置sleepwatcher失败: {e}")
        return False

def start_sleepwatcher():
    """启动sleepwatcher服务"""
    print()
    print("启动sleepwatcher服务...")
    
    try:
        result = subprocess.run(
            ["brew", "services", "start", "sleepwatcher"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ sleepwatcher服务已启动")
            return True
        else:
            print("❌ 启动sleepwatcher服务失败")
            print(f"错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 启动服务失败: {e}")
        return False

def main():
    print("欢迎使用小米智能显示器挂灯1s 自动化设置工具")
    print()
    
    # 检查是否已有配置
    if os.path.exists(CONFIG_FILE):
        print(f"检测到已有配置文件: {CONFIG_FILE}")
        choice = input("是否重新配置？(y/N): ").strip().lower()
        if choice != 'y':
            print("使用现有配置")
            return
    
    # 获取用户输入
    ip, token = get_user_input()
    
    # 测试连接
    if not test_connection(ip, token):
        print()
        choice = input("连接测试失败，是否仍要保存配置？(y/N): ").strip().lower()
        if choice != 'y':
            print("设置已取消")
            return
    
    # 保存配置
    if not save_config(ip, token):
        return
    
    # 配置sleepwatcher
    if not setup_sleepwatcher():
        return
    
    # 启动sleepwatcher
    if not start_sleepwatcher():
        return
    
    print()
    print("=" * 60)
    print("🎉 设置完成！")
    print("=" * 60)
    print()
    print("自动化功能已启用：")
    print("- Mac睡眠时 → 挂灯自动关闭")
    print("- Mac唤醒时 → 挂灯自动打开")
    print()
    print("日志文件位置：")
    print(f"- 睡眠日志: ~/.mi_light_sleep.log")
    print(f"- 唤醒日志: ~/.mi_light_wakeup.log")
    print()
    print("配置文件位置：")
    print(f"- {CONFIG_FILE}")
    print()
    print("测试命令：")
    print(f"- 打开灯: python3 {SCRIPT_DIR}/mi_light_controller.py on")
    print(f"- 关闭灯: python3 {SCRIPT_DIR}/mi_light_controller.py off")
    print("=" * 60)

if __name__ == "__main__":
    main()
