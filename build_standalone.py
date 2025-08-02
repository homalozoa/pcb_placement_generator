#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立二进制文件打包脚本
使用PyInstaller将程序打包为完全独立的可执行文件
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def check_pyinstaller():
    """检查并安装PyInstaller"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller已安装，版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("PyInstaller未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller安装成功")
            return True
        except subprocess.CalledProcessError:
            print("✗ PyInstaller安装失败")
            return False


def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"✓ 清理目录: {dir_name}")
    
    for pattern in files_to_clean:
        for file_path in Path('.').glob(pattern):
            file_path.unlink()
            print(f"✓ 清理文件: {file_path}")


def build_standalone():
    """构建独立可执行文件"""
    print("开始构建独立可执行文件...")
    
    # 构建参数
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # 单文件模式
        "--console",  # 控制台应用
        "--name", "pcb-generator",
        "--clean",
        "--noconfirm",
        
        # 包含的模块
        "--hidden-import", "matplotlib.backends.backend_pdf",
        "--hidden-import", "matplotlib.backends.backend_agg", 
        "--hidden-import", "numpy.core._methods",
        "--hidden-import", "numpy.lib.format",
        "--hidden-import", "csv_parser",
        "--hidden-import", "pdf_generator",
        "--hidden-import", "config",
        "--hidden-import", "error_handler",
        
        # 排除的模块（减小文件大小）
        "--exclude-module", "tkinter",
        "--exclude-module", "matplotlib.backends.backend_tkagg",
        "--exclude-module", "matplotlib.backends.backend_qt5agg",
        "--exclude-module", "PyQt5",
        "--exclude-module", "PyQt6",
        "--exclude-module", "PySide2",
        "--exclude-module", "PySide6",
        "--exclude-module", "IPython",
        "--exclude-module", "jupyter",
        "--exclude-module", "scipy",
        "--exclude-module", "pandas",
        "--exclude-module", "sklearn",
        "--exclude-module", "tensorflow",
        "--exclude-module", "torch",
        
        # 主入口文件
        "cli_main.py"
    ]
    
    print(f"执行命令: {' '.join(cmd[:10])}...")  # 只显示前几个参数
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ 构建成功！")
            return True
        else:
            print("✗ 构建失败！")
            print("错误输出:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ 构建过程中发生错误: {e}")
        return False


def create_distribution():
    """创建分发包"""
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("✗ dist目录不存在，构建可能失败")
        return False

    # 检查可执行文件
    system = platform.system().lower()
    if system == 'windows':
        exe_name = 'pcb-generator.exe'
    else:
        exe_name = 'pcb-generator'

    exe_path = dist_dir / exe_name
    if not exe_path.exists():
        print(f"✗ 可执行文件不存在: {exe_path}")
        return False
    
    # 创建README文件
    readme_content = """# PCB Generator - 独立可执行文件

## 使用方法

### 命令行使用
```bash
# 生成所有类型的PDF
./pcb-generator input.csv

# 指定输出目录
./pcb-generator input.csv -o output_dir

# 只生成编号图
./pcb-generator input.csv --refdes-only

# 只生成封装图  
./pcb-generator input.csv --package-only

# 只生成值图
./pcb-generator input.csv --value-only

# 查看帮助
./pcb-generator --help
```

### CSV文件格式
```csv
Num,RefDes,PartDecal,X,Y,Layer,Orient.,value
1,CN2,SD-V2,22.798,-0.898,Top,0,SD
2,CN3,DP-8-18000,-9,37.5,Top,270,DP_SMD
3,C1,C0603,78.389,19.541,Bottom,180,10uF
```

### 输出文件
程序会生成以下PDF文件：
- RefDes_Top.pdf / RefDes_Bottom.pdf（编号图）
- Package_Top.pdf / Package_Bottom.pdf（封装图）
- Value_Top.pdf / Value_Bottom.pdf（值图）

## 特性
- 完全独立，无需安装Python环境
- 支持密集布局的智能文字排版
- 基于0201封装优化的字体大小
- 高质量PDF输出
- 跨平台支持

## 系统要求
- 无特殊要求，可在任何现代操作系统上运行

## 技术支持
如有问题，请联系开发团队。
"""
    
    readme_path = dist_dir / 'README.md'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✓ 创建说明文件: {readme_path}")
    
    # 显示文件信息
    file_size = exe_path.stat().st_size / (1024 * 1024)  # MB
    print(f"✓ 可执行文件: {exe_path} ({file_size:.1f} MB)")
    
    return True


def main():
    """主函数"""
    print("PCB Generator - 独立二进制文件构建器")
    print("=" * 50)
    
    # 检查PyInstaller
    if not check_pyinstaller():
        return False
    
    # 清理构建目录
    print("\n清理构建目录...")
    clean_build_dirs()
    
    # 构建可执行文件
    print("\n构建独立可执行文件...")
    if not build_standalone():
        return False
    
    # 创建分发包
    print("\n创建分发包...")
    if not create_distribution():
        return False
    
    print("\n" + "=" * 50)
    print("✓ 构建完成！")
    print("\n生成的文件:")
    
    dist_dir = Path('dist')
    for file_path in dist_dir.iterdir():
        if file_path.is_file():
            size = file_path.stat().st_size / (1024 * 1024)  # MB
            print(f"  {file_path} ({size:.1f} MB)")
    
    print(f"\n独立可执行文件位于: {dist_dir.absolute()}")
    print("可以将整个dist目录分发给用户使用。")
    
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        print("\n✗ 构建失败")
        sys.exit(1)
    else:
        print("\n✓ 构建成功")
        sys.exit(0)
