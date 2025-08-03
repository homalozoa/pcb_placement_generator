# 字体大小配置指南

## 概述

PCB Generator 提供了灵活的字体大小配置选项，让你可以根据PCB布局密度和使用需求调整文字大小。

## 🎯 快速调整字体大小

### 方法1: 使用字体配置工具 (推荐)

```bash
# 交互式配置
python font_config.py

# 查看当前设置
python font_config.py --current

# 查看所有预设
python font_config.py --list

# 快速应用预设
python font_config.py --set "中等字体 (推荐)"
```

### 方法2: 直接修改配置文件

编辑 `config.py` 文件中的字体设置：

```python
# 文字配置
base_font_size: int = 8   # 基础字体大小
min_font_size: int = 5    # 最小字体大小  
max_font_size: int = 12   # 最大字体大小
```

## 📏 字体大小预设

### 极小字体 (密集布局)
- **基础**: 4 pt, **最小**: 2 pt, **最大**: 6 pt
- **适用**: 元器件非常密集的PCB，字体很小但仍可读
- **使用**: `python font_config.py --set "极小字体 (密集布局)"`

### 小字体 (默认)
- **基础**: 6 pt, **最小**: 3 pt, **最大**: 8 pt
- **适用**: 原始默认设置，适用于大多数PCB布局
- **使用**: `python font_config.py --set "小字体 (默认)"`

### 平衡字体 (推荐) ⭐
- **基础**: 7 pt, **最小**: 4 pt, **最大**: 10 pt
- **适用**: 在可读性和重叠避免之间的最佳平衡，适用于大多数PCB
- **使用**: `python font_config.py --set "平衡字体 (推荐)"`

### 中等字体
- **基础**: 8 pt, **最小**: 5 pt, **最大**: 12 pt
- **适用**: 增大的字体，更易读，适用于中等密度布局
- **使用**: `python font_config.py --set "中等字体"`

### 大字体 (稀疏布局)
- **基础**: 10 pt, **最小**: 7 pt, **最大**: 15 pt
- **适用**: 大字体，适用于元器件稀疏的PCB
- **使用**: `python font_config.py --set "大字体 (稀疏布局)"`

### 超大字体 (演示用)
- **基础**: 12 pt, **最小**: 9 pt, **最大**: 18 pt
- **适用**: 超大字体，适用于演示或打印大尺寸图纸
- **使用**: `python font_config.py --set "超大字体 (演示用)"`

## 🔧 高级配置

### 修改PDF生成器中的字体限制

编辑 `pdf_generator.py` 中的 `_calculate_optimal_text_size` 函数：

```python
# 确保最小可读性
optimal_size = max(3.0, optimal_size)  # 最小字体大小

# 限制最大值避免过大  
optimal_size = min(8.0, optimal_size)  # 最大字体大小
```

### 调整0201封装的放大倍数

```python
# 基于0201封装的字体大小（放大倍数）
package_based_size = max_text_height_mm * 2.83 * 3  # 3倍放大
```

## 📊 字体大小对比

| 预设 | 基础字体 | 最小字体 | 最大字体 | 适用场景 |
|------|----------|----------|----------|----------|
| 极小字体 | 4 pt | 2 pt | 6 pt | 超密集PCB |
| 小字体 | 6 pt | 3 pt | 8 pt | 一般PCB |
| **平衡字体** | **7 pt** | **4 pt** | **10 pt** | **推荐使用** |
| 中等字体 | 8 pt | 5 pt | 12 pt | 中等密度PCB |
| 大字体 | 10 pt | 7 pt | 15 pt | 稀疏PCB |
| 超大字体 | 12 pt | 9 pt | 18 pt | 演示/大图 |

## 🎨 字体效果示例

### 测试不同字体大小

```bash
# 应用中等字体
python font_config.py --set "中等字体 (推荐)"

# 生成测试PDF
python cli_main.py test_position.csv -o test_medium_font --refdes-only

# 应用大字体
python font_config.py --set "大字体 (稀疏布局)"

# 生成对比PDF
python cli_main.py test_position.csv -o test_large_font --refdes-only
```

## 💡 选择建议

### 根据PCB密度选择

- **超密集布局** (>1000个0201元器件): 极小字体
- **密集布局** (500-1000个元器件): 小字体
- **中等布局** (100-500个元器件): 平衡字体 ⭐
- **稀疏布局** (<100个元器件): 大字体
- **演示展示**: 超大字体

### 根据用途选择

- **生产制造**: 平衡字体 (清晰易读，重叠少)
- **工程审查**: 大字体 (便于检查)
- **客户演示**: 超大字体 (视觉效果好)
- **存档备份**: 小字体 (节省空间)

## 🔄 实时调整工作流

1. **查看当前设置**
   ```bash
   python font_config.py --current
   ```

2. **选择合适预设**
   ```bash
   python font_config.py --list
   python font_config.py --set "平衡字体 (推荐)"
   ```

3. **生成测试PDF**
   ```bash
   python cli_main.py your_file.csv -o test_output --refdes-only
   ```

4. **检查效果并调整**
   - 如果字体太小：选择更大的预设
   - 如果字体太大：选择更小的预设
   - 如果有重叠：选择更小的预设

5. **生成最终PDF**
   ```bash
   python cli_main.py your_file.csv -o final_output
   ```

## ⚠️ 注意事项

### 字体大小限制
- 最小字体不应小于2pt (打印时可能不清晰)
- 最大字体不应大于20pt (可能造成严重重叠)
- 确保 最小 ≤ 基础 ≤ 最大

### 重叠问题
- 字体越大，重叠风险越高
- 密集布局建议使用较小字体
- 程序会自动调整位置避免重叠

### 打印考虑
- 打印时字体会比屏幕显示小
- 建议比屏幕预览大1-2个级别
- 高DPI打印机可以使用更小字体

## 🛠️ 故障排除

### 字体配置不生效
```bash
# 检查配置文件是否正确修改
python font_config.py --current

# 重新生成PDF
python cli_main.py your_file.csv -o new_output
```

### 字体仍然太小/太大
```bash
# 尝试自定义设置
python font_config.py
# 选择 "自定义设置" 选项
```

### 重叠问题严重
```bash
# 使用更小的字体预设
python font_config.py --set "小字体 (默认)"
```

---

💡 **推荐**: 对于大多数用户，建议使用 "平衡字体 (推荐)" 预设，它在可读性和重叠避免之间提供了最佳平衡。
