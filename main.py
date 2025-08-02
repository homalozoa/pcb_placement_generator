#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PCB元器件位号图生成器
支持从CSV文件生成PCB正反面的位号图PDF文件
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
from pathlib import Path
import threading
from typing import Optional

# 导入自定义模块
from csv_parser import CSVParser
from pdf_generator import PDFGenerator
from config import Config
from error_handler import (
    get_error_handler, handle_errors, ValidationError,
    validate_csv_file, validate_output_directory, check_dependencies
)


class PCBLayoutGenerator:
    """PCB位号图生成器主程序"""
    
    def __init__(self):
        # 初始化错误处理器
        self.error_handler = get_error_handler()

        # 检查依赖
        try:
            check_dependencies()
        except ImportError as e:
            messagebox.showerror("依赖错误", str(e))
            sys.exit(1)

        self.root = tk.Tk()
        self.root.title("PCB元器件位号图生成器 v1.0")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # 配置
        self.config = Config()

        # 变量
        self.csv_file_path = tk.StringVar()
        self.output_dir_path = tk.StringVar()
        self.generate_refdes = tk.BooleanVar(value=True)
        self.generate_package = tk.BooleanVar(value=True)
        self.generate_value = tk.BooleanVar(value=True)
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="就绪")

        # 初始化界面
        self.setup_ui()

        # 设置默认输出目录为当前目录
        self.output_dir_path.set(os.getcwd())
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # CSV文件选择
        ttk.Label(file_frame, text="CSV文件:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Entry(file_frame, textvariable=self.csv_file_path, state="readonly").grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=(0, 5)
        )
        ttk.Button(file_frame, text="浏览...", command=self.select_csv_file).grid(
            row=0, column=2, pady=(0, 5)
        )
        
        # 输出目录选择
        ttk.Label(file_frame, text="输出目录:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(file_frame, textvariable=self.output_dir_path, state="readonly").grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5)
        )
        ttk.Button(file_frame, text="浏览...", command=self.select_output_dir).grid(
            row=1, column=2
        )
        
        # 生成选项区域
        options_frame = ttk.LabelFrame(main_frame, text="生成选项", padding="10")
        options_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(options_frame, text="生成编号图 (RefDes)", 
                       variable=self.generate_refdes).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="生成封装图 (Package)", 
                       variable=self.generate_package).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="生成值图 (Value)", 
                       variable=self.generate_value).grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # 说明文本
        info_frame = ttk.LabelFrame(main_frame, text="说明", padding="10")
        info_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        info_text = tk.Text(info_frame, height=8, wrap=tk.WORD, state="disabled")
        info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=info_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        info_text.configure(yscrollcommand=scrollbar.set)
        
        # 插入说明文本
        info_content = """程序功能说明：

1. 选择包含PCB元器件位置信息的CSV文件
2. 选择PDF文件的输出目录
3. 选择要生成的图纸类型（编号、封装、值）
4. 程序将自动生成正面(Top)和反面(Bottom)的位号图
5. 生成的PDF文件将保存在输出目录下的CSV同名子目录中

CSV文件格式要求：
- 第一行为标题行：Num,RefDes,PartDecal,X,Y,Layer,Orient.,value
- 数据行包含：序号、编号、封装、X坐标、Y坐标、层面、角度、值
- 层面字段支持：Top（正面）、Bottom（反面）

生成的文件：
- RefDes_Top.pdf / RefDes_Bottom.pdf（编号图）
- Package_Top.pdf / Package_Bottom.pdf（封装图）  
- Value_Top.pdf / Value_Bottom.pdf（值图）"""
        
        info_text.configure(state="normal")
        info_text.insert("1.0", info_content)
        info_text.configure(state="disabled")
        
        # 控制按钮区域
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(0, weight=1)
        
        # 生成按钮
        self.generate_button = ttk.Button(control_frame, text="生成PDF", 
                                        command=self.start_generation, style="Accent.TButton")
        self.generate_button.grid(row=0, column=0, pady=5)
        
        # 进度条
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 状态标签
        self.status_label = ttk.Label(control_frame, textvariable=self.status_var)
        self.status_label.grid(row=2, column=0, pady=5)
    
    def select_csv_file(self):
        """选择CSV文件"""
        file_path = filedialog.askopenfilename(
            title="选择CSV文件",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )
        if file_path:
            self.csv_file_path.set(file_path)
    
    def select_output_dir(self):
        """选择输出目录"""
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_dir_path.set(dir_path)
    
    def validate_inputs(self) -> bool:
        """验证输入参数"""
        try:
            # 验证CSV文件
            validate_csv_file(self.csv_file_path.get())

            # 验证输出目录
            validate_output_directory(self.output_dir_path.get())

            # 验证生成选项
            if not (self.generate_refdes.get() or self.generate_package.get() or self.generate_value.get()):
                raise ValidationError("请至少选择一种生成选项")

            return True

        except ValidationError as e:
            messagebox.showerror("验证错误", str(e))
            return False
        except Exception as e:
            messagebox.showerror("验证错误", f"验证过程中发生错误: {str(e)}")
            return False
    
    def start_generation(self):
        """开始生成PDF"""
        if not self.validate_inputs():
            return
        
        # 禁用生成按钮
        self.generate_button.configure(state="disabled")
        self.progress_var.set(0)
        self.status_var.set("正在生成...")
        
        # 在新线程中执行生成任务
        thread = threading.Thread(target=self.generate_pdfs)
        thread.daemon = True
        thread.start()
    
    def generate_pdfs(self):
        """生成PDF文件（在后台线程中执行）"""
        try:
            # 解析CSV文件
            self.update_progress(10, "正在解析CSV文件...")
            parser = CSVParser()
            components = parser.parse_file(self.csv_file_path.get())
            
            # 创建输出目录
            csv_filename = Path(self.csv_file_path.get()).stem
            output_dir = Path(self.output_dir_path.get()) / csv_filename
            output_dir.mkdir(exist_ok=True)
            
            # 初始化PDF生成器
            generator = PDFGenerator(self.config)
            
            # 计算总任务数
            total_tasks = 0
            if self.generate_refdes.get():
                total_tasks += 2  # Top + Bottom
            if self.generate_package.get():
                total_tasks += 2
            if self.generate_value.get():
                total_tasks += 2
            
            current_task = 0
            
            # 生成编号图
            if self.generate_refdes.get():
                self.update_progress(20 + (current_task * 60 // total_tasks), "正在生成编号图...")
                generator.generate_refdes_pdf(components, output_dir)
                current_task += 2
            
            # 生成封装图
            if self.generate_package.get():
                self.update_progress(20 + (current_task * 60 // total_tasks), "正在生成封装图...")
                generator.generate_package_pdf(components, output_dir)
                current_task += 2
            
            # 生成值图
            if self.generate_value.get():
                self.update_progress(20 + (current_task * 60 // total_tasks), "正在生成值图...")
                generator.generate_value_pdf(components, output_dir)
                current_task += 2
            
            self.update_progress(100, "生成完成！")
            
            # 显示成功消息
            self.root.after(0, lambda: messagebox.showinfo(
                "成功", f"PDF文件已生成完成！\n输出目录：{output_dir}"
            ))
            
        except Exception as e:
            error_msg = f"生成PDF时发生错误：{str(e)}"
            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))
            self.update_progress(0, "生成失败")
        
        finally:
            # 重新启用生成按钮
            self.root.after(0, lambda: self.generate_button.configure(state="normal"))
    
    def update_progress(self, value: float, status: str):
        """更新进度条和状态"""
        self.root.after(0, lambda: self.progress_var.set(value))
        self.root.after(0, lambda: self.status_var.set(status))
    
    def run(self):
        """运行程序"""
        self.root.mainloop()


def main():
    """主函数"""
    try:
        app = PCBLayoutGenerator()
        app.run()
    except Exception as e:
        messagebox.showerror("致命错误", f"程序启动失败：{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
