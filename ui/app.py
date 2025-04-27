#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主应用启动文件
"""

import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入UI模块
from ui.obfuscator_ui import ObfuscatorUI


def main():
    app = ObfuscatorUI()
    app.mainloop()


if __name__ == "__main__":
    main() 