# 使用示例

## 快速开始

### 1. 准备CSV文件

创建一个包含PCB元器件信息的CSV文件，例如 `my_pcb.csv`：

```csv
Num,RefDes,PartDecal,X,Y,Layer,Orient.,value
1,C1,C0603,10.0,10.0,Top,0,10uF
2,C2,C0805,20.0,15.0,Bottom,90,22uF
3,R1,R0402,30.0,20.0,Top,180,1K
4,U1,QFN48,40.0,25.0,Top,270,MCU
5,J1,USB-C,50.0,30.0,Top,0,USB
```

### 2. 使用命令行版本

```bash
# 生成所有类型的PDF
python cli_main.py my_pcb.csv

# 只生成编号图
python cli_main.py my_pcb.csv --refdes-only

# 指定输出目录并显示详细信息
python cli_main.py my_pcb.csv -o output --verbose
```

### 3. 使用图形界面版本

```bash
python main.py
```

然后在界面中：
1. 点击"浏览..."选择CSV文件
2. 选择输出目录
3. 勾选要生成的图纸类型
4. 点击"生成PDF"

## 高级用法

### 批量处理多个文件

```bash
# 处理目录中的所有CSV文件
for file in *.csv; do
    python cli_main.py "$file" -o batch_output --verbose
done
```

### 不同质量设置

```bash
# 高质量（默认）
python cli_main.py my_pcb.csv --quality high

# 中等质量（文件更小）
python cli_main.py my_pcb.csv --quality medium

# 低质量（最小文件）
python cli_main.py my_pcb.csv --quality low
```

### 选择性生成

```bash
# 只生成编号图和封装图
python cli_main.py my_pcb.csv -r -p

# 只生成值图
python cli_main.py my_pcb.csv --value-only
```

## 实际项目示例

### 示例1：简单的LED电路

CSV内容：
```csv
Num,RefDes,PartDecal,X,Y,Layer,Orient.,value
1,LED1,LED-0805,10.0,10.0,Top,0,Red
2,R1,R0603,20.0,10.0,Top,0,330R
3,C1,C0603,30.0,10.0,Top,0,100nF
4,U1,SOT23,40.0,10.0,Top,0,LM317
```

生成命令：
```bash
python cli_main.py led_circuit.csv -o led_output --verbose
```

### 示例2：复杂的多层PCB

对于包含数百个元器件的复杂PCB：

```bash
# 分别生成不同类型的图，避免信息过载
python cli_main.py complex_pcb.csv --refdes-only -o output/refdes
python cli_main.py complex_pcb.csv --package-only -o output/package  
python cli_main.py complex_pcb.csv --value-only -o output/value
```

### 示例3：生产用位号图

```bash
# 生成高质量的生产用图纸
python cli_main.py production_pcb.csv \
    --quality high \
    --refdes-only \
    -o production_docs \
    --verbose
```

## 输出文件说明

生成的PDF文件会保存在指定目录下的CSV同名子目录中：

```
output/
└── my_pcb/
    ├── RefDes_Top.pdf      # 正面编号图
    ├── RefDes_Bottom.pdf   # 反面编号图
    ├── Package_Top.pdf     # 正面封装图
    ├── Package_Bottom.pdf  # 反面封装图
    ├── Value_Top.pdf       # 正面值图
    └── Value_Bottom.pdf    # 反面值图
```

## 常见使用场景

### 1. PCB装配指导

生成编号图用于装配时查找元器件位置：
```bash
python cli_main.py assembly.csv --refdes-only -o assembly_guide
```

### 2. 元器件采购清单

生成值图用于核对元器件规格：
```bash
python cli_main.py bom.csv --value-only -o procurement
```

### 3. 封装验证

生成封装图用于验证PCB设计：
```bash
python cli_main.py layout.csv --package-only -o verification
```

### 4. 完整文档包

生成所有类型的图纸用于完整的技术文档：
```bash
python cli_main.py final_design.csv -o complete_docs --quality high --verbose
```

## 故障排除示例

### 处理编码问题

如果CSV文件包含中文或特殊字符：

1. 确保文件保存为UTF-8编码
2. 或者使用GBK编码（程序会自动检测）

### 处理大文件

对于包含大量元器件的文件：

```bash
# 使用低质量设置减少内存使用
python cli_main.py large_pcb.csv --quality low

# 分批处理
python cli_main.py large_pcb.csv --refdes-only
python cli_main.py large_pcb.csv --package-only
python cli_main.py large_pcb.csv --value-only
```

### 自定义配置

如需修改默认设置，编辑 `config.py` 文件：

```python
# 修改图形尺寸
figure_size = (16.53, 11.69)  # A3尺寸

# 修改字体大小
base_font_size = 10

# 添加自定义封装尺寸
package_sizes['my_custom_package'] = (5.0, 3.0)
```

## 自动化脚本示例

### Windows批处理脚本

创建 `generate_pdfs.bat`：
```batch
@echo off
for %%f in (*.csv) do (
    python cli_main.py "%%f" -o output --verbose
)
pause
```

### Linux/macOS脚本

创建 `generate_pdfs.sh`：
```bash
#!/bin/bash
for file in *.csv; do
    if [ -f "$file" ]; then
        echo "Processing $file..."
        python cli_main.py "$file" -o output --verbose
    fi
done
echo "All files processed!"
```

使用方法：
```bash
chmod +x generate_pdfs.sh
./generate_pdfs.sh
```
