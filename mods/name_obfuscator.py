import ast
import random
import string
import keyword


class FunctionNameObfuscator(ast.NodeTransformer):
    """用于替换函数名的AST转换器类"""
    
    def __init__(self, prefix='func_', length=8):
        self.prefix = prefix
        self.length = length
        self.name_mapping = {}
        self.used_names = set(keyword.kwlist)  # 避免使用Python关键字
        
    def _generate_random_name(self):
        """生成一个随机的函数名"""
        while True:
            random_str = ''.join(random.choice(string.ascii_lowercase) for _ in range(self.length))
            new_name = f"{self.prefix}{random_str}"

            if new_name not in self.used_names:
                self.used_names.add(new_name)
                return new_name
    
    def visit_FunctionDef(self, node):
        """访问函数定义节点，替换函数名"""
        original_name = node.name

        if original_name in self.name_mapping:
            new_name = self.name_mapping[original_name]
        else:
            new_name = self._generate_random_name()
            self.name_mapping[original_name] = new_name

        node.name = new_name

        self.generic_visit(node)
        return node
    
    def visit_Name(self, node):
        """访问名称节点，替换对函数的引用"""
        if isinstance(node.ctx, ast.Load) and node.id in self.name_mapping:
            node.id = self.name_mapping[node.id]
        return node
    
    def visit_Call(self, node):
        """访问函数调用节点，替换被调用的函数名"""
        self.generic_visit(node)

        if isinstance(node.func, ast.Name) and node.func.id in self.name_mapping:
            node.func.id = self.name_mapping[node.func.id]
        
        return node


def obfuscate_function_names(tree):
    """对AST进行函数名混淆处理"""
    # 创建函数名混淆器
    obfuscator = FunctionNameObfuscator()
    
    # 对AST进行转换
    transformed_tree = obfuscator.visit(tree)
    
    # 修复行号等信息
    ast.fix_missing_locations(transformed_tree)
    
    return transformed_tree, obfuscator.name_mapping 