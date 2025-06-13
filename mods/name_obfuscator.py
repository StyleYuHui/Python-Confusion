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


class VariableNameObfuscator(ast.NodeTransformer):
    """用于替换变量名的AST转换器类"""
    
    def __init__(self, prefix='var_', length=8):
        self.prefix = prefix
        self.length = length
        self.name_mapping = {}
        self.used_names = set(keyword.kwlist)  # 避免使用Python关键字
        self.builtin_names = set(__builtins__)  # 避免使用内置函数名
        self.function_names = set()  # 存储函数名，避免混淆
        self.current_function_args = set()  # 当前函数的参数名集合
        self.module_level_names = set()  # 模块级别的变量名集合
        
    def _generate_random_name(self):
        """生成一个随机的变量名"""
        while True:
            random_str = ''.join(random.choice(string.ascii_lowercase) for _ in range(self.length))
            new_name = f"{self.prefix}{random_str}"

            if new_name not in self.used_names and new_name not in self.builtin_names and new_name not in self.function_names:
                self.used_names.add(new_name)
                return new_name
    
    def visit_Import(self, node):
        """处理import语句"""
        for name in node.names:
            self.module_level_names.add(name.name)
            if name.asname:
                self.module_level_names.add(name.asname)
        return node
    
    def visit_ImportFrom(self, node):
        """处理from ... import语句"""
        for name in node.names:
            self.module_level_names.add(name.name)
            if name.asname:
                self.module_level_names.add(name.asname)
        return node
    
    def visit_Assign(self, node):
        """处理赋值语句，记录模块级别的变量名"""
        if not self.current_function_args:  # 在模块级别
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.module_level_names.add(target.id)
        self.generic_visit(node)
        return node
    
    def visit_FunctionDef(self, node):
        """处理函数定义，记录函数名和参数名"""
        self.function_names.add(node.name)
        
        # 保存当前函数的参数名
        old_args = self.current_function_args
        self.current_function_args = {arg.arg for arg in node.args.args}
        
        # 处理函数体
        self.generic_visit(node)
        
        # 恢复之前的参数名集合
        self.current_function_args = old_args
        return node
    
    def visit_Name(self, node):
        """访问名称节点，只替换变量名"""
        # 只处理变量赋值和使用的场景
        if isinstance(node.ctx, (ast.Store, ast.Load)):
            # 跳过内置函数、关键字、函数名、函数参数和模块级别的变量
            if (node.id in keyword.kwlist or 
                node.id in self.builtin_names or 
                node.id in self.function_names or
                node.id in self.current_function_args or
                node.id in self.module_level_names):
                return node
                
            if node.id in self.name_mapping:
                node.id = self.name_mapping[node.id]
            else:
                new_name = self._generate_random_name()
                self.name_mapping[node.id] = new_name
                node.id = new_name
        return node


def obfuscate_function_names(tree):
    """对AST进行函数名混淆处理"""
    obfuscator = FunctionNameObfuscator()
    transformed_tree = obfuscator.visit(tree)
    ast.fix_missing_locations(transformed_tree)
    return transformed_tree, obfuscator.name_mapping


def obfuscate_variable_names(tree):
    """对AST进行变量名混淆处理"""
    obfuscator = VariableNameObfuscator()
    transformed_tree = obfuscator.visit(tree)
    ast.fix_missing_locations(transformed_tree)
    return transformed_tree, obfuscator.name_mapping 