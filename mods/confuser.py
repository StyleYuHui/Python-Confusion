import ast
import astor
import random
import string


class CodeFlattener(ast.NodeVisitor):
    """用于执行代码平坦化的AST访问器类"""
    
    def __init__(self):
        self.state_var = '_' + ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        self.next_state = 0
        self.states = {}
        
    def get_next_state(self):
        """获取下一个状态值"""
        state = self.next_state
        self.next_state += 1
        return state
    
    def visit_FunctionDef(self, node):
        """访问函数定义节点，对函数体进行平坦化"""
        # 保存原始函数体
        original_body = node.body
        
        # 重置状态
        self.state_var = '_' + ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        self.next_state = 0
        self.states = {}
        
        # 为每个语句分配状态
        state_mapping = {}
        for i, stmt in enumerate(original_body):
            state = self.get_next_state()
            state_mapping[i] = state
        
        # 特殊的结束状态
        end_state = -1
        
        # 创建平坦化的函数体
        flattened_body = []
        
        # 1. 状态变量初始化
        state_assign = ast.Assign(
            targets=[ast.Name(id=self.state_var, ctx=ast.Store())],
            value=ast.Constant(value=0)  # 从状态0开始
        )
        flattened_body.append(state_assign)
        
        # 2. 主循环
        while_test = ast.Compare(
            left=ast.Name(id=self.state_var, ctx=ast.Load()),
            ops=[ast.NotEq()],
            comparators=[ast.Constant(value=end_state)]
        )
        
        # 3. 构建switch-case结构(if-elif结构)
        switch_body = []
        
        for i, stmt in enumerate(original_body):
            state = state_mapping[i]
            next_state = state_mapping.get(i + 1, end_state)
            
            # 创建条件判断
            condition = ast.Compare(
                left=ast.Name(id=self.state_var, ctx=ast.Load()),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value=state)]
            )
            
            # 创建分支体
            if isinstance(stmt, ast.Return):
                # 对于return语句，先执行，然后设置为结束状态
                branch_body = [
                    stmt,  # 原始的return语句
                    ast.Assign(
                        targets=[ast.Name(id=self.state_var, ctx=ast.Store())],
                        value=ast.Constant(value=end_state)
                    )
                ]
            else:
                # 对于其他语句，执行后跳转到下一个状态
                branch_body = [
                    stmt,  # 原始语句
                    ast.Assign(
                        targets=[ast.Name(id=self.state_var, ctx=ast.Store())],
                        value=ast.Constant(value=next_state)
                    )
                ]
            
            # 创建if语句
            if_stmt = ast.If(
                test=condition,
                body=branch_body,
                orelse=[]
            )
            
            switch_body.append(if_stmt)
        
        # 创建while循环
        while_loop = ast.While(
            test=while_test,
            body=switch_body,
            orelse=[]
        )
        
        flattened_body.append(while_loop)
        
        # 替换原始函数体
        node.body = flattened_body
        
        return node
    
    def visit_Module(self, node):
        """访问模块节点，处理全局层次的代码"""
        # 只对函数体进行平坦化处理
        new_body = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                new_body.append(self.visit_FunctionDef(item))
            else:
                new_body.append(item)
        
        node.body = new_body
        return node


class PythonConfuser:
    """Python代码混淆器主类"""
    
    def __init__(self):
        self.flattener = CodeFlattener()
    
    def obfuscate(self, source_code):
        """混淆输入的源代码"""
        try:
            # 解析源代码为AST
            tree = ast.parse(source_code)
            
            # 应用代码平坦化
            flattened_tree = self.flattener.visit(tree)
            
            # 修复行号等信息
            ast.fix_missing_locations(flattened_tree)
            
            # 将AST转换回Python代码
            obfuscated_code = astor.to_source(flattened_tree)
            
            return obfuscated_code
        except Exception as e:
            return f"混淆失败: {str(e)}"


def obfuscate_file(input_file, output_file=None):
    """混淆指定的Python文件"""
    with open(input_file, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    confuser = PythonConfuser()
    obfuscated_code = confuser.obfuscate(source_code)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(obfuscated_code)
        return f"混淆后的代码已保存到 {output_file}"
    else:
        return obfuscated_code 