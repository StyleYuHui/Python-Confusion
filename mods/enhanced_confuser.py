import ast
import astor
from .planarization_confuser import PythonConfuser, obfuscate_file as flatten_file
from .name_obfuscator import obfuscate_function_names


class EnhancedPythonConfuser:
    """增强版Python代码混淆器 - 集成代码平坦化和函数名替换功能"""
    
    def __init__(self, flatten_code=True, obfuscate_names=True):
        self.flatten_code = flatten_code  # 是否启用代码平坦化
        self.obfuscate_names = obfuscate_names  # 是否启用函数名混淆
        self.original_confuser = PythonConfuser() if flatten_code else None
        self.name_mapping = {}  # 保存函数名映射关系
    
    def obfuscate(self, source_code):
        """混淆输入的源代码"""
        try:
            # 解析源代码为AST
            tree = ast.parse(source_code)
            
            # 如果启用了函数名混淆，先进行函数名混淆
            if self.obfuscate_names:
                tree, self.name_mapping = obfuscate_function_names(tree)
                # 修复行号等信息
                ast.fix_missing_locations(tree)
            
            if self.flatten_code:
                # 使用原始混淆器的代码平坦化功能
                tree = self.original_confuser.flattener.visit(tree)
                # 修复行号等信息
                ast.fix_missing_locations(tree)
            
            # 将AST转换回Python代码
            obfuscated_code = astor.to_source(tree)
            
            # 如果有函数名映射，添加注释
            if self.obfuscate_names and self.name_mapping:
                mapping_comment = "# 函数名映射表:\n"
                for original, obfuscated in self.name_mapping.items():
                    mapping_comment += f"# {original} -> {obfuscated}\n"
                obfuscated_code = mapping_comment + "\n" + obfuscated_code
            
            return obfuscated_code
        except Exception as e:
            return f"混淆失败: {str(e)}"
    
    def get_name_mapping(self):
        """获取函数名映射表"""
        return self.name_mapping


def obfuscate_file(input_file, output_file=None, flatten_code=True, obfuscate_names=True):
    """混淆指定的Python文件，支持代码平坦化和函数名混淆"""
    with open(input_file, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    confuser = EnhancedPythonConfuser(
        flatten_code=flatten_code,
        obfuscate_names=obfuscate_names
    )
    obfuscated_code = confuser.obfuscate(source_code)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(obfuscated_code)
        return f"混淆后的代码已保存到 {output_file}"
    else:
        return obfuscated_code 