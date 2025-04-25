# Python代码混淆器

这是一个Python代码混淆工具，集成了多种混淆技术，包括代码平坦化技术（Control Flow Flattening）、函数名替换和字节码级混淆，增加代码的理解难度，同时保持原始功能不变。

## 功能特点

- 将Python代码的控制流结构扁平化
- 引入状态变量和状态机结构替代原始控制流
- 随机化状态变量名称，增加逆向分析难度
- 使用随机字符串替换函数名
- 编译为pyc字节码文件，并插入NOP花指令
- 保持代码功能完全一致
- 支持函数级别的代码混淆

## 技术原理

### 代码平坦化

代码平坦化是一种常见的代码混淆技术，它将原始代码的控制流结构（如条件分支、循环等）转换为一个扁平化的结构。具体做法是：

1. 为每个代码块分配一个唯一的状态值
2. 引入一个状态变量，用于控制程序流程
3. 使用一个大型switch-case结构（在Python中以if-elif实现）和while循环替代原始控制流
4. 每个代码块执行后修改状态变量以跳转到下一个代码块

这样，原始代码的控制流结构就被彻底打乱，使得逆向工程和代码分析变得更加困难。

### 函数名混淆

函数名混淆通过将函数名替换为随机生成的字符串来增加代码的理解难度：

1. 为代码中的每个函数生成唯一的随机名称
2. 替换所有函数定义和调用中的函数名
3. 保持函数调用关系不变，确保代码功能正常

### 字节码混淆

字节码混淆在编译后的Python字节码级别进行操作：

1. 将源代码编译为Python字节码
2. 在指令序列中插入无操作(NOP)指令
3. 将混淆后的字节码保存为pyc文件
4. 防止简单的反编译和代码恢复

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 命令行方式

```bash
python main.py input.py -o output.py --pyc --nop-ratio 0.2
```

参数说明：
- `input.py`: 输入的Python文件
- `-o output.py`: 输出的混淆后文件
- `--no-flatten`: 禁用代码平坦化
- `--no-name-obfuscation`: 禁用函数名混淆
- `--pyc`: 编译为pyc文件并插入NOP指令
- `--nop-ratio`: NOP指令比例 (默认: 0.2)

### 图形界面方式

本项目现在提供了基于Tkinter的图形用户界面，可以通过以下方式启动：

```bash
# 从项目根目录运行
python -m ui.app
```

图形界面提供了所有混淆选项的配置，并且有详细的操作日志输出。

### 作为库使用

```python
from mods.complete_obfuscator import CompletePythonObfuscator

# 创建混淆器实例
confuser = CompletePythonObfuscator(
    flatten_code=True,     # 启用代码平坦化
    obfuscate_names=True,  # 启用函数名混淆
    compile_to_pyc=True,   # 编译为pyc文件
    nop_ratio=0.2          # NOP指令比例
)

# 混淆代码
source_code = """
def hello_world():
    print("Hello, World!")
"""
obfuscated_code = confuser.obfuscate(source_code)
print(obfuscated_code)
```

## 演示

运行以下命令以查看混淆效果演示：

```bash
python demo.py                      # 展示所有混淆技术
python demo.py --only-flatten       # 仅展示代码平坦化
python demo.py --only-name-obfuscation  # 仅展示函数名混淆
python demo.py --only-pyc           # 仅展示pyc编译和字节码混淆
python demo.py --pyc --nop-ratio 0.3  # 自定义NOP指令比例
```

## 局限性

当前版本的混淆器有以下局限性：

1. 只对函数体内的代码进行平坦化处理
2. 函数名替换不处理类方法和内置函数
3. 对于复杂的控制流结构（如嵌套循环、异常处理等），效果可能不够理想
4. 不处理类定义、装饰器等高级Python特性
5. pyc文件在不同Python版本间可能不兼容

# Python代码混淆器 UI界面

这个模块提供了Python代码混淆器的图形用户界面，基于Tkinter实现。

## 功能特点

- 支持将Python源代码进行多种混淆处理
- 提供代码平坦化选项
- 支持函数名混淆
- 支持编译为pyc文件并插入NOP指令
- 可配置NOP指令的比例
- 提供直观的用户界面和详细的操作日志

## 使用方法

### 直接运行UI

```bash
# 从ui目录运行
python app.py

# 或从项目根目录运行
python -m ui.app
```

### 作为模块导入

```python
from ui.obfuscator_ui import ObfuscatorUI

# 创建并启动UI
app = ObfuscatorUI()
app.mainloop()
```

## 界面说明

界面主要包含以下几个部分：

1. **文件选择区域**：选择输入的Python源文件和指定输出文件路径
2. **混淆选项区域**：配置混淆选项，包括代码平坦化、函数名混淆和pyc编译
3. **操作按钮**：包含开始混淆和清除表单的按钮
4. **日志输出区域**：显示混淆过程的详细日志
5. **状态栏**：显示当前操作状态

## 依赖项

- Python 3.6+
- Tkinter (Python标准库)
- 项目内部的mods模块

## 注意事项

- 如果选择编译为pyc文件，输出文件的扩展名将自动调整为.pyc
- NOP指令比例范围为0-0.5，表示插入的NOP指令占原指令数量的比例 