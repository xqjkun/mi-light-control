# 小米智能显示器挂灯1S - Mac自动控制

> Mac 锁屏/熄屏/睡眠时自动关闭挂灯，解锁/亮屏/唤醒时自动打开挂灯

## 功能

| 触发事件 | 灯光动作 | 实现方式 |
|---------|---------|---------|
| 🔒 锁屏 (`⌃⌘Q`) | 关灯 | screen_monitor.py |
| 🔓 解锁 | 开灯 | screen_monitor.py |
| 🖥️ 熄屏 | 关灯 | screen_monitor.py |
| 🖥️ 亮屏 | 开灯 | screen_monitor.py |
| 🌙 屏保启动 | 关灯 | screen_monitor.py |
| ☀️ 屏保停止 | 开灯 | screen_monitor.py |
| 💤 合盖/睡眠 | 关灯 | sleepwatcher |
| ⏰ 开盖/唤醒 | 开灯 | sleepwatcher |

## 架构

```
Mac 系统事件
    │
    ├── sleepwatcher ──→ ~/.sleep / ~/.wakeup
    │
    └── screen_monitor.py ──→ 锁屏/解锁通知
            │
            ▼
    mi_light_controller.py
            │
            ▼
      mijiaAPI (云端控制)
            │
            ▼
    小米智能显示器挂灯1S
```

## 前置条件

- macOS（已测试 arm64）
- Homebrew
- Python 3.11
- 小米账号（已绑定设备）
- Mac 和挂灯**无需同一局域网**（通过云端控制）

## 安装

### 1. 安装依赖

```bash
# 安装 sleepwatcher（监听睡眠/唤醒）
brew install sleepwatcher

# 安装 Python 依赖
/opt/homebrew/bin/python3.11 -m pip install mijiaAPI pyobjc-framework-Quartz
```

### 2. 登录小米账号

```bash
/opt/homebrew/bin/python3.11 -m mijiaAPI login
```

用米家 App 扫码登录，认证信息保存在 `~/.config/mijia-api/auth.json`

### 3. 确认设备

```bash
/opt/homebrew/bin/python3.11 -m mijiaAPI -l
```

找到你的 **米家智能显示器挂灯1S**，记录 DID 号。

### 4. 修改配置

编辑 `mi_light_controller.py`，修改 `DEVICE_DID`：

```python
# 设备DID（从设备列表中获取）
DEVICE_DID = "你的设备DID"
```

### 5. 启动服务

```bash
# 复制 sleep/wakeup 脚本
cp ~/mi_light_control/sleep_script.sh ~/.sleep
cp ~/mi_light_control/wakeup_script.sh ~/.wakeup
chmod +x ~/.sleep ~/.wakeup

# 启动 sleepwatcher
brew services start sleepwatcher

# 加载屏幕监听器（开机自启）
launchctl load ~/Library/LaunchAgents/com.milight.screenmonitor.plist
```

## 文件结构

```
~/mi_light_control/
├── mi_light_controller.py   # 灯光控制脚本（核心）
├── screen_monitor.py        # 锁屏/解锁监听器
├── sleep_script.sh          # 睡眠时执行
├── wakeup_script.sh         # 唤醒时执行
└── README.md

~/.config/mijia-api/
└── auth.json                # 小米账号认证文件

~/.sleep                     # sleepwatcher 睡眠脚本
~/.wakeup                    # sleepwatcher 唤醒脚本
~/.mi_light_control.log      # 控制日志
~/.mi_light_monitor.log      # 监听器日志

~/Library/LaunchAgents/
└── com.milight.screenmonitor.plist  # 开机自启配置
```

## 手动测试

```bash
# 开灯
/opt/homebrew/bin/python3.11 ~/mi_light_control/mi_light_controller.py on

# 关灯
/opt/homebrew/bin/python3.11 ~/mi_light_control/mi_light_controller.py off
```

## 查看日志

```bash
# 实时查看控制日志
tail -f ~/.mi_light_control.log

# 查看监听器日志
cat ~/.mi_light_monitor.log
```

## 服务管理

### sleepwatcher（睡眠/唤醒）

```bash
brew services list | grep sleepwatcher   # 查看状态
brew services start sleepwatcher         # 启动
brew services stop sleepwatcher          # 停止
brew services restart sleepwatcher       # 重启
```

### screen_monitor（锁屏/解锁）

```bash
launchctl list | grep milight            # 查看状态
launchctl load ~/Library/LaunchAgents/com.milight.screenmonitor.plist    # 启动
launchctl unload ~/Library/LaunchAgents/com.milight.screenmonitor.plist  # 停止
```

## 故障排除

### 灯没有反应

```bash
# 1. 检查手动控制是否正常
/opt/homebrew/bin/python3.11 ~/mi_light_control/mi_light_controller.py on

# 2. 检查认证文件
ls -la ~/.config/mijia-api/auth.json

# 3. 重新登录
/opt/homebrew/bin/python3.11 -m mijiaAPI login
```

### 监听器没有响应

```bash
# 1. 检查进程是否运行
ps aux | grep screen_monitor | grep -v grep

# 2. 查看日志
cat ~/.mi_light_control.log

# 3. 重启监听器
launchctl unload ~/Library/LaunchAgents/com.milight.screenmonitor.plist
launchctl load ~/Library/LaunchAgents/com.milight.screenmonitor.plist
```

### sleepwatcher 没有响应

```bash
# 1. 检查服务状态
brew services list | grep sleepwatcher

# 2. 检查脚本权限
ls -la ~/.sleep ~/.wakeup

# 3. 重启服务
brew services restart sleepwatcher
```

## 卸载

```bash
# 停止服务
brew services stop sleepwatcher
launchctl unload ~/Library/LaunchAgents/com.milight.screenmonitor.plist

# 删除文件
rm -rf ~/mi_light_control
rm -f ~/.sleep ~/.wakeup
rm -f ~/.mi_light_control.log ~/.mi_light_monitor.log
rm -f ~/Library/LaunchAgents/com.milight.screenmonitor.plist

# 可选：卸载依赖
brew uninstall sleepwatcher
/opt/homebrew/bin/python3.11 -m pip uninstall mijiaAPI pyobjc-framework-Quartz pyobjc-core pyobjc-framework-Cocoa
```

## 技术栈

- **sleepwatcher** - Mac 睡眠/唤醒事件监听
- **mijiaAPI** - 小米设备云端控制（[GitHub](https://github.com/Do1e/mijia-api)）
- **PyObjC** - macOS 原生通知监听（锁屏/解锁）
- **launchd** - macOS 服务管理（开机自启）

## License

MIT
