#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV文件解析模块
用于解析PCB元器件位置数据CSV文件
"""

import csv
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import re


@dataclass
class Component:
    """元器件数据类"""
    num: int
    refdes: str  # 编号
    package: str  # 封装
    x: float  # X坐标
    y: float  # Y坐标
    layer: str  # 层面 (Top/Bottom)
    orientation: float  # 角度
    value: str  # 值
    
    def __post_init__(self):
        """数据后处理"""
        # 标准化层面名称
        if self.layer.lower() in ['top', 'top layer', '正面']:
            self.layer = 'Top'
        elif self.layer.lower() in ['bottom', 'bottom layer', '反面']:
            self.layer = 'Bottom'
        
        # 确保角度在0-360度范围内
        self.orientation = self.orientation % 360


class CSVParser:
    """CSV文件解析器"""
    
    def __init__(self):
        self.components: List[Component] = []
        self.top_components: List[Component] = []
        self.bottom_components: List[Component] = []
    
    def parse_file(self, file_path: str) -> Dict[str, List[Component]]:
        """
        解析CSV文件
        
        Args:
            file_path: CSV文件路径
            
        Returns:
            包含top和bottom元器件列表的字典
            
        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 文件格式错误
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        self.components.clear()
        self.top_components.clear()
        self.bottom_components.clear()
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                # 尝试UTF-8编码
                content = file.read()
        except UnicodeDecodeError:
            try:
                # 如果UTF-8失败，尝试GBK编码
                with open(file_path, 'r', encoding='gbk', errors='ignore') as file:
                    content = file.read()
            except UnicodeDecodeError:
                # 最后尝试latin-1编码
                with open(file_path, 'r', encoding='latin-1', errors='ignore') as file:
                    content = file.read()
        
        # 解析CSV内容
        lines = content.strip().split('\n')
        if len(lines) < 2:
            raise ValueError("CSV文件格式错误：文件内容不足")
        
        # 解析标题行
        header = lines[0].strip()
        if not self._validate_header(header):
            raise ValueError("CSV文件格式错误：标题行格式不正确")
        
        # 解析数据行
        for line_num, line in enumerate(lines[1:], start=2):
            line = line.strip()
            if not line or line.count(',') < 7:  # 跳过空行或格式不正确的行
                continue
            
            try:
                component = self._parse_component_line(line, line_num)
                if component:
                    self.components.append(component)
                    
                    # 按层面分类
                    if component.layer == 'Top':
                        self.top_components.append(component)
                    elif component.layer == 'Bottom':
                        self.bottom_components.append(component)
            except Exception as e:
                print(f"警告：第{line_num}行数据解析失败: {e}")
                continue
        
        if not self.components:
            raise ValueError("CSV文件中没有找到有效的元器件数据")
        
        return {
            'top': self.top_components,
            'bottom': self.bottom_components,
            'all': self.components
        }
    
    def _validate_header(self, header: str) -> bool:
        """验证CSV标题行格式"""
        expected_columns = ['num', 'refdes', 'partdecal', 'x', 'y', 'layer', 'orient', 'value']
        header_lower = header.lower().replace('.', '').replace(' ', '')
        
        # 检查是否包含必要的列
        for col in expected_columns:
            if col not in header_lower:
                return False
        
        return True
    
    def _parse_component_line(self, line: str, line_num: int) -> Optional[Component]:
        """解析单行元器件数据"""
        # 使用CSV模块解析，处理可能包含逗号的字段
        reader = csv.reader([line])
        fields = next(reader)
        
        if len(fields) < 8:
            raise ValueError(f"字段数量不足，期望8个字段，实际{len(fields)}个")
        
        try:
            # 解析各字段
            num = self._parse_int(fields[0], "序号")
            refdes = fields[1].strip()
            package = fields[2].strip()
            x = self._parse_float(fields[3], "X坐标")
            y = self._parse_float(fields[4], "Y坐标")
            layer = fields[5].strip()
            orientation = self._parse_float(fields[6], "角度", default=0.0)
            value = fields[7].strip()
            
            # 验证必要字段
            if not refdes:
                raise ValueError("编号不能为空")
            
            if not layer:
                raise ValueError("层面不能为空")
            
            # 创建元器件对象
            component = Component(
                num=num,
                refdes=refdes,
                package=package,
                x=x,
                y=y,
                layer=layer,
                orientation=orientation,
                value=value
            )
            
            return component
            
        except Exception as e:
            raise ValueError(f"数据解析错误: {e}")
    
    def _parse_int(self, value: str, field_name: str) -> int:
        """解析整数字段"""
        try:
            return int(float(value.strip()))
        except (ValueError, TypeError):
            raise ValueError(f"{field_name}格式错误: {value}")
    
    def _parse_float(self, value: str, field_name: str, default: Optional[float] = None) -> float:
        """解析浮点数字段"""
        try:
            return float(value.strip())
        except (ValueError, TypeError):
            if default is not None:
                return default
            raise ValueError(f"{field_name}格式错误: {value}")
    
    def get_bounds(self, components: List[Component]) -> Tuple[float, float, float, float]:
        """
        获取元器件的边界坐标
        
        Args:
            components: 元器件列表
            
        Returns:
            (min_x, min_y, max_x, max_y)
        """
        if not components:
            return (0, 0, 0, 0)
        
        x_coords = [comp.x for comp in components]
        y_coords = [comp.y for comp in components]
        
        return (
            min(x_coords),
            min(y_coords),
            max(x_coords),
            max(y_coords)
        )
    
    def filter_by_layer(self, layer: str) -> List[Component]:
        """按层面筛选元器件"""
        return [comp for comp in self.components if comp.layer.lower() == layer.lower()]
    
    def filter_by_package(self, package_pattern: str) -> List[Component]:
        """按封装筛选元器件（支持正则表达式）"""
        pattern = re.compile(package_pattern, re.IGNORECASE)
        return [comp for comp in self.components if pattern.search(comp.package)]
    
    def get_statistics(self) -> Dict[str, int]:
        """获取统计信息"""
        return {
            'total': len(self.components),
            'top': len(self.top_components),
            'bottom': len(self.bottom_components),
            'packages': len(set(comp.package for comp in self.components)),
            'unique_values': len(set(comp.value for comp in self.components if comp.value))
        }


def test_parser():
    """测试解析器"""
    parser = CSVParser()
    
    # 测试数据
    test_csv = """Num,RefDes,PartDecal,X,Y,Layer,Orient.,value
1,CN2,SD-V2,22.798,-0.898,Top,0,SD
2,CN3,DP-8-18000,-9,37.5,Top,270,DP_SMD
3,C1,C0603,78.389,19.541,Bottom,180,10uF"""
    
    # 写入临时文件
    with open('test.csv', 'w', encoding='utf-8') as f:
        f.write(test_csv)
    
    try:
        components = parser.parse_file('test.csv')
        print(f"解析成功：{parser.get_statistics()}")
        print(f"Top层元器件：{len(components['top'])}")
        print(f"Bottom层元器件：{len(components['bottom'])}")
        
        # 清理临时文件
        os.remove('test.csv')
        
    except Exception as e:
        print(f"测试失败：{e}")


if __name__ == "__main__":
    test_parser()
