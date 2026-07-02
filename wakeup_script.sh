#!/bin/bash
# Mac唤醒/亮屏时调用 - 打开小米显示器挂灯

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
/opt/homebrew/bin/python3.11 "$SCRIPT_DIR/mi_light_controller.py" on
