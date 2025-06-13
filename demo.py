#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
演示脚本：展示Python代码混淆器的效果
"""

import os
import time
import sys
from mods.complete_obfuscator import CompletePythonObfuscator, obfuscate_to_pyc

# 确保examples目录存在
if not os.path.exists('examples'):
    os.makedirs('examples')

# 测试代码示例
SAMPLE_CODE = """
def calculate_sum(n):
    # 计算1到n的和
    total = 0
    for i in range(1, n + 1):
        if i % 2 == 0:
            total += i * 2
        else:
            total += i
    return total

def is_prime(n):
    # 判断n是否为质数
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def process_data(data_list):
    # 处理数据列表
    result = []
    temp_sum = 0
    for item in data_list:
        if isinstance(item, (int, float)):
            temp_sum += item
            if temp_sum > 100:
                result.append(temp_sum)
                temp_sum = 0
        elif isinstance(item, str):
            result.append(item.upper())
    return result

# 测试函数
result = calculate_sum(10)
print(f"1到10的加权和: {result}")

for num in range(10, 20):
    if is_prime(num):
        print(f"{num}是质数")
    else:
        print(f"{num}不是质数")

# 测试变量名混淆
test_data = [1, 2, 3, 4, 5, "hello", 6, 7, 8, 9, "world"]
processed = process_data(test_data)
print("处理后的数据:", processed)
"""

def show_comparison(flatten_code=True, obfuscate_names=True, obfuscate_vars=True, compile_to_pyc=False, nop_ratio=0.2):
    """展示混淆前后的代码对比"""
    print("=" * 80)
    print("Python代码混淆器演示")
    if flatten_code:
        print("- 启用代码平坦化")
    if obfuscate_names:
        print("- 启用函数名混淆")
    if obfuscate_vars:
        print("- 启用变量名混淆")
    if compile_to_pyc:
        print(f"- 启用pyc编译并插入NOP花指令 (比例: {nop_ratio})")
    print("=" * 80)
    
    # 原始代码
    print("\n【原始代码】:")
    print("-" * 80)
    print(SAMPLE_CODE)
    
    # 混淆后的代码
    print("\n【开始混淆代码...】")
    start_time = time.time()
    
    # 生成文件后缀
    suffix = ""
    if flatten_code:
        suffix += "_flat"
    if obfuscate_names:
        suffix += "_named"
    if obfuscate_vars:
        suffix += "_var"
    if compile_to_pyc:
        suffix += "_pyc"
    
    # 保存原始代码
    original_path = 'examples/original.py'
    with open(original_path, 'w', encoding='utf-8') as f:
        f.write(SAMPLE_CODE)
    
    # 混淆代码
    if compile_to_pyc:
        # 编译为pyc文件
        temp_py_path = f'examples/obfuscated{suffix}.py'
        output_path = f'examples/obfuscated{suffix}.pyc'
        
        # 先保存原始代码
        with open(temp_py_path, 'w', encoding='utf-8') as f:
            f.write(SAMPLE_CODE)
        
        # 使用混淆函数编译成pyc
        success = obfuscate_to_pyc(
            temp_py_path, 
            output_path, 
            nop_ratio=nop_ratio,
            use_original_compile=False
        )
        
        if success:
            print(f"成功编译为pyc: {output_path}")
        else:
            print(f"编译失败: {output_path}")
            
        # 使用普通混淆器创建可比较的源代码版本
        confuser = CompletePythonObfuscator(
            flatten_code=flatten_code,
            obfuscate_names=obfuscate_names,
            obfuscate_vars=obfuscate_vars,
            compile_to_pyc=False
        )
        obfuscated_code = confuser.obfuscate(SAMPLE_CODE, temp_py_path)
        with open(temp_py_path, 'w', encoding='utf-8') as f:
            f.write(obfuscated_code)
            
        final_output_path = output_path
    else:
        # 仅混淆源代码
        confuser = CompletePythonObfuscator(
            flatten_code=flatten_code,
            obfuscate_names=obfuscate_names,
            obfuscate_vars=obfuscate_vars,
            compile_to_pyc=False
        )
        obfuscated_code = confuser.obfuscate(SAMPLE_CODE)
        
        output_path = f'examples/obfuscated{suffix}.py'
        # 保存混淆后的代码
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(obfuscated_code)
        final_output_path = output_path
    
    end_time = time.time()
    
    print(f"混淆耗时: {end_time - start_time:.3f}秒")
    
    if not compile_to_pyc:
        print("\n【混淆后的代码】:")
        print("-" * 80)
        print(obfuscated_code)
    else:
        print("\n【已编译为pyc文件】")
        if os.path.exists(output_path):
            print(f"- 文件大小: {os.path.getsize(output_path)} 字节")
        else:
            print("- 文件未创建成功")
        print("- pyc文件不显示字节码，可以使用Python的dis模块查看")
    
    print("\n【文件已保存】:")
    print(f"原始代码: {original_path} ({len(SAMPLE_CODE)} 字节)")
    
    if os.path.exists(final_output_path):
        print(f"混淆后代码: {final_output_path} ({os.path.getsize(final_output_path)} 字节)")
        if not compile_to_pyc:
            print(f"代码膨胀率: {len(obfuscated_code) / len(SAMPLE_CODE):.2f}倍")
    else:
        print(f"混淆后代码: {final_output_path} (文件未创建)")
    
    print("\n【验证功能一致性】:")
    print("运行原始代码:")
    print("-" * 30)
    os.system(f'python {original_path}')
    print("-" * 30)
    
    print("\n运行混淆后代码:")
    print("-" * 30)
    if compile_to_pyc:
        # 运行普通混淆版本，因为pyc可能不兼容
        os.system(f'python {temp_py_path}')
    else:
        os.system(f'python {final_output_path}')
    print("-" * 30)
    
    if obfuscate_names and hasattr(confuser, 'name_mapping') and confuser.name_mapping:
        print("\n【函数名映射】:")
        for original, obfuscated in confuser.name_mapping.items():
            print(f"{original} -> {obfuscated}")
    
    if obfuscate_vars and hasattr(confuser, 'var_mapping') and confuser.var_mapping:
        print("\n【变量名映射】:")
        for original, obfuscated in confuser.var_mapping.items():
            print(f"{original} -> {obfuscated}")
    
    print("\n【混淆后的代码特点】:")
    features = []
    if flatten_code:
        features.append("1. 使用了代码平坦化技术，改变了原始控制流")
        features.append("2. 引入了状态变量和状态机结构")
        counter = 3
    else:
        counter = 1
        
    if obfuscate_names:
        features.append(f"{counter}. 替换了函数名为随机字符串")
        features.append(f"{counter+1}. 保持了函数调用的一致性")
        counter += 2
        
    if obfuscate_vars:
        features.append(f"{counter}. 替换了局部变量名为随机字符串")
        features.append(f"{counter+1}. 保持了变量作用域的一致性")
        counter += 2
        
    if compile_to_pyc:
        features.append(f"{counter}. 编译为字节码文件(pyc)")
        features.append(f"{counter+1}. 在字节码中插入NOP花指令")
        counter += 2
    
    features.append(f"{counter}. 功能与原始代码完全相同")
    
    for feature in features:
        print(feature)
    
    print("\n如何使用此工具:")
    print("1. 命令行方式: python main.py input.py -o output.py [选项]")
    print("2. 在代码中导入: from mods.complete_obfuscator import CompletePythonObfuscator")
    print("=" * 80)


if __name__ == "__main__":
    import sys

    flatten = '--no-flatten' not in sys.argv
    name_obfuscation = '--no-name-obfuscation' not in sys.argv
    var_obfuscation = '--no-var-obfuscation' not in sys.argv
    compile_to_pyc = '--pyc' in sys.argv
    verbose = '--verbose' in sys.argv
    
    # 特定混淆模式
    if '--only-flatten' in sys.argv:
        flatten, name_obfuscation, var_obfuscation, compile_to_pyc = True, False, False, False
    elif '--only-name-obfuscation' in sys.argv:
        flatten, name_obfuscation, var_obfuscation, compile_to_pyc = False, True, False, False
    elif '--only-var-obfuscation' in sys.argv:
        flatten, name_obfuscation, var_obfuscation, compile_to_pyc = False, False, True, False
    elif '--only-pyc' in sys.argv:
        flatten, name_obfuscation, var_obfuscation, compile_to_pyc = False, False, False, True
    
    # NOP比例
    nop_ratio = 0.2
    for i, arg in enumerate(sys.argv):
        if arg == '--nop-ratio' and i + 1 < len(sys.argv):
            try:
                nop_ratio = float(sys.argv[i + 1])
                nop_ratio = max(0.05, min(0.5, nop_ratio))
            except ValueError:
                pass
    
    try:
        # 运行演示
        show_comparison(
            flatten_code=flatten, 
            obfuscate_names=name_obfuscation,
            obfuscate_vars=var_obfuscation,
            compile_to_pyc=compile_to_pyc,
            nop_ratio=nop_ratio
        )
    except Exception as e:
        if verbose:
            import traceback
            traceback.print_exc()
        print(f"错误: {str(e)}") 