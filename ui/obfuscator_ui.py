#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

# 添加项目根目录到路径，以便能够导入mods模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mods.complete_obfuscator import obfuscate_file


class ObfuscatorUI(tk.Tk):
    """Python代码混淆器的GUI界面"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Python代码混淆器V0.01 By PaperPlane")
        self.geometry("750x600")
        self.resizable(True, True)
        
        
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kunkun.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        
        self.create_widgets()
        self.setup_layout()
    
    def create_widgets(self):
        """创建UI组件"""
        # 样式配置
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat")
        self.style.configure("TFrame", padding=5)
        self.style.configure("TLabel", padding=3)
        
        # 文件选择区域
        self.file_frame = ttk.LabelFrame(self, text="文件选择")
        
        self.input_label = ttk.Label(self.file_frame, text="输入文件:")
        self.input_path = ttk.Entry(self.file_frame, width=50)
        self.input_browse = ttk.Button(self.file_frame, text="浏览...", command=self.browse_input)
        
        self.output_label = ttk.Label(self.file_frame, text="输出文件:")
        self.output_path = ttk.Entry(self.file_frame, width=50)
        self.output_browse = ttk.Button(self.file_frame, text="浏览...", command=self.browse_output)
        
        # 混淆选项区域
        self.options_frame = ttk.LabelFrame(self, text="混淆选项")
        
        self.flatten_var = tk.BooleanVar(value=True)
        self.flatten_check = ttk.Checkbutton(self.options_frame, text="启用代码平坦化", variable=self.flatten_var)
        
        self.name_var = tk.BooleanVar(value=True)
        self.name_check = ttk.Checkbutton(self.options_frame, text="启用函数名混淆", variable=self.name_var)
        
        self.pyc_var = tk.BooleanVar(value=False)
        self.pyc_check = ttk.Checkbutton(self.options_frame, text="编译为pyc文件并插入NOP指令", variable=self.pyc_var, command=self.toggle_pyc)
        
        self.nop_label = ttk.Label(self.options_frame, text="NOP指令比例:")
        self.nop_ratio = ttk.Scale(self.options_frame, from_=0.0, to=0.5, orient=tk.HORIZONTAL, length=200)
        self.nop_ratio.set(0.2)  # 默认值
        self.nop_value = ttk.Label(self.options_frame, text="0.2")
        
        # 绑定Scale的值变化事件
        self.nop_ratio.bind("<Motion>", self.update_nop_value)
        
        # 操作按钮区域
        self.buttons_frame = ttk.Frame(self)
        
        self.obfuscate_button = ttk.Button(self.buttons_frame, text="开始混淆", command=self.start_obfuscation)
        self.clear_button = ttk.Button(self.buttons_frame, text="清除", command=self.clear_form)
        
        # 输出区域
        self.output_frame = ttk.LabelFrame(self, text="日志输出")
        self.log_output = ScrolledText(self.output_frame, width=80, height=15)
        self.log_output.config(state=tk.DISABLED)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
    
    def setup_layout(self):
        # 文件选择区域布局
        self.file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.input_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.input_path.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        self.input_browse.grid(row=0, column=2, padx=5, pady=5)
        
        self.output_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.output_path.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        self.output_browse.grid(row=1, column=2, padx=5, pady=5)
        
        # 设置列权重，使输入框可以随窗口调整大小
        self.file_frame.columnconfigure(1, weight=1)
        
        # 混淆选项区
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.flatten_check.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_check.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.pyc_check.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.nop_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.nop_ratio.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        self.nop_value.grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        

        self.toggle_pyc()
        
        # 按钮区域
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.obfuscate_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 输出区
        self.output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.log_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 状态栏
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def browse_input(self):
        """浏览并选择输入文件"""
        filename = filedialog.askopenfilename(
            title="选择Python文件",
            filetypes=[("Python文件", "*.py"), ("所有文件", "*.*")]
        )
        if filename:
            self.input_path.delete(0, tk.END)
            self.input_path.insert(0, filename)
            
            # 如果输出路径为空，自动设置为同目录同名文件
            if not self.output_path.get():
                default_output = filename
                if self.pyc_var.get():
                    default_output = os.path.splitext(filename)[0] + '.pyc'
                else:
                    default_output = os.path.splitext(filename)[0] + '_obfuscated.py'
                self.output_path.delete(0, tk.END)
                self.output_path.insert(0, default_output)
    
    def browse_output(self):
        """浏览并选择输出文件"""
        if self.pyc_var.get():
            filetypes = [("Python编译文件", "*.pyc"), ("所有文件", "*.*")]
            defaultext = '.pyc'
        else:
            filetypes = [("Python文件", "*.py"), ("所有文件", "*.*")]
            defaultext = '.py'
            
        filename = filedialog.asksaveasfilename(
            title="保存混淆后的文件",
            filetypes=filetypes,
            defaultextension=defaultext
        )
        if filename:
            self.output_path.delete(0, tk.END)
            self.output_path.insert(0, filename)
    
    def toggle_pyc(self):
        """切换pyc选项状态"""
        if self.pyc_var.get():
            # 启用NOP比例调整
            self.nop_label.config(state=tk.NORMAL)
            self.nop_ratio.config(state=tk.NORMAL)
            self.nop_value.config(state=tk.NORMAL)
            
            # 如果已有输出路径，检查是否需要修改扩展名
            output = self.output_path.get()
            if output and not output.endswith('.pyc'):
                output = os.path.splitext(output)[0] + '.pyc'
                self.output_path.delete(0, tk.END)
                self.output_path.insert(0, output)
        else:
            # 禁用NOP比例调整
            self.nop_label.config(state=tk.DISABLED)
            self.nop_ratio.config(state=tk.DISABLED)
            self.nop_value.config(state=tk.DISABLED)
            
            # 如果已有输出路径，检查是否需要修改扩展名
            output = self.output_path.get()
            if output and output.endswith('.pyc'):
                output = os.path.splitext(output)[0] + '.py'
                self.output_path.delete(0, tk.END)
                self.output_path.insert(0, output)
    
    def update_nop_value(self, event=None):
        """更新NOP比例显示值"""
        value = round(self.nop_ratio.get(), 2)
        self.nop_value.config(text=str(value))
    
    def log(self, message):
        """向日志输出区域添加消息"""
        self.log_output.config(state=tk.NORMAL)
        self.log_output.insert(tk.END, message + "\n")
        self.log_output.see(tk.END)
        self.log_output.config(state=tk.DISABLED)
        
        # 更新UI
        self.update()
    
    def clear_form(self):
        """清除表单"""
        self.input_path.delete(0, tk.END)
        self.output_path.delete(0, tk.END)
        
        self.flatten_var.set(True)
        self.name_var.set(True)
        self.pyc_var.set(False)
        self.nop_ratio.set(0.2)
        self.update_nop_value()
        
        self.toggle_pyc()
        
        self.log_output.config(state=tk.NORMAL)
        self.log_output.delete(1.0, tk.END)
        self.log_output.config(state=tk.DISABLED)
        
        self.status_var.set("已清除")
    
    def start_obfuscation(self):
        """开始混淆处理"""
        input_file = self.input_path.get().strip()
        output_file = self.output_path.get().strip()
        
        # 参数验证
        if not input_file:
            messagebox.showerror("错误", "请选择输入文件!")
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror("错误", f"输入文件不存在: {input_file}")
            return
        
        if not output_file:
            messagebox.showerror("错误", "请指定输出文件!")
            return
        
        # 获取选项
        flatten_code = self.flatten_var.get()
        obfuscate_names = self.name_var.get()
        compile_to_pyc = self.pyc_var.get()
        nop_ratio = round(self.nop_ratio.get(), 2)
        
        # 日志清空
        self.log_output.config(state=tk.NORMAL)
        self.log_output.delete(1.0, tk.END)
        self.log_output.config(state=tk.DISABLED)
        
        # 更新状态
        self.status_var.set("正在混淆...")
        
        # 打印混淆选项
        self.log(f"输入文件: {input_file}")
        self.log(f"输出文件: {output_file}")
        self.log(f"代码平坦化: {'启用' if flatten_code else '禁用'}")
        self.log(f"函数名混淆: {'启用' if obfuscate_names else '禁用'}")
        self.log(f"编译为pyc: {'启用' if compile_to_pyc else '禁用'}")
        if compile_to_pyc:
            self.log(f"NOP指令比例: {nop_ratio}")
        self.log("-" * 50)
        
        # 执行混淆
        try:
            result = obfuscate_file(
                input_file=input_file,
                output_file=output_file,
                flatten_code=flatten_code,
                obfuscate_names=obfuscate_names,
                compile_to_pyc=compile_to_pyc,
                nop_ratio=nop_ratio
            )
            
            # 输出结果
            if isinstance(result, str):
                self.log(result)
            else:
                self.log("混淆成功完成!")
            
            # 成功完成
            self.status_var.set("混淆完成")
            messagebox.showinfo("成功", "混淆处理已完成!")
            
        except Exception as e:
            import traceback
            error_msg = str(e)
            self.log(f"错误: {error_msg}")
            self.log(traceback.format_exc())
            
            self.status_var.set("混淆失败")
            messagebox.showerror("错误", f"混淆处理失败!\n{error_msg}")


def main():
    """UI主函数"""
    app = ObfuscatorUI()
    app.mainloop()


if __name__ == "__main__":
    main() 