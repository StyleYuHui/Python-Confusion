import ast
import random
import string
import keyword


class FunctionNameObfuscator(ast.NodeTransformer):
    """用于替换函数名的AST转换器类"""
    
    def __init__(self, prefix='func_', length=8):
        self.prefix = prefix
        self.length = length
        self.name_mapping = {}  # 存储原始函数名到混淆后函数名的映射
        self.used_names = set(keyword.kwlist)  # 避免使用Python关键字
        
    def _generate_random_name(self):
        """生成一个随机的函数名"""
        while True:
            # 生成随机字符串作为函数名
            random_str = ''.join(random.choice(string.ascii_lowercase) for _ in range(self.length))
            new_name = f"{self.prefix}{random_str}"
            
            # 确保生成的名称不是Python关键字且之前未使用过
            if new_name not in self.used_names:
                self.used_names.add(new_name)
                return new_name
    
    def visit_FunctionDef(self, node):
        """访问函数定义节点，替换函数名"""
        # 记录原始名称
        original_name = node.name
        
        # 如果已经有映射，则使用已有的映射
        if original_name in self.name_mapping:
            new_name = self.name_mapping[original_name]
        else:
            # 否则生成新的随机名称
            new_name = self._generate_random_name()
            self.name_mapping[original_name] = new_name
        
        # 更新节点的函数名
        node.name = new_name
        
        # 继续递归处理函数体
        self.generic_visit(node)
        return node
    
    def visit_Name(self, node):
        """访问名称节点，替换对函数的引用"""
        if isinstance(node.ctx, ast.Load) and node.id in self.name_mapping:
            # 如果是加载上下文且名称在映射表中，则替换名称
            node.id = self.name_mapping[node.id]
        return node
    
    def visit_Call(self, node):
        """访问函数调用节点，替换被调用的函数名"""
        # 处理函数调用的参数
        self.generic_visit(node)
        
        # 检查函数名是否为直接的名称引用
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