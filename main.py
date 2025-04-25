#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
from mods.complete_obfuscator import obfuscate_file


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(description='Python代码混淆器 - 支持多种混淆技术')
    
    parser.add_argument('input_file', help='输入的Python文件路径')
    parser.add_argument('-o', '--output', help='输出的混淆后文件路径 (默认为stdout)')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    
    # 混淆选项
    obfuscation_group = parser.add_argument_group('混淆选项')
    obfuscation_group.add_argument('--no-flatten', action='store_true', help='禁用代码平坦化')
    obfuscation_group.add_argument('--no-name-obfuscation', action='store_true', help='禁用函数名混淆')
    obfuscation_group.add_argument('--pyc', action='store_true', help='编译为pyc文件并插入NOP指令')
    obfuscation_group.add_argument('--nop-ratio', type=float, default=0.2, help='NOP指令比例 (默认: 0.2)')
    
    args = parser.parse_args()
    
    try:
        if args.verbose:
            print(f"正在混淆文件: {args.input_file}")
            if not args.no_flatten:
                print("- 启用代码平坦化")
            if not args.no_name_obfuscation:
                print("- 启用函数名混淆")
            if args.pyc:
                print(f"- 启用pyc编译并插入NOP花指令 (比例: {args.nop_ratio})")
        
        # 如果输出到pyc文件但未指定输出文件名，则自动添加.pyc后缀
        output_file = args.output
        if args.pyc and output_file and not output_file.endswith('.pyc'):
            output_file += '.pyc'
            if args.verbose:
                print(f"输出文件已自动调整为: {output_file}")
            
        result = obfuscate_file(
            args.input_file, 
            output_file,
            flatten_code=not args.no_flatten,
            obfuscate_names=not args.no_name_obfuscation,
            compile_to_pyc=args.pyc,
            nop_ratio=args.nop_ratio
        )
        
        if args.verbose:
            print(result)
        elif not args.output:
            print(result)
            
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())