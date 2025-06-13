import py_compile
import os
import random
import sys
import importlib
import importlib.util
import marshal
import struct
import time
import types
import traceback


class BytecodeObfuscator:
    """字节码级混淆器 - 编译为pyc并插入nop花指令"""
    
    def __init__(self, nop_ratio=0.2, max_consecutive_nops=5):
        """
        初始化字节码混淆器
        
        Args:
            nop_ratio: 插入的nop指令占原指令数量的比例
            max_consecutive_nops: 最大连续nop指令数量
        """
        self.nop_ratio = nop_ratio
        self.max_consecutive_nops = max_consecutive_nops
        self.nop_opcode = 9  # Python中NOP指令的操作码
    
    def _insert_nops(self, code_obj):
        """
        在代码对象中插入NOP指令
        
        Args:
            code_obj: 代码对象
            
        Returns:
            带有NOP指令的新代码对象
        """
        try:
            # 获取代码对象的属性
            co_argcount = code_obj.co_argcount
            co_posonlyargcount = code_obj.co_posonlyargcount if hasattr(code_obj, 'co_posonlyargcount') else 0
            co_kwonlyargcount = code_obj.co_kwonlyargcount
            co_nlocals = code_obj.co_nlocals
            co_stacksize = code_obj.co_stacksize
            co_flags = code_obj.co_flags
            co_code = bytearray(code_obj.co_code)
            co_consts = list(code_obj.co_consts)
            co_names = code_obj.co_names
            co_varnames = code_obj.co_varnames
            co_filename = code_obj.co_filename
            co_name = code_obj.co_name
            co_firstlineno = code_obj.co_firstlineno
            co_lnotab = code_obj.co_lnotab
            co_freevars = code_obj.co_freevars
            co_cellvars = code_obj.co_cellvars
            
            # 处理常量中的代码对象（递归处理）
            for i, const in enumerate(co_consts):
                if isinstance(const, types.CodeType):
                    co_consts[i] = self._insert_nops(const)
            
            # 计算要插入的NOP指令数量
            num_instructions = len(co_code) // 2
            num_nops = int(num_instructions * self.nop_ratio)
            
            # 逐字节检查并插入NOP指令
            i = 0
            nops_inserted = 0
            new_code = bytearray()
            
            while i < len(co_code):
                # 随机决定是否在此处插入NOP
                if nops_inserted < num_nops and random.random() < 0.3:
                    # 决定要插入的连续NOP数量
                    nop_count = random.randint(1, self.max_consecutive_nops)
                    nop_count = min(nop_count, num_nops - nops_inserted)
                    
                    # 插入NOP指令和参数0
                    for _ in range(nop_count):
                        new_code.append(self.nop_opcode)
                        new_code.append(0)  # NOP的参数为0
                    
                    nops_inserted += nop_count
                
                # 复制原始字节码
                opcode = co_code[i]
                new_code.append(opcode)
                
                # 如果是有参数的指令，复制参数
                if i + 1 < len(co_code):
                    arg = co_code[i + 1]
                    new_code.append(arg)
                    i += 2
                else:
                    # 安全检查，通常不应该到达这里
                    i += 1
            
            # 创建新的代码对象
            new_code_obj_args = [
                co_argcount,
                co_posonlyargcount,
                co_kwonlyargcount,
                co_nlocals,
                co_stacksize + self.max_consecutive_nops,  # 增加堆栈大小以适应额外的NOP
                co_flags,
                bytes(new_code),
                tuple(co_consts),
                co_names,
                co_varnames,
                co_filename,
                co_name,
                co_firstlineno,
                co_lnotab,
                co_freevars,
                co_cellvars
            ]
            
            # 调试输出各个参数的类型
            print(f"co_firstlineno类型: {type(co_firstlineno).__name__}，值: {co_firstlineno}")
            print(f"co_lnotab类型: {type(co_lnotab).__name__}，值: {co_lnotab[:10] if isinstance(co_lnotab, (bytes, bytearray)) else co_lnotab}")
            
            # 确保co_lnotab是bytes类型
            if not isinstance(co_lnotab, bytes):
                co_lnotab = bytes(co_lnotab) if isinstance(co_lnotab, (list, bytearray)) else bytes()
            
            # 更新数组中的值
            new_code_obj_args[13] = co_lnotab
            
            try:
                return types.CodeType(*new_code_obj_args)
            except TypeError as e:
                print(f"创建CodeType对象错误: {e}")
                if "argument 13 must be str, not int" in str(e):
                    new_code_obj_args[12] = str(co_firstlineno)
                elif "argument 13 must be int, not str" in str(e):
                    new_code_obj_args[12] = int(co_firstlineno) if isinstance(co_firstlineno, str) else co_firstlineno
                
                try:
                    return types.CodeType(*new_code_obj_args)
                except TypeError as e2:
                    print(f"第二次尝试创建CodeType对象错误: {e2}")
                    return code_obj
        except Exception as e:
            print(f"NOP插入失败: {str(e)}")
            traceback.print_exc()
            return code_obj
    
    def obfuscate_bytecode(self, source_code, filename="<string>"):
        """
        混淆Python源代码的字节码
        
        Args:
            source_code: Python源代码
            filename: 源代码的文件名（用于错误报告）
            
        Returns:
            混淆后的代码对象
        """

        code_obj = compile(source_code, filename, 'exec')
        

        obfuscated_code = self._insert_nops(code_obj)
        
        return obfuscated_code
    
    def compile_to_pyc(self, source_code, output_file, source_file="<string>"):
        """
        将源代码编译为pyc文件并插入NOP花指令
        
        Args:
            source_code: Python源代码
            output_file: 输出的pyc文件路径
            source_file: 源文件名（用于错误报告）
            
        Returns:
            是否成功编译
        """
        try:
            # 获取混淆后的代码对象
            code_obj = self.obfuscate_bytecode(source_code, source_file)
            
            # 获取Python魔术数
            # 在较新版本的Python中使用MAGIC_NUMBER，在较旧版本中使用MAGIC
            if hasattr(importlib.util, 'MAGIC_NUMBER'):
                magic = importlib.util.MAGIC_NUMBER
            else:
                magic = importlib.util.MAGIC
            

            timestamp = int(time.time())
            

            os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
            
            # 写入pyc文件
            with open(output_file, 'wb') as f:
                f.write(magic)
                if sys.version_info >= (3, 7):
                    f.write(struct.pack('<I', 0))
                f.write(struct.pack('<I', timestamp))
                if sys.version_info >= (3, 8):
                    source_size = len(source_code.encode())
                    f.write(struct.pack('<I', source_size))
                marshal.dump(code_obj, f)
            
            print(f"编译成功: {output_file}")
            return True
        except Exception as e:
            print(f"编译失败: {str(e)}")
            traceback.print_exc()
            return False


def simple_compile_to_pyc(input_file, output_file=None):
    """
    简单地将Python文件编译为pyc文件
    
    Args:
        input_file: 输入的Python文件
        output_file: 输出的pyc文件，默认为input_file+c
        
    Returns:
        是否成功编译
    """
    try:
        if output_file is None:
            output_file = input_file + 'c'
        

        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        

        py_compile.compile(input_file, output_file)
        print(f"编译成功: {output_file}")
        return True
    except Exception as e:
        print(f"编译失败: {str(e)}")
        traceback.print_exc()
        return False


def obfuscate_to_pyc(input_file, output_file=None, nop_ratio=0.2, use_original_compile=False, source_code=None):
    """
    将Python文件混淆并编译为pyc文件
    
    Args:
        input_file: 输入的Python文件
        output_file: 输出的pyc文件，默认为input_file+c
        nop_ratio: NOP指令的比例
        use_original_compile: 是否使用原始编译方式，不插入NOP
        source_code: 已经混淆的源代码，如果提供则直接使用，否则从input_file读取
        
    Returns:
        是否成功混淆和编译
    """
    try:
        if source_code is None:
            with open(input_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
        
        if output_file is None:
            output_file = input_file + 'c'

        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        
        print(f"输入文件: {input_file}")
        print(f"输出文件: {output_file}")
        print(f"NOP比例: {nop_ratio}")
        print(f"使用原始编译: {use_original_compile}")
        print(f"使用提供的源代码: {source_code is not None}")
        
        if use_original_compile:
            # 如果提供了源代码但使用原始编译方式，先写入临时文件
            if source_code is not None:
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
                    temp_file = temp.name
                    temp.write(source_code.encode('utf-8'))
                
                try:
                    result = simple_compile_to_pyc(temp_file, output_file)
                finally:
                    os.unlink(temp_file)
                return result
            else:
                return simple_compile_to_pyc(input_file, output_file)
        else:
            obfuscator = BytecodeObfuscator(nop_ratio=nop_ratio)
            return obfuscator.compile_to_pyc(source_code, output_file, input_file)
        
    except Exception as e:
        print(f"混淆失败: {str(e)}")
        traceback.print_exc()
        return False 