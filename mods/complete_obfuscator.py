import os
import ast
import astor
from .confuser import PythonConfuser, obfuscate_file as flatten_file
from .name_obfuscator import obfuscate_function_names
from .bytecode_obfuscator import obfuscate_to_pyc, BytecodeObfuscator


class CompletePythonObfuscator:
    """
    完整的Python代码混淆器 - 集成多种混淆技术
    1. 代码平坦化
    2. 函数名混淆
    3. 字节码混淆(NOP指令)和pyc编译
    """
    
    def __init__(self, flatten_code=True, obfuscate_names=True, 
                compile_to_pyc=False, nop_ratio=0.2):
        """
        初始化混淆器
        
        Args:
            flatten_code: 是否启用代码平坦化
            obfuscate_names: 是否启用函数名混淆
            compile_to_pyc: 是否编译为pyc文件
            nop_ratio: NOP指令占比
        """
        self.flatten_code = flatten_code
        self.obfuscate_names = obfuscate_names
        self.compile_to_pyc = compile_to_pyc
        self.nop_ratio = nop_ratio
        
        self.original_confuser = PythonConfuser() if flatten_code else None
        self.bytecode_obfuscator = BytecodeObfuscator(nop_ratio=nop_ratio) if compile_to_pyc else None
        
        self.name_mapping = {}  # 保存函数名映射关系
    
    def obfuscate(self, source_code, filename="<string>"):
        """
        混淆Python源代码
        
        Args:
            source_code: Python源代码
            filename: 源代码的文件名（用于错误报告）
            
        Returns:
            混淆后的代码或代码对象（如果编译为pyc）
        """
        try:
            # 解析源代码为AST
            tree = ast.parse(source_code)
            
            # 步骤1: 函数名混淆
            if self.obfuscate_names:
                tree, self.name_mapping = obfuscate_function_names(tree)
                # 修复行号等信息
                ast.fix_missing_locations(tree)
            
            # 步骤2: 代码平坦化
            if self.flatten_code:
                tree = self.original_confuser.flattener.visit(tree)
                # 修复行号等信息
                ast.fix_missing_locations(tree)
            
            # 生成混淆后的源代码
            obfuscated_code = astor.to_source(tree)
            
            # 如果有函数名映射，添加注释
            if self.obfuscate_names and self.name_mapping:
                mapping_comment = "# 函数名映射表:\n"
                for original, obfuscated in self.name_mapping.items():
                    mapping_comment += f"# {original} -> {obfuscated}\n"
                obfuscated_code = mapping_comment + "\n" + obfuscated_code
            
            # 步骤3: 如果需要编译为pyc，进行字节码混淆
            if self.compile_to_pyc:
                # 返回混淆后的代码，供后续编译使用
                return obfuscated_code
            
            return obfuscated_code
            
        except Exception as e:
            return f"混淆失败: {str(e)}"
    
    def get_name_mapping(self):
        """获取函数名映射表"""
        return self.name_mapping


def obfuscate_file(input_file, output_file=None, flatten_code=True, 
                  obfuscate_names=True, compile_to_pyc=False, nop_ratio=0.2):
    """
    混淆指定的Python文件
    
    Args:
        input_file: 输入的Python文件
        output_file: 输出文件路径（如果为None，则输出到屏幕）
        flatten_code: 是否启用代码平坦化
        obfuscate_names: 是否启用函数名混淆
        compile_to_pyc: 是否编译为pyc文件
        nop_ratio: NOP指令比例
        
    Returns:
        混淆结果消息
    """
    try:
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # 创建混淆器
        confuser = CompletePythonObfuscator(
            flatten_code=flatten_code,
            obfuscate_names=obfuscate_names,
            compile_to_pyc=compile_to_pyc,
            nop_ratio=nop_ratio
        )
        
        # 首先对源码进行混淆（代码平坦化和函数名混淆）
        obfuscated_code = confuser.obfuscate(source_code, input_file)
        
        # 特殊处理pyc编译
        if compile_to_pyc:
            # 如果没有指定输出文件，则使用默认名称
            if output_file is None:
                output_file = input_file + 'c'
            
            # 使用字节码混淆器直接编译为pyc（使用已混淆的代码）
            success = obfuscate_to_pyc(
                input_file=input_file,
                output_file=output_file,
                nop_ratio=nop_ratio,
                source_code=obfuscated_code  # 传递已混淆的代码而不是重新读取文件
            )
            
            if success:
                return f"混淆后的代码已编译为pyc文件: {output_file}"
            else:
                return "pyc文件编译失败"
        else:
            # 写入输出文件或返回
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(obfuscated_code)
                return f"混淆后的代码已保存到 {output_file}"
            else:
                return obfuscated_code
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"混淆失败: {str(e)}" 