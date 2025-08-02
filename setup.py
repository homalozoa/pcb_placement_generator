#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装脚本
用于安装依赖和设置开发环境
"""

import sys
import subprocess
import os
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"错误: 需要Python 3.8或更高版本，当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True


def install_requirements():
    """安装依赖包"""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("错误: requirements.txt文件不存在")
        return False
    
    print("正在安装依赖包...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("依赖包安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖包安装失败: {e}")
        return False


def install_pyinstaller():
    """安装PyInstaller（用于打包）"""
    print("正在安装PyInstaller...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "pyinstaller"
        ])
        print("PyInstaller安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"PyInstaller安装失败: {e}")
        return False


def test_imports():
    """测试导入"""
    test_modules = [
        ('matplotlib', 'matplotlib'),
        ('numpy', 'numpy'),
        ('reportlab', 'reportlab'),
        ('PIL', 'Pillow'),
        ('tkinter', '内置模块'),
    ]
    
    print("测试模块导入...")
    failed_modules = []
    
    for module_name, package_name in test_modules:
        try:
            __import__(module_name)
            print(f"✓ {module_name} ({package_name})")
        except ImportError:
            print(f"✗ {module_name} ({package_name})")
            failed_modules.append(package_name)
    
    if failed_modules:
        print(f"\n以下模块导入失败: {', '.join(failed_modules)}")
        return False
    
    print("所有模块导入成功")
    return True


def create_test_csv():
    """创建测试CSV文件"""
    test_csv_content = """Num,RefDes,PartDecal,X,Y,Layer,Orient.,value
1,CN2,SD-V2,22.798,-0.898,Top,0,SD
2,CN3,DP-8-18000,-9,37.5,Top,270,DP_SMD
3,CON2,RJ45-1A,-10.4,14.3,Top,270,RJ45
4,C1,C0603,78.389,19.541,Bottom,180,10uF
5,C17,C0603,57.46,30.087,Bottom,90,10uF
6,R1,R0402,88.875,19.116,Top,270,10K
7,U1,QFN64,82.001,24.568,Top,270,GL3510
8,Q1,SOT23,120.795,8.875,Top,270,TF3401"""
    
    test_file = Path("test_sample.csv")
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_csv_content)
    
    print(f"已创建测试CSV文件: {test_file}")


def run_test():
    """运行简单测试"""
    print("运行程序测试...")
    
    try:
        # 测试CSV解析
        from csv_parser import CSVParser
        parser = CSVParser()
        
        # 创建测试文件
        create_test_csv()
        
        # 解析测试文件
        components = parser.parse_file("test_sample.csv")
        print(f"CSV解析测试通过: 解析了 {len(components['all'])} 个元器件")
        
        # 测试配置
        from config import Config
        config = Config()
        if config.validate():
            print("配置验证测试通过")
        else:
            print("配置验证测试失败")
            return False
        
        # 清理测试文件
        os.remove("test_sample.csv")
        
        print("所有测试通过")
        return True
        
    except Exception as e:
        print(f"测试失败: {e}")
        return False


def main():
    """主函数"""
    print("PCB位号图生成器 - 安装脚本")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    # 安装依赖包
    if not install_requirements():
        return False
    
    # 安装PyInstaller
    if not install_pyinstaller():
        print("警告: PyInstaller安装失败，但不影响程序运行")
    
    # 测试导入
    if not test_imports():
        return False
    
    # 运行测试
    if not run_test():
        return False
    
    print("\n" + "=" * 50)
    print("安装完成！")
    print("\n使用说明:")
    print("1. 运行程序: python main.py")
    print("2. 打包程序: python build.py")
    print("3. 查看帮助: python main.py --help")
    
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        print("\n安装失败，请检查错误信息并重试")
        sys.exit(1)
    else:
        print("\n安装成功！")
        sys.exit(0)
