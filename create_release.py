#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建发布包脚本
生成完整的独立发布包，包含可执行文件、文档和示例
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path
import zipfile
import tarfile


def create_sample_csv():
    """创建示例CSV文件"""
    sample_content = """Num,RefDes,PartDecal,X,Y,Layer,Orient.,value
1,R1,R0201,10.0,20.0,Top,0,10K
2,R2,R0201,10.5,20.0,Top,0,1K
3,R3,R0201,11.0,20.0,Top,0,100
4,C1,C0201,10.0,20.5,Top,0,100nF
5,C2,C0201,10.5,20.5,Top,0,10uF
6,C3,C0201,11.0,20.5,Top,0,1nF
7,U1,QFN-32,25.0,30.0,Top,0,MCU
8,U2,SOT-23,15.0,25.0,Top,0,LDO
9,L1,L0805,35.0,30.0,Top,0,10uH
10,R10,R0201,13.0,21.0,Bottom,0,0R
11,R11,R0201,13.5,21.0,Bottom,0,33R
12,C10,C0201,13.0,21.5,Bottom,0,4.7uF
"""
    return sample_content


def create_user_manual():
    """创建用户手册"""
    manual_content = """# PCB Generator 用户手册

## 概述

PCB Generator 是一个专业的PCB元器件位号图生成工具，能够从CSV文件生成高质量的PDF位号图。

## 主要特性

- ✅ **完全独立**：无需安装Python环境，开箱即用
- ✅ **智能布局**：自动避免文字重叠，优化密集布局
- ✅ **精确对应**：文字中心精确对应元器件坐标
- ✅ **0201优化**：基于0201封装优化字体大小
- ✅ **高质量输出**：生成矢量PDF文件，支持任意缩放
- ✅ **多种类型**：支持编号图、封装图、值图
- ✅ **双面支持**：自动分离正面和反面元器件

## 快速开始

### 1. 准备CSV文件

CSV文件必须包含以下列（顺序固定）：
```
Num,RefDes,PartDecal,X,Y,Layer,Orient.,value
```

- **Num**: 序号
- **RefDes**: 元器件编号（如R1, C2, U3）
- **PartDecal**: 封装类型（如R0603, C0402, QFN48）
- **X**: X坐标（毫米）
- **Y**: Y坐标（毫米）
- **Layer**: 层面（Top或Bottom）
- **Orient.**: 角度（度）
- **value**: 元器件值（如10K, 100nF, MCU）

### 2. 运行程序

#### 基本用法
```bash
# 生成所有类型的PDF
./pcb-generator sample.csv

# 指定输出目录
./pcb-generator sample.csv -o output_folder
```

#### 选择性生成
```bash
# 只生成编号图
./pcb-generator sample.csv --refdes-only

# 只生成封装图
./pcb-generator sample.csv --package-only

# 只生成值图
./pcb-generator sample.csv --value-only

# 生成编号图和封装图
./pcb-generator sample.csv -r -p
```

#### 高级选项
```bash
# 高质量输出
./pcb-generator sample.csv --quality high

# 详细输出
./pcb-generator sample.csv --verbose

# 查看帮助
./pcb-generator --help
```

### 3. 输出文件

程序会在输出目录下创建与CSV文件同名的子目录，包含以下PDF文件：

- `RefDes_Top.pdf` - 正面编号图
- `RefDes_Bottom.pdf` - 反面编号图
- `Package_Top.pdf` - 正面封装图
- `Package_Bottom.pdf` - 反面封装图
- `Value_Top.pdf` - 正面值图
- `Value_Bottom.pdf` - 反面值图

## 技术特性

### 智能文字布局
- 文字中心精确对应元器件坐标点
- 自动检测并避免文字重叠
- 基于元器件密度动态调整字体大小
- 优先使用原始坐标位置

### 0201封装优化
- 字体大小基于0201封装尺寸（0.6mm x 0.3mm）计算
- 确保在最密集的布局中也能保持可读性
- 动态缓冲区避免文字重叠

### 高质量输出
- 矢量PDF格式，支持无损缩放
- 300 DPI高分辨率
- 专业的排版和字体渲染

## 故障排除

### 常见问题

**Q: 程序无法启动**
A: 确保文件有执行权限：`chmod +x pcb-generator`

**Q: CSV文件解析失败**
A: 检查CSV文件格式，确保列名和数据格式正确

**Q: 生成的PDF文字重叠**
A: 这通常发生在极密集的布局中，程序会自动调整位置

**Q: 文件大小过大**
A: 使用 `--quality medium` 或 `--quality low` 选项

### 错误日志

程序运行时会生成详细的日志信息，帮助诊断问题。

## 系统要求

- **操作系统**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **内存**: 建议512MB以上可用内存
- **磁盘空间**: 50MB可用空间

## 技术支持

如有问题或建议，请联系开发团队。

---

© 2024 PCB Generator. 保留所有权利。
"""
    return manual_content


def create_release_package():
    """创建发布包"""
    print("创建发布包...")
    
    # 确保dist目录存在
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("✗ dist目录不存在，请先运行 build_standalone.py")
        return False
    
    # 创建发布目录
    release_dir = Path('release')
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # 复制可执行文件
    system = platform.system().lower()
    if system == 'windows':
        exe_name = 'pcb-generator.exe'
    else:
        exe_name = 'pcb-generator'
    
    exe_src = dist_dir / exe_name
    exe_dst = release_dir / exe_name
    
    if not exe_src.exists():
        print(f"✗ 可执行文件不存在: {exe_src}")
        return False
    
    shutil.copy2(exe_src, exe_dst)
    print(f"✓ 复制可执行文件: {exe_name}")
    
    # 创建示例文件
    sample_csv = release_dir / 'sample.csv'
    with open(sample_csv, 'w', encoding='utf-8') as f:
        f.write(create_sample_csv())
    print("✓ 创建示例CSV文件")
    
    # 创建用户手册
    manual_file = release_dir / 'USER_MANUAL.md'
    with open(manual_file, 'w', encoding='utf-8') as f:
        f.write(create_user_manual())
    print("✓ 创建用户手册")
    
    # 复制README
    if Path('README.md').exists():
        shutil.copy2('README.md', release_dir / 'README.md')
        print("✓ 复制README文件")
    
    # 创建快速开始脚本
    if system != 'windows':
        # Unix shell script
        quick_start = release_dir / 'quick_start.sh'
        with open(quick_start, 'w', encoding='utf-8') as f:
            f.write(f"""#!/bin/bash
# PCB Generator 快速开始脚本

echo "PCB Generator 快速开始"
echo "===================="

# 检查示例文件
if [ ! -f "sample.csv" ]; then
    echo "错误: 找不到 sample.csv 文件"
    exit 1
fi

# 创建输出目录
mkdir -p example_output

# 运行示例
echo "正在使用示例文件生成PDF..."
./{exe_name} sample.csv -o example_output --refdes-only

if [ $? -eq 0 ]; then
    echo "✓ 示例PDF生成成功！"
    echo "查看生成的文件: example_output/sample/"
    echo ""
    echo "使用说明:"
    echo "  查看帮助: ./{exe_name} --help"
    echo "  用户手册: cat USER_MANUAL.md"
else
    echo "✗ 示例生成失败"
fi
""")
        quick_start.chmod(0o755)
        print("✓ 创建快速开始脚本 (Unix)")
    else:
        # Windows batch script
        quick_start = release_dir / 'quick_start.bat'
        with open(quick_start, 'w', encoding='utf-8') as f:
            f.write(f"""@echo off
REM PCB Generator 快速开始脚本

echo PCB Generator 快速开始
echo ====================

REM 检查示例文件
if not exist "sample.csv" (
    echo 错误: 找不到 sample.csv 文件
    pause
    exit /b 1
)

REM 创建输出目录
if not exist "example_output" mkdir example_output

REM 运行示例
echo 正在使用示例文件生成PDF...
{exe_name} sample.csv -o example_output --refdes-only

if %errorlevel% equ 0 (
    echo ✓ 示例PDF生成成功！
    echo 查看生成的文件: example_output\\sample\\
    echo.
    echo 使用说明:
    echo   查看帮助: {exe_name} --help
    echo   用户手册: type USER_MANUAL.md
) else (
    echo ✗ 示例生成失败
)

pause
""")
        print("✓ 创建快速开始脚本 (Windows)")
    
    return True


def create_archive():
    """创建压缩包"""
    release_dir = Path('release')
    if not release_dir.exists():
        print("✗ release目录不存在")
        return False
    
    system = platform.system().lower()
    version = "v1.0.0"
    
    if system == 'windows':
        archive_name = f"pcb-generator-{version}-windows.zip"
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in release_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(release_dir)
                    zf.write(file_path, arcname)
    else:
        if system == 'darwin':
            archive_name = f"pcb-generator-{version}-macos.tar.gz"
        else:
            archive_name = f"pcb-generator-{version}-linux.tar.gz"
        
        with tarfile.open(archive_name, 'w:gz') as tf:
            tf.add(release_dir, arcname='pcb-generator')
    
    archive_path = Path(archive_name)
    if archive_path.exists():
        size = archive_path.stat().st_size / (1024 * 1024)  # MB
        print(f"✓ 创建压缩包: {archive_name} ({size:.1f} MB)")
        return True
    
    return False


def main():
    """主函数"""
    print("PCB Generator - 发布包创建器")
    print("=" * 40)
    
    # 创建发布包
    if not create_release_package():
        print("✗ 发布包创建失败")
        return False
    
    # 创建压缩包
    if not create_archive():
        print("✗ 压缩包创建失败")
        return False
    
    print("\n" + "=" * 40)
    print("✓ 发布包创建完成！")
    
    # 显示文件列表
    print("\n发布文件:")
    release_dir = Path('release')
    for file_path in release_dir.rglob('*'):
        if file_path.is_file():
            size = file_path.stat().st_size / 1024  # KB
            print(f"  {file_path.relative_to(release_dir)} ({size:.1f} KB)")
    
    # 显示压缩包
    for archive in Path('.').glob('pcb-generator-*.tar.gz'):
        size = archive.stat().st_size / (1024 * 1024)  # MB
        print(f"\n压缩包: {archive} ({size:.1f} MB)")
    
    for archive in Path('.').glob('pcb-generator-*.zip'):
        size = archive.stat().st_size / (1024 * 1024)  # MB
        print(f"\n压缩包: {archive} ({size:.1f} MB)")
    
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        print("\n✗ 创建失败")
        sys.exit(1)
    else:
        print("\n✓ 创建成功")
        sys.exit(0)
