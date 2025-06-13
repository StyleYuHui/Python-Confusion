import os
import ast
import astor
from .confuser import PythonConfuser, obfuscate_file as flatten_file
from .name_obfuscator import obfuscate_function_names, obfuscate_variable_names
from .bytecode_obfuscator import obfuscate_to_pyc, BytecodeObfuscator


class CompletePythonObfuscator:
    """
    完整的Python代码混淆器 - 集成多种混淆技术
    1. 代码平坦化
    2. 函数名混淆
    3. 变量名混淆
    4. 字节码混淆(NOP指令)和pyc编译
    """
    
    def __init__(self, flatten_code=True, obfuscate_names=True, obfuscate_vars=True,
                compile_to_pyc=False, nop_ratio=0.2):
        """
        初始化混淆器
        
        Args:
            flatten_code: 是否启用代码平坦化
            obfuscate_names: 是否启用函数名混淆
            obfuscate_vars: 是否启用变量名混淆
            compile_to_pyc: 是否编译为pyc文件
            nop_ratio: NOP指令占比
        """
        self.flatten_code = flatten_code
        self.obfuscate_names = obfuscate_names
        self.obfuscate_vars = obfuscate_vars
        self.compile_to_pyc = compile_to_pyc
        self.nop_ratio = nop_ratio
        
        self.original_confuser = PythonConfuser() if flatten_code else None
        self.bytecode_obfuscator = BytecodeObfuscator(nop_ratio=nop_ratio) if compile_to_pyc else None
        
        self.name_mapping = {}  # 保存函数名映射关系
        self.var_mapping = {}   # 保存变量名映射关系
    
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
                ast.fix_missing_locations(tree)
            
            # 步骤2: 变量名混淆
            if self.obfuscate_vars:
                tree, self.var_mapping = obfuscate_variable_names(tree)
                ast.fix_missing_locations(tree)
            
            # 步骤3: 代码平坦化
            if self.flatten_code:
                tree = self.original_confuser.flattener.visit(tree)
                ast.fix_missing_locations(tree)
            
            # 生成混淆后的源代码
            obfuscated_code = astor.to_source(tree)
            
            # 添加映射表注释
            mapping_comment = ""
            if self.obfuscate_names and self.name_mapping:
                mapping_comment += "# 函数名映射表:\n"
                for original, obfuscated in self.name_mapping.items():
                    mapping_comment += f"# {original} -> {obfuscated}\n"
                mapping_comment += "\n"
            
            if self.obfuscate_vars and self.var_mapping:
                mapping_comment += "# 变量名映射表:\n"
                for original, obfuscated in self.var_mapping.items():
                    mapping_comment += f"# {original} -> {obfuscated}\n"
                mapping_comment += "\n"
            
            if mapping_comment:
                obfuscated_code = mapping_comment + obfuscated_code
            
            # 步骤4: 如果需要编译为pyc，进行字节码混淆
            if self.compile_to_pyc:
                return obfuscated_code
            
            return obfuscated_code
            
        except Exception as e:
            return f"混淆失败: {str(e)}"
    
    def get_name_mapping(self):
        """获取函数名映射表"""
        return self.name_mapping
    
    def get_var_mapping(self):
        """获取变量名映射表"""
        return self.var_mapping


def obfuscate_file(input_file, output_file=None, flatten_code=True, 
                  obfuscate_names=True, obfuscate_vars=True,
                  compile_to_pyc=False, nop_ratio=0.2):
    """
    混淆指定的Python文件
    
    Args:
        input_file: 输入的Python文件
        output_file: 输出文件路径（如果为None，则输出到屏幕）
        flatten_code: 是否启用代码平坦化
        obfuscate_names: 是否启用函数名混淆
        obfuscate_vars: 是否启用变量名混淆
        compile_to_pyc: 是否编译为pyc文件
        nop_ratio: NOP指令比例
        
    Returns:
        混淆结果消息
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()

        confuser = CompletePythonObfuscator(
            flatten_code=flatten_code,
            obfuscate_names=obfuscate_names,
            obfuscate_vars=obfuscate_vars,
            compile_to_pyc=compile_to_pyc,
            nop_ratio=nop_ratio
        )

        obfuscated_code = confuser.obfuscate(source_code, input_file)

        if compile_to_pyc:
            if output_file is None:
                output_file = input_file + 'c'

            success = obfuscate_to_pyc(
                input_file=input_file,
                output_file=output_file,
                nop_ratio=nop_ratio,
                source_code=obfuscated_code
            )
            
            if success:
                return f"混淆后的代码已编译为pyc文件: {output_file}"
            else:
                return "pyc文件编译失败"
        else:
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