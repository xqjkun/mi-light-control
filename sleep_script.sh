#!/bin/bash
# Mac睡眠/熄屏/锁屏时调用 - 关闭小米显示器挂灯

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
/opt/homebrew/bin/python3.11 "$SCRIPT_DIR/mi_light_controller.py" off
