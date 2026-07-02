#!/usr/bin/env python3
"""
测试小米设备连接的脚本
用于验证设备IP和Token是否正确
"""

import sys
import subprocess

def test_device(ip, token):
    """测试设备连接"""
    print(f"测试连接到设备: {ip}")
    print(f"Token: {token[:8]}...{token[-8:]}")
    print()
    
    # 使用miiocli测试连接
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
            print()
            print("设备信息：")
            print(result.stdout)
            return True
        else:
            print("❌ 设备连接失败")
            print()
            print("错误信息：")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 连接超时，请检查：")
        print("1. 设备IP地址是否正确")
        print("2. 设备是否在同一局域网")
        print("3. 设备是否在线")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("用法: python3 test_device.py <IP地址> <Token>")
        print()
        print("示例:")
        print("python3 test_device.py 192.168.1.100 0123456789abcdef0123456789abcdef")
        sys.exit(1)
    
    ip = sys.argv[1]
    token = sys.argv[2]
    
    if len(token) != 32:
        print("❌ Token长度错误，应该是32位十六进制字符串")
        sys.exit(1)
    
    success = test_device(ip, token)
    
    if success:
        print()
        print("🎉 设备配置正确！")
        print("现在可以运行主程序来设置自动化了。")
    else:
        print()
        print("请检查设备信息后重试。")

if __name__ == "__main__":
    main()
