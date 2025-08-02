#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本
使用PyInstaller将程序打包为可执行文件
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print(f"PyInstaller版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("PyInstaller未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            return True
        except subprocess.CalledProcessError:
            print("PyInstaller安装失败，请手动安装: pip install pyinstaller")
            return False


def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 清理.spec文件
    for spec_file in Path('.').glob('*.spec'):
        print(f"删除文件: {spec_file}")
        spec_file.unlink()


def create_spec_file():
    """创建PyInstaller规格文件"""
    system = platform.system().lower()

    # 确定主入口文件
    main_script = 'cli_main.py'  # 使用命令行版本作为主入口，避免tkinter依赖问题

    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{main_script}'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.py', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'matplotlib.backends.backend_pdf',
        'matplotlib.backends.backend_agg',
        'matplotlib.figure',
        'matplotlib.pyplot',
        'matplotlib.patches',
        'numpy.core._methods',
        'numpy.lib.format',
        'reportlab.pdfgen.canvas',
        'reportlab.lib.pagesizes',
        'reportlab.lib.colors',
        'csv_parser',
        'pdf_generator',
        'config',
        'error_handler',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'matplotlib.backends.backend_qt5agg',
        'matplotlib.backends.backend_gtk3agg',
        'matplotlib.backends.backend_tkagg',
        'tkinter',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'IPython',
        'jupyter',
        'notebook',
        'scipy',
        'pandas',
        'sklearn',
        'tensorflow',
        'torch',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='pcb-generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)'''

    if system == 'darwin':  # macOS
        spec_content += '''

app = BUNDLE(
    exe,
    name='PCB-Generator.app',
    icon=None,
    bundle_identifier='com.pcbgenerator.cli',
    info_plist={{
        'CFBundleDisplayName': 'PCB Generator',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSBackgroundOnly': False,
    }},
)'''

    with open('pcb_generator.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("已创建PyInstaller规格文件: pcb_generator.spec")


def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    try:
        # 使用spec文件构建
        cmd = [sys.executable, "-m", "PyInstaller", "pcb_generator.spec"]
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("构建成功！")
            print(result.stdout)
            return True
        else:
            print("构建失败！")
            print("错误输出:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"构建过程中发生错误: {e}")
        return False


def copy_resources():
    """复制资源文件"""
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("dist目录不存在，构建可能失败")
        return
    
    # 复制README文件
    readme_content = """# PCB元器件位号图生成器

## 使用说明

1. 运行程序
2. 选择包含PCB元器件位置信息的CSV文件
3. 选择PDF文件的输出目录
4. 选择要生成的图纸类型（编号、封装、值）
5. 点击"生成PDF"按钮

## CSV文件格式

CSV文件应包含以下列：
- Num: 序号
- RefDes: 元器件编号
- PartDecal: 封装类型
- X: X坐标（毫米）
- Y: Y坐标（毫米）
- Layer: 层面（Top/Bottom）
- Orient.: 角度
- value: 元器件值

## 输出文件

程序会在输出目录下创建与CSV文件同名的子目录，并生成以下PDF文件：
- RefDes_Top.pdf / RefDes_Bottom.pdf（编号图）
- Package_Top.pdf / Package_Bottom.pdf（封装图）
- Value_Top.pdf / Value_Bottom.pdf（值图）

## 技术支持

如有问题，请检查：
1. CSV文件格式是否正确
2. 文件编码是否为UTF-8或GBK
3. 输出目录是否有写入权限

版本: 1.0.0
"""
    
    readme_file = dist_dir / "README.txt"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"已创建说明文件: {readme_file}")


def main():
    """主函数"""
    print("PCB位号图生成器 - 打包脚本")
    print("=" * 50)
    
    # 检查PyInstaller
    if not check_pyinstaller():
        return False
    
    # 清理构建目录
    clean_build_dirs()
    
    # 创建规格文件
    create_spec_file()
    
    # 构建可执行文件
    if not build_executable():
        return False
    
    # 复制资源文件
    copy_resources()
    
    # 显示结果
    system = platform.system().lower()
    if system == 'windows':
        exe_path = Path('dist') / 'pcb-generator.exe'
    elif system == 'darwin':
        exe_path = Path('dist') / 'PCB-Generator.app'
    else:
        exe_path = Path('dist') / 'pcb-generator'
    
    if exe_path.exists():
        print(f"\n构建完成！可执行文件位置: {exe_path.absolute()}")
        print(f"文件大小: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        
        # 显示分发说明
        print("\n分发说明:")
        print("1. 将整个dist目录复制到目标机器")
        print("2. 运行可执行文件即可使用")
        print("3. 无需安装Python或其他依赖")
        
        return True
    else:
        print("\n构建失败：找不到可执行文件")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
