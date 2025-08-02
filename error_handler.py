#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误处理模块
提供统一的错误处理和用户友好的错误信息
"""

import sys
import traceback
import logging
from typing import Optional, Callable, Any
from functools import wraps

# 尝试导入tkinter，如果失败则设置为None
try:
    import tkinter as tk
    from tkinter import messagebox
    HAS_TKINTER = True
except ImportError:
    tk = None
    messagebox = None
    HAS_TKINTER = False


class ErrorHandler:
    """错误处理器"""
    
    def __init__(self, log_file: Optional[str] = None):
        self.log_file = log_file
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        
        if self.log_file:
            logging.basicConfig(
                level=logging.INFO,
                format=log_format,
                handlers=[
                    logging.FileHandler(self.log_file, encoding='utf-8'),
                    logging.StreamHandler(sys.stdout)
                ]
            )
        else:
            logging.basicConfig(
                level=logging.INFO,
                format=log_format,
                handlers=[logging.StreamHandler(sys.stdout)]
            )
        
        self.logger = logging.getLogger(__name__)
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """全局异常处理器"""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.logger.error(f"未捕获的异常: {error_msg}")
        
        # 显示用户友好的错误消息
        user_msg = self.get_user_friendly_message(exc_type, exc_value)
        try:
            if HAS_TKINTER and messagebox:
                messagebox.showerror("程序错误", user_msg)
            else:
                print(f"错误: {user_msg}")
        except:
            print(f"错误: {user_msg}")
    
    def get_user_friendly_message(self, exc_type, exc_value) -> str:
        """获取用户友好的错误消息"""
        error_messages = {
            FileNotFoundError: "文件未找到，请检查文件路径是否正确。",
            PermissionError: "权限不足，请检查文件或目录的访问权限。",
            UnicodeDecodeError: "文件编码错误，请确保CSV文件使用UTF-8或GBK编码。",
            ValueError: "数据格式错误，请检查CSV文件格式是否正确。",
            MemoryError: "内存不足，请尝试处理较小的文件或关闭其他程序。",
            ImportError: "缺少必要的库，请运行 'pip install -r requirements.txt' 安装依赖。",
        }
        
        for error_type, message in error_messages.items():
            if isinstance(exc_value, error_type):
                return f"{message}\n\n详细错误: {str(exc_value)}"
        
        return f"程序发生未知错误，请联系开发者。\n\n错误类型: {exc_type.__name__}\n错误信息: {str(exc_value)}"
    
    def safe_execute(self, func: Callable, *args, **kwargs) -> tuple[bool, Any]:
        """安全执行函数"""
        try:
            result = func(*args, **kwargs)
            return True, result
        except Exception as e:
            self.logger.error(f"执行函数 {func.__name__} 时发生错误: {str(e)}")
            return False, str(e)


def handle_errors(error_handler: Optional[ErrorHandler] = None):
    """错误处理装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if error_handler:
                    error_handler.logger.error(f"函数 {func.__name__} 执行错误: {str(e)}")
                    user_msg = error_handler.get_user_friendly_message(type(e), e)
                    try:
                        if HAS_TKINTER and messagebox:
                            messagebox.showerror("错误", user_msg)
                        else:
                            print(f"错误: {user_msg}")
                    except:
                        print(f"错误: {user_msg}")
                else:
                    print(f"函数 {func.__name__} 执行错误: {str(e)}")
                raise
        return wrapper
    return decorator


class ValidationError(Exception):
    """验证错误"""
    pass


class CSVFormatError(Exception):
    """CSV格式错误"""
    pass


class PDFGenerationError(Exception):
    """PDF生成错误"""
    pass


def validate_csv_file(file_path: str) -> bool:
    """验证CSV文件"""
    import os
    
    if not file_path:
        raise ValidationError("请选择CSV文件")
    
    if not os.path.exists(file_path):
        raise ValidationError("CSV文件不存在")
    
    if not file_path.lower().endswith(('.csv', '.txt')):
        raise ValidationError("文件格式不正确，请选择CSV文件")
    
    # 检查文件大小
    file_size = os.path.getsize(file_path)
    if file_size == 0:
        raise ValidationError("CSV文件为空")
    
    if file_size > 50 * 1024 * 1024:  # 50MB
        raise ValidationError("CSV文件过大（超过50MB），请选择较小的文件")
    
    return True


def validate_output_directory(dir_path: str) -> bool:
    """验证输出目录"""
    import os
    
    if not dir_path:
        raise ValidationError("请选择输出目录")
    
    if not os.path.exists(dir_path):
        raise ValidationError("输出目录不存在")
    
    if not os.path.isdir(dir_path):
        raise ValidationError("输出路径不是有效的目录")
    
    # 检查写入权限
    test_file = os.path.join(dir_path, 'test_write_permission.tmp')
    try:
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
    except Exception:
        raise ValidationError("输出目录没有写入权限")
    
    return True


def check_dependencies() -> bool:
    """检查依赖库"""
    required_modules = [
        ('matplotlib', 'matplotlib'),
        ('numpy', 'numpy'),
        ('reportlab', 'reportlab'),
        ('PIL', 'Pillow'),
    ]
    
    missing_modules = []
    
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
        except ImportError:
            missing_modules.append(package_name)
    
    if missing_modules:
        error_msg = f"缺少以下依赖库: {', '.join(missing_modules)}\n"
        error_msg += "请运行以下命令安装:\n"
        error_msg += f"pip install {' '.join(missing_modules)}"
        raise ImportError(error_msg)
    
    return True


def setup_global_error_handler():
    """设置全局错误处理器"""
    error_handler = ErrorHandler('pcb_generator.log')
    sys.excepthook = error_handler.handle_exception
    return error_handler


# 创建全局错误处理器实例
global_error_handler = None


def get_error_handler() -> ErrorHandler:
    """获取全局错误处理器"""
    global global_error_handler
    if global_error_handler is None:
        global_error_handler = setup_global_error_handler()
    return global_error_handler


def test_error_handler():
    """测试错误处理器"""
    handler = ErrorHandler()
    
    # 测试安全执行
    def test_func(x, y):
        if y == 0:
            raise ValueError("除数不能为零")
        return x / y
    
    success, result = handler.safe_execute(test_func, 10, 2)
    print(f"成功: {success}, 结果: {result}")
    
    success, result = handler.safe_execute(test_func, 10, 0)
    print(f"成功: {success}, 错误: {result}")
    
    # 测试验证函数
    try:
        validate_csv_file("")
    except ValidationError as e:
        print(f"验证错误: {e}")
    
    try:
        check_dependencies()
        print("依赖检查通过")
    except ImportError as e:
        print(f"依赖检查失败: {e}")


if __name__ == "__main__":
    test_error_handler()
