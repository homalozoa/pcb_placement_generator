# PCB Generator - 独立二进制文件分发指南

## 概述

PCB Generator 现在提供完全独立的二进制可执行文件，无需安装Python环境即可使用。

## 🚀 快速开始

### 1. 下载和解压

```bash
# 下载对应平台的压缩包
# macOS: pcb-generator-v1.0.0-macos.tar.gz
# Linux: pcb-generator-v1.0.0-linux.tar.gz  
# Windows: pcb-generator-v1.0.0-windows.zip

# 解压文件
tar -xzf pcb-generator-v1.0.0-macos.tar.gz  # macOS/Linux
# 或者在Windows上解压zip文件

cd pcb-generator
```

### 2. 运行快速测试

```bash
# 运行快速开始脚本（macOS/Linux）
./quick_start.sh

# 或者手动运行示例
./pcb-generator sample.csv -o output --refdes-only
```

### 3. 使用你的CSV文件

```bash
# 生成所有类型的PDF
./pcb-generator your_file.csv

# 只生成编号图
./pcb-generator your_file.csv --refdes-only

# 指定输出目录
./pcb-generator your_file.csv -o output_directory
```

## 📦 分发包内容

```
pcb-generator/
├── pcb-generator          # 主可执行文件
├── sample.csv             # 示例CSV文件
├── quick_start.sh         # 快速开始脚本（Unix系统）
├── USER_MANUAL.md         # 详细用户手册
└── README.md              # 项目说明
```

## 🔧 构建独立二进制文件

如果你需要自己构建二进制文件：

### 方法1：使用简化构建脚本

```bash
# 安装依赖
python -m pip install -r requirements.txt
python -m pip install pyinstaller

# 构建独立二进制文件
python build_standalone.py

# 创建完整发布包
python create_release.py
```

### Windows平台特殊说明

在Windows上构建时：
```cmd
# 使用命令提示符或PowerShell
python -m pip install -r requirements.txt
python -m pip install pyinstaller

# 构建
python build_standalone.py

# 创建发布包
python create_release.py
```

生成的文件：
- `dist/pcb-generator.exe` - Windows可执行文件
- `pcb-generator-v1.0.0-windows.zip` - Windows发布包
- 包含 `quick_start.bat` - Windows批处理脚本

### 方法2：使用完整构建脚本

```bash
# 使用原有的构建脚本
python build.py
```

### 方法3：手动使用PyInstaller

```bash
# 基本命令
pyinstaller --onefile --console --name pcb-generator cli_main.py

# 完整命令（包含优化）
pyinstaller \
  --onefile \
  --console \
  --name pcb-generator \
  --hidden-import matplotlib.backends.backend_pdf \
  --hidden-import numpy.core._methods \
  --exclude-module tkinter \
  --exclude-module PyQt5 \
  cli_main.py
```

## 📋 系统要求

### 运行要求（二进制文件）
- **macOS**: 10.14+ (Mojave)
- **Linux**: Ubuntu 18.04+ 或等效系统
- **Windows**: Windows 10+
- **内存**: 512MB 可用内存
- **磁盘**: 50MB 可用空间

### 构建要求（开发环境）
- **Python**: 3.8+
- **依赖包**: matplotlib, numpy, reportlab, Pillow
- **构建工具**: PyInstaller

## 🎯 优化特性

### 文件大小优化
- 排除不必要的模块（tkinter, PyQt, scipy等）
- 使用UPX压缩（如果可用）
- 单文件打包模式

### 性能优化
- 预编译Python字节码
- 优化导入路径
- 最小化启动时间

### 兼容性优化
- 静态链接所有依赖
- 包含必要的系统库
- 跨平台字体支持

## 📊 文件大小对比

| 平台 | 文件大小 | 压缩后 |
|------|----------|--------|
| macOS | ~26MB | ~26MB |
| Linux | ~25MB | ~25MB |
| Windows | ~28MB | ~28MB |

## 🔍 故障排除

### 常见问题

**Q: 程序启动慢**
A: 首次运行时matplotlib需要构建字体缓存，这是正常现象

**Q: 权限错误（Unix系统）**
A: 运行 `chmod +x pcb-generator` 添加执行权限

**Q: 找不到文件**
A: 确保CSV文件路径正确，使用绝对路径或相对路径

**Q: 内存不足**
A: 对于大型PCB文件，建议至少1GB可用内存

### 调试模式

```bash
# 启用详细输出
./pcb-generator your_file.csv --verbose

# 查看帮助信息
./pcb-generator --help
```

## 📈 性能建议

### 大文件处理
- 对于超过1000个元器件的PCB，建议分批处理
- 使用SSD存储提高I/O性能
- 确保足够的可用内存

### 批量处理
```bash
# 批量处理多个文件
for file in *.csv; do
    ./pcb-generator "$file" -o "output_$(basename "$file" .csv)"
done
```

## 🚀 分发建议

### 给最终用户
1. 提供对应平台的压缩包
2. 包含示例文件和快速开始指南
3. 提供简单的使用说明

### 企业部署
1. 可以集成到现有的PCB设计流程中
2. 支持命令行自动化
3. 可以通过脚本批量处理

## 📝 更新日志

### v1.0.0
- ✅ 首个独立二进制版本
- ✅ 支持所有主要平台
- ✅ 优化的文字布局算法
- ✅ 基于0201封装的字体优化
- ✅ 完整的用户文档

---

© 2024 PCB Generator. 保留所有权利。
