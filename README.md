# PCB元器件位号图生成器

一个用于从CSV文件生成PCB元器件位号图PDF文件的工具，支持正面和反面分层显示，可生成编号图、封装图和值图。

## 功能特点

- 📊 **多种图纸类型**：支持生成编号图、封装图、值图
- 🔄 **正反面分层**：自动分离Top层和Bottom层元器件
- 🎨 **智能布局**：自动避免文字重叠，优化显示效果
- 📱 **双界面支持**：提供图形界面和命令行界面
- 🖥️ **跨平台**：支持Windows、macOS、Linux
- 📦 **独立部署**：可打包为独立可执行文件

## 安装方法

### 方法一：从源码安装

1. 克隆或下载项目文件
2. 安装依赖：
```bash
python setup.py
```

### 方法二：使用pip安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 图形界面版本

```bash
python main.py
```

启动后：
1. 选择CSV文件
2. 选择输出目录
3. 选择要生成的图纸类型
4. 点击"生成PDF"

### 命令行版本

```bash
# 生成所有类型的图
python cli_main.py input.csv

# 指定输出目录
python cli_main.py input.csv -o output_dir

# 只生成编号图
python cli_main.py input.csv --refdes-only

# 只生成封装图
python cli_main.py input.csv --package-only

# 只生成值图
python cli_main.py input.csv --value-only

# 生成编号图和封装图
python cli_main.py input.csv -r -p

# 显示详细信息
python cli_main.py input.csv --verbose

# 查看帮助
python cli_main.py --help
```

## CSV文件格式

CSV文件应包含以下列（第一行为标题行）：

| 列名 | 说明 | 示例 |
|------|------|------|
| Num | 序号 | 1, 2, 3... |
| RefDes | 元器件编号 | C1, R1, U1... |
| PartDecal | 封装类型 | C0603, R0402, QFN48... |
| X | X坐标（毫米） | 22.798, -9.0... |
| Y | Y坐标（毫米） | -0.898, 37.5... |
| Layer | 层面 | Top, Bottom |
| Orient. | 角度 | 0, 90, 180, 270... |
| value | 元器件值 | 10uF, 1K, MCU... |

### 示例CSV内容

```csv
Num,RefDes,PartDecal,X,Y,Layer,Orient.,value
1,CN2,SD-V2,22.798,-0.898,Top,0,SD
2,CN3,DP-8-18000,-9,37.5,Top,270,DP_SMD
3,C1,C0603,78.389,19.541,Bottom,180,10uF
4,R1,R0402,88.875,19.116,Top,270,10K
5,U1,QFN64,82.001,24.568,Top,270,GL3510
```

## 输出文件

程序会在输出目录下创建与CSV文件同名的子目录，并生成以下PDF文件：

- `RefDes_Top.pdf` - 正面编号图
- `RefDes_Bottom.pdf` - 反面编号图
- `Package_Top.pdf` - 正面封装图
- `Package_Bottom.pdf` - 反面封装图
- `Value_Top.pdf` - 正面值图
- `Value_Bottom.pdf` - 反面值图

## 打包部署

### 生成可执行文件

```bash
python build.py
```

生成的可执行文件位于`dist`目录中，可以直接分发给用户使用，无需安装Python环境。

### 系统要求

- Python 3.8+
- matplotlib >= 3.5.0
- numpy >= 1.21.0
- reportlab >= 3.6.0
- Pillow >= 8.3.0

## 配置选项

程序支持多种配置选项，可在`config.py`中修改：

- 图形尺寸和DPI
- 字体大小和颜色
- 元器件封装尺寸映射
- PDF质量设置

## 故障排除

### 常见问题

1. **中文字体显示问题**
   - 程序会自动尝试使用系统中文字体
   - 如果显示异常，可以在配置中指定字体

2. **tkinter模块错误**
   - 使用命令行版本：`python cli_main.py`
   - 或安装支持tkinter的Python版本

3. **CSV编码问题**
   - 确保CSV文件使用UTF-8或GBK编码
   - 程序会自动尝试多种编码

4. **内存不足**
   - 处理大文件时可能需要更多内存
   - 可以分批处理或使用低质量设置

### 错误日志

程序运行时会生成`pcb_generator.log`日志文件，包含详细的错误信息。

## 开发说明

### 项目结构

```
placement_number_gen/
├── main.py              # 图形界面主程序
├── cli_main.py          # 命令行主程序
├── csv_parser.py        # CSV解析模块
├── pdf_generator.py     # PDF生成模块
├── config.py            # 配置模块
├── error_handler.py     # 错误处理模块
├── setup.py             # 安装脚本
├── build.py             # 打包脚本
├── requirements.txt     # 依赖列表
└── README.md            # 说明文档
```

### 扩展开发

1. **添加新的封装类型**：在`config.py`中的`package_sizes`字典中添加
2. **修改图形样式**：在`config.py`中调整颜色和样式设置
3. **添加新的输出格式**：在`pdf_generator.py`中扩展生成方法

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 更新日志

### v1.0.0 (2024-08-02)
- 初始版本发布
- 支持CSV解析和PDF生成
- 提供图形界面和命令行界面
- 支持跨平台部署

## 技术支持

如有问题或建议，请：
1. 检查本文档的故障排除部分
2. 查看生成的日志文件
3. 确认CSV文件格式是否正确
4. 验证输出目录权限

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！
