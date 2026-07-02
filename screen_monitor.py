#!/opt/homebrew/bin/python3.11
# -*- coding: utf-8 -*-
"""
Mac屏幕状态监听器
监听锁屏/解锁/熄屏/亮屏事件，控制小米显示器挂灯
"""

import signal
import sys
import os
import subprocess
import objc

# 控制脚本路径
CONTROLLER = "/Users/sxq/mi_light_control/mi_light_controller.py"
# 日志文件
LOG_FILE = os.path.expanduser("~/.mi_light_control.log")


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
    try:
        subprocess.run(
            ["/opt/homebrew/bin/python3.11", CONTROLLER, action],
            capture_output=True,
            timeout=15
        )
    except Exception as e:
        log(f"❌ 控制挂灯失败: {e}")


def main():
    from Foundation import NSObject, NSRunLoop, NSDate
    from AppKit import NSWorkspace
    import Quartz

    class ScreenObserver(NSObject):
        def screenLocked_(self, notification):
            log("🔒 锁屏 - 关闭挂灯")
            control_light("off")

        def screenUnlocked_(self, notification):
            log("🔓 解锁 - 打开挂灯")
            control_light("on")

        def screensaverStarted_(self, notification):
            log("🌙 屏保启动 - 关闭挂灯")
            control_light("off")

        def screensaverStopped_(self, notification):
            log("☀️ 屏保停止 - 打开挂灯")
            control_light("on")

    observer = ScreenObserver.alloc().init()

    nc = Quartz.NSDistributedNotificationCenter.defaultCenter()

    # 锁屏
    nc.addObserver_selector_name_object_(
        observer,
        objc.selector(observer.screenLocked_, signature=b'v@:@'),
        "com.apple.screenIsLocked",
        None
    )

    # 解锁
    nc.addObserver_selector_name_object_(
        observer,
        objc.selector(observer.screenUnlocked_, signature=b'v@:@'),
        "com.apple.screenIsUnlocked",
        None
    )

    # 屏保启动
    nc.addObserver_selector_name_object_(
        observer,
        objc.selector(observer.screensaverStarted_, signature=b'v@:@'),
        "com.apple.screensaver.didstart",
        None
    )

    # 屏保停止
    nc.addObserver_selector_name_object_(
        observer,
        objc.selector(observer.screensaverStopped_, signature=b'v@:@'),
        "com.apple.screensaver.didstop",
        None
    )

    log("✅ 屏幕状态监听器已启动")
    log("  - 锁屏/熄屏 → 关闭挂灯")
    log("  - 解锁/亮屏 → 打开挂灯")
    log("  - 屏保启动 → 关闭挂灯")
    log("  - 屏保停止 → 打开挂灯")

    # 优雅退出
    def signal_handler(sig, frame):
        log("🛑 屏幕状态监听器已停止")
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # 运行事件循环
    try:
        while True:
            NSRunLoop.currentRunLoop().runUntilDate_(
                NSDate.dateWithTimeIntervalSinceNow_(1.0)
            )
    except KeyboardInterrupt:
        log("🛑 屏幕状态监听器已停止")


if __name__ == "__main__":
    main()
