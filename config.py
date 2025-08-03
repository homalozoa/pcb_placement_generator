#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置模块
包含程序的各种配置参数
"""

from dataclasses import dataclass
from typing import Dict, Tuple, List
import os


@dataclass
class Config:
    """程序配置类"""
    
    # 图形配置
    figure_size: Tuple[float, float] = (16.53, 11.69)  # A3横向尺寸（英寸），提供更多空间
    dpi: int = 300
    margin_ratio: float = 0.15  # 增加边距比例，提供更多空间
    
    # 文字配置
    base_font_size: int = 8  # 基础字体大小
    min_font_size: int = 5   # 最小字体大小
    max_font_size: int = 12  # 最大字体大小
    
    # 颜色配置
    component_edge_color: str = 'blue'
    component_face_color: str = 'lightblue'
    component_alpha: float = 0.3
    text_background_color: str = 'white'
    text_background_alpha: float = 0.8
    center_point_color: str = 'red'
    center_point_size: int = 1
    grid_alpha: float = 0.3
    
    # 元器件尺寸映射（毫米）
    package_sizes: Dict[str, Tuple[float, float]] = None
    
    # 支持的文件格式
    supported_csv_extensions: List[str] = None
    
    # 输出配置
    pdf_quality: str = 'high'  # 'low', 'medium', 'high'
    
    def __post_init__(self):
        """初始化后处理"""
        if self.package_sizes is None:
            self.package_sizes = {
                # 电容
                'c0201': (0.6, 0.3),
                'c0402': (1.0, 0.5),
                'c0603': (1.6, 0.8),
                'c0805': (2.0, 1.25),
                'c1206': (3.2, 1.6),
                'c1210': (3.2, 2.5),
                'c1812': (4.5, 3.2),
                'c2220': (5.7, 5.0),
                
                # 电阻
                'r0201': (0.6, 0.3),
                'r0402': (1.0, 0.5),
                'r0603': (1.6, 0.8),
                'r0805': (2.0, 1.25),
                'r1206': (3.2, 1.6),
                'r1210': (3.2, 2.5),
                'r2010': (5.0, 2.5),
                'r2512': (6.4, 3.2),
                
                # 晶体管
                'sot23': (2.9, 1.3),
                'sot23-3': (2.9, 1.3),
                'sot23-5': (2.9, 1.6),
                'sot23-6': (2.9, 1.6),
                'sot89': (4.5, 2.5),
                'sot223': (6.5, 3.5),
                'to-220': (10.0, 4.5),
                'to-252': (6.5, 6.0),
                
                # 集成电路
                'sop8': (5.0, 4.0),
                'sop14': (8.7, 4.0),
                'sop16': (10.0, 4.0),
                'sop20': (12.8, 4.0),
                'sop28': (17.9, 4.0),
                'soic8': (5.0, 4.0),
                'soic14': (8.7, 4.0),
                'soic16': (10.0, 4.0),
                'soic20': (12.8, 4.0),
                'soic28': (17.9, 4.0),
                
                # QFN封装
                'qfn': (5.0, 5.0),
                'qfn16': (3.0, 3.0),
                'qfn20': (4.0, 4.0),
                'qfn24': (4.0, 4.0),
                'qfn32': (5.0, 5.0),
                'qfn48': (7.0, 7.0),
                'qfn64': (9.0, 9.0),
                'qfn76': (10.0, 10.0),
                'qfn128': (14.0, 14.0),
                
                # QFP封装
                'qfp32': (7.0, 7.0),
                'qfp44': (10.0, 10.0),
                'qfp64': (12.0, 12.0),
                'qfp100': (14.0, 14.0),
                'qfp144': (20.0, 20.0),
                
                # BGA封装
                'bga': (15.0, 15.0),
                'bga64': (8.0, 8.0),
                'bga100': (10.0, 10.0),
                'bga144': (13.0, 13.0),
                'bga256': (17.0, 17.0),
                
                # 连接器
                'usb': (12.0, 8.0),
                'usb-a': (14.0, 6.5),
                'usb-b': (12.0, 11.0),
                'usb-c': (9.0, 3.2),
                'usb3.0': (14.0, 8.0),
                'usb3.1': (14.0, 8.0),
                'type-c': (9.0, 3.2),
                'hdmi': (15.0, 12.0),
                'rj45': (16.0, 13.0),
                'sd': (15.0, 11.0),
                'tf': (11.0, 15.0),
                'audio': (6.0, 6.0),
                
                # 晶振
                'x-3225': (3.2, 2.5),
                'x-5032': (5.0, 3.2),
                'x-7050': (7.0, 5.0),
                
                # 电感
                'l-0630': (6.0, 3.0),
                'l-4040': (4.0, 4.0),
                'l-zadh252012': (2.5, 2.0),
                
                # 二极管
                'sod-323': (1.7, 1.25),
                'sod-523': (1.25, 0.85),
                'sod-923': (0.8, 0.6),
                
                # 其他
                'ce-1206': (3.2, 1.6),
                'dfn3x3': (3.0, 3.0),
                'cap-5x8mm': (5.0, 8.0),
            }
        
        if self.supported_csv_extensions is None:
            self.supported_csv_extensions = ['.csv', '.txt']
    
    def get_package_size(self, package: str) -> Tuple[float, float]:
        """
        获取封装尺寸
        
        Args:
            package: 封装名称
            
        Returns:
            (width, height) 尺寸元组（毫米）
        """
        package_lower = package.lower().replace('-', '').replace('_', '')
        
        # 精确匹配
        if package_lower in self.package_sizes:
            return self.package_sizes[package_lower]
        
        # 模糊匹配
        for key, size in self.package_sizes.items():
            if key in package_lower or package_lower.startswith(key):
                return size
        
        # 尝试从名称中提取尺寸信息
        size = self._extract_size_from_name(package)
        if size:
            return size
        
        # 默认尺寸
        return (2.0, 2.0)
    
    def _extract_size_from_name(self, package: str) -> Tuple[float, float]:
        """从封装名称中提取尺寸信息"""
        import re
        
        # 匹配类似 "0603", "1206" 等格式
        match = re.search(r'(\d{2})(\d{2})', package)
        if match:
            width_code = int(match.group(1))
            height_code = int(match.group(2))
            
            # 转换为毫米（假设是英制代码）
            width = width_code * 0.254  # 0.01英寸 = 0.254毫米
            height = height_code * 0.254
            
            return (width, height)
        
        return None
    
    def get_dpi_by_quality(self) -> int:
        """根据质量设置获取DPI"""
        quality_map = {
            'low': 150,
            'medium': 200,
            'high': 300
        }
        return quality_map.get(self.pdf_quality, 300)
    
    def get_font_size_by_density(self, density: float) -> float:
        """根据元器件密度计算字体大小"""
        if density > 0.15:  # 极高密度
            return max(self.min_font_size, self.base_font_size * 0.5)
        elif density > 0.1:  # 高密度
            return max(self.min_font_size, self.base_font_size * 0.7)
        elif density > 0.05:  # 中密度
            return self.base_font_size * 0.85
        else:  # 低密度
            return min(self.max_font_size, self.base_font_size * 1.1)
    
    def validate(self) -> bool:
        """验证配置参数"""
        try:
            assert self.figure_size[0] > 0 and self.figure_size[1] > 0
            assert self.dpi > 0
            assert 0 <= self.margin_ratio <= 1
            assert self.min_font_size <= self.base_font_size <= self.max_font_size
            assert 0 <= self.component_alpha <= 1
            assert 0 <= self.text_background_alpha <= 1
            assert 0 <= self.grid_alpha <= 1
            return True
        except AssertionError:
            return False
    
    def save_to_file(self, filepath: str):
        """保存配置到文件"""
        import json
        
        config_dict = {
            'figure_size': self.figure_size,
            'dpi': self.dpi,
            'margin_ratio': self.margin_ratio,
            'base_font_size': self.base_font_size,
            'min_font_size': self.min_font_size,
            'max_font_size': self.max_font_size,
            'pdf_quality': self.pdf_quality,
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'Config':
        """从文件加载配置"""
        import json
        
        if not os.path.exists(filepath):
            return cls()
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
            
            config = cls()
            for key, value in config_dict.items():
                if hasattr(config, key):
                    setattr(config, key, value)
            
            return config
        except Exception:
            return cls()


# 默认配置实例
default_config = Config()


def test_config():
    """测试配置模块"""
    config = Config()
    
    # 测试封装尺寸获取
    test_packages = ['C0603', 'R0402', 'QFN48', 'USB3.0', 'unknown_package']
    
    for package in test_packages:
        size = config.get_package_size(package)
        print(f"{package}: {size}")
    
    # 测试配置验证
    print(f"配置验证: {config.validate()}")
    
    # 测试密度计算
    densities = [0.01, 0.08, 0.15]
    for density in densities:
        font_size = config.get_font_size_by_density(density)
        print(f"密度 {density}: 字体大小 {font_size}")


if __name__ == "__main__":
    test_config()
