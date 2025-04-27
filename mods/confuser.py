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
        original_body = node.body

        self.state_var = '_' + ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        self.next_state = 0
        self.states = {}

        state_mapping = {}
        for i, stmt in enumerate(original_body):
            state = self.get_next_state()
            state_mapping[i] = state

        end_state = -1

        flattened_body = []

        state_assign = ast.Assign(
            targets=[ast.Name(id=self.state_var, ctx=ast.Store())],
            value=ast.Constant(value=0)
        )
        flattened_body.append(state_assign)

        while_test = ast.Compare(
            left=ast.Name(id=self.state_var, ctx=ast.Load()),
            ops=[ast.NotEq()],
            comparators=[ast.Constant(value=end_state)]
        )

        switch_body = []

        for i, stmt in enumerate(original_body):
            state = state_mapping[i]
            next_state = state_mapping.get(i + 1, end_state)

            condition = ast.Compare(
                left=ast.Name(id=self.state_var, ctx=ast.Load()),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value=state)]
            )

            # 创建分支体
            if isinstance(stmt, ast.Return):
                branch_body = [
                    stmt,
                    ast.Assign(
                        targets=[ast.Name(id=self.state_var, ctx=ast.Store())],
                        value=ast.Constant(value=end_state)
                    )
                ]
            else:
                branch_body = [
                    stmt,
                    ast.Assign(
                        targets=[ast.Name(id=self.state_var, ctx=ast.Store())],
                        value=ast.Constant(value=next_state)
                    )
                ]

            if_stmt = ast.If(
                test=condition,
                body=branch_body,
                orelse=[]
            )

            switch_body.append(if_stmt)

        while_loop = ast.While(
            test=while_test,
            body=switch_body,
            orelse=[]
        )

        flattened_body.append(while_loop)

        node.body = flattened_body

        return node

    def visit_Module(self, node):
        """访问模块节点，处理全局层次的代码"""
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
            tree = ast.parse(source_code)

            flattened_tree = self.flattener.visit(tree)

            ast.fix_missing_locations(flattened_tree)

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