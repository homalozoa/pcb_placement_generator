# Windows 平台构建指南

## 概述

本文档详细说明如何在Windows平台上构建PCB Generator的独立可执行文件。

## 系统要求

### 开发环境
- **操作系统**: Windows 10 或更高版本
- **Python**: 3.8 或更高版本
- **内存**: 至少 2GB 可用内存
- **磁盘空间**: 至少 1GB 可用空间

### 推荐工具
- **命令行**: PowerShell 或 Command Prompt
- **编辑器**: VS Code, PyCharm, 或任何文本编辑器

## 安装步骤

### 1. 安装Python

从 [python.org](https://www.python.org/downloads/windows/) 下载并安装Python：

```cmd
# 验证Python安装
python --version
python -m pip --version
```

### 2. 克隆或下载项目

```cmd
# 如果使用Git
git clone <repository-url>
cd placement_number_gen

# 或者下载ZIP文件并解压
```

### 3. 安装依赖

```cmd
# 安装项目依赖
python -m pip install -r requirements.txt

# 安装PyInstaller
python -m pip install pyinstaller
```

## 构建独立可执行文件

### 方法1: 使用自动化脚本

```cmd
# 构建独立二进制文件
python build_standalone.py

# 创建完整发布包
python create_release.py
```

### 方法2: 手动构建

```cmd
# 基本构建命令
pyinstaller --onefile --console --name pcb-generator cli_main.py

# 完整构建命令（推荐）
pyinstaller ^
  --onefile ^
  --console ^
  --name pcb-generator ^
  --hidden-import matplotlib.backends.backend_pdf ^
  --hidden-import matplotlib.backends.backend_agg ^
  --hidden-import numpy.core._methods ^
  --hidden-import csv_parser ^
  --hidden-import pdf_generator ^
  --hidden-import config ^
  --hidden-import error_handler ^
  --exclude-module tkinter ^
  --exclude-module PyQt5 ^
  --exclude-module PyQt6 ^
  cli_main.py
```

## 生成的文件

构建成功后，你将得到：

```
dist/
├── pcb-generator.exe          # 主可执行文件

release/                       # 完整发布包
├── pcb-generator.exe          # 可执行文件
├── sample.csv                 # 示例CSV文件
├── quick_start.bat            # Windows快速开始脚本
├── USER_MANUAL.md             # 用户手册
└── README.md                  # 项目说明

pcb-generator-v1.0.0-windows.zip  # 压缩发布包
```

## 使用方法

### 基本使用

```cmd
# 生成所有类型的PDF
pcb-generator.exe input.csv

# 指定输出目录
pcb-generator.exe input.csv -o output_folder

# 只生成编号图
pcb-generator.exe input.csv --refdes-only

# 查看帮助
pcb-generator.exe --help
```

### 快速测试

```cmd
# 运行快速开始脚本
quick_start.bat

# 或手动测试
mkdir test_output
pcb-generator.exe sample.csv -o test_output --refdes-only
```

## 故障排除

### 常见问题

**Q: Python命令不被识别**
```cmd
# 解决方案：将Python添加到PATH环境变量
# 或使用完整路径
C:\Python39\python.exe -m pip install -r requirements.txt
```

**Q: pip安装失败**
```cmd
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像源
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

**Q: PyInstaller构建失败**
```cmd
# 清理缓存
rmdir /s build
rmdir /s dist
del *.spec

# 重新构建
python build_standalone.py
```

**Q: 可执行文件启动慢**
A: 首次运行时matplotlib需要构建字体缓存，这是正常现象

**Q: 杀毒软件误报**
A: 将生成的exe文件添加到杀毒软件白名单

### 调试模式

```cmd
# 启用详细输出
pcb-generator.exe input.csv --verbose

# 检查依赖
python -c "import matplotlib, numpy, reportlab; print('All dependencies OK')"
```

## 性能优化

### 减小文件大小

```cmd
# 使用UPX压缩（需要单独安装UPX）
pyinstaller --onefile --upx-dir=C:\upx cli_main.py
```

### 提高启动速度

```cmd
# 预编译Python文件
python -m compileall .

# 使用--noupx选项（如果UPX导致问题）
pyinstaller --onefile --noupx cli_main.py
```

## 分发建议

### 给最终用户
1. 提供完整的ZIP包 `pcb-generator-v1.0.0-windows.zip`
2. 包含使用说明和示例文件
3. 提供快速开始脚本 `quick_start.bat`

### 企业部署
1. 可以通过组策略分发
2. 支持静默安装和配置
3. 可以集成到现有的PCB设计流程

## 自动化构建

### 批处理脚本示例

创建 `build_windows.bat`:

```batch
@echo off
echo Building PCB Generator for Windows...

REM 清理旧文件
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist release rmdir /s /q release

REM 安装依赖
python -m pip install -r requirements.txt
python -m pip install pyinstaller

REM 构建
python build_standalone.py

REM 创建发布包
python create_release.py

echo Build completed!
pause
```

### CI/CD集成

可以集成到GitHub Actions或其他CI/CD系统：

```yaml
# .github/workflows/build-windows.yml
name: Build Windows
on: [push, pull_request]
jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - run: python -m pip install -r requirements.txt
    - run: python -m pip install pyinstaller
    - run: python build_standalone.py
    - run: python create_release.py
```

## 技术支持

如有问题，请检查：
1. Python版本是否正确
2. 所有依赖是否已安装
3. 防火墙/杀毒软件设置
4. 系统环境变量配置

---

© 2024 PCB Generator. 保留所有权利。
