#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF生成模块
使用matplotlib生成PCB位号图PDF文件
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import math

from csv_parser import Component
from config import Config


class PDFGenerator:
    """PDF生成器"""
    
    def __init__(self, config: Config):
        self.config = config
        
        # 设置英文字体
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Liberation Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 图形参数
        self.figure_size = (11.69, 8.27)  # A4横向尺寸（英寸）
        self.dpi = 300
        self.margin = 0.5  # 边距（英寸）
    
    def generate_refdes_pdf(self, components: Dict[str, List[Component]], output_dir: Path):
        """生成编号图PDF"""
        self._generate_pdf(components, output_dir, 'RefDes', 'refdes', 'Reference Designator Layout')

    def generate_package_pdf(self, components: Dict[str, List[Component]], output_dir: Path):
        """生成封装图PDF"""
        self._generate_pdf(components, output_dir, 'Package', 'package', 'Package Layout')

    def generate_value_pdf(self, components: Dict[str, List[Component]], output_dir: Path):
        """生成值图PDF"""
        self._generate_pdf(components, output_dir, 'Value', 'value', 'Component Value Layout')
    
    def _generate_pdf(self, components: Dict[str, List[Component]], output_dir: Path, 
                     file_prefix: str, field_name: str, title_suffix: str):
        """生成PDF文件的通用方法"""
        layers = ['top', 'bottom']
        layer_names = {'top': 'Top', 'bottom': 'Bottom'}

        for layer in layers:
            if not components[layer]:
                continue

            filename = f"{file_prefix}_{layer_names[layer]}.pdf"
            filepath = output_dir / filename

            with PdfPages(filepath) as pdf:
                fig = self._create_layout_figure(
                    components[layer],
                    field_name,
                    f"PCB {title_suffix} - {layer_names[layer]} Layer"
                )
                pdf.savefig(fig, dpi=self.dpi, bbox_inches='tight')
                plt.close(fig)
    
    def _create_layout_figure(self, components: List[Component], field_name: str, title: str):
        """创建位号图"""
        if not components:
            # 创建空图
            fig, ax = plt.subplots(figsize=self.figure_size)
            ax.text(0.5, 0.5, 'No components on this layer', ha='center', va='center',
                   transform=ax.transAxes, fontsize=16)
            ax.set_title(title, fontsize=14, fontweight='bold')
            return fig

        # 获取坐标边界
        x_coords = [comp.x for comp in components]
        y_coords = [comp.y for comp in components]

        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)

        # 添加边距
        x_range = max_x - min_x
        y_range = max_y - min_y

        if x_range == 0:
            x_range = 10
        if y_range == 0:
            y_range = 10

        margin_x = x_range * self.config.margin_ratio
        margin_y = y_range * self.config.margin_ratio

        plot_min_x = min_x - margin_x
        plot_max_x = max_x + margin_x
        plot_min_y = min_y - margin_y
        plot_max_y = max_y + margin_y

        # 创建图形
        fig, ax = plt.subplots(figsize=self.figure_size)

        # 设置坐标轴
        ax.set_xlim(plot_min_x, plot_max_x)
        ax.set_ylim(plot_min_y, plot_max_y)
        ax.set_aspect('equal')
        ax.grid(True, alpha=self.config.grid_alpha, linestyle='-', linewidth=0.5)
        ax.set_xlabel('X (mm)', fontsize=10)
        ax.set_ylabel('Y (mm)', fontsize=10)
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

        # 添加次要网格
        ax.grid(True, which='minor', alpha=self.config.grid_alpha * 0.5, linestyle=':', linewidth=0.3)
        ax.minorticks_on()

        # 计算统一的文字大小
        text_size = self._calculate_optimal_text_size(components, plot_max_x - plot_min_x, plot_max_y - plot_min_y)

        # 初始化文本位置跟踪
        self.text_positions = []
        self.component_bounds = []

        # 第一遍：收集所有元器件边界
        for comp in components:
            package_size = self._get_package_size(comp.package)
            bounds = {
                'x': comp.x,
                'y': comp.y,
                'width': package_size[0],
                'height': package_size[1],
                'component': comp
            }
            self.component_bounds.append(bounds)

        # 第二遍：绘制元器件和文本
        for comp in components:
            self._draw_component_with_smart_layout(ax, comp, field_name, text_size)

        # 添加图例和信息
        self._add_legend_and_info(ax, components, field_name)

        plt.tight_layout()
        return fig
    
    def _draw_component(self, ax, component: Component, field_name: str, text_size: float):
        """绘制单个元器件"""
        x, y = component.x, component.y

        # 获取要显示的文本
        if field_name == 'refdes':
            text = component.refdes
        elif field_name == 'package':
            text = component.package
        elif field_name == 'value':
            text = component.value if component.value else 'N/A'
        else:
            text = component.refdes

        # 绘制元器件轮廓（简化为矩形）
        package_size = self._get_package_size(component.package)
        width, height = package_size

        # 根据角度旋转
        angle_rad = math.radians(component.orientation)

        # 创建矩形
        rect = patches.Rectangle(
            (x - width/2, y - height/2),
            width, height,
            angle=component.orientation,
            linewidth=0.5,
            edgecolor=self.config.component_edge_color,
            facecolor=self.config.component_face_color,
            alpha=self.config.component_alpha
        )
        ax.add_patch(rect)

        # 智能文本定位，避免重叠
        text_x, text_y = self._get_optimal_text_position(x, y, text, text_size, width, height)

        # 绘制文本
        ax.text(text_x, text_y, text,
               fontsize=text_size,
               ha='center', va='center',
               rotation=self._get_text_rotation(component.orientation),
               bbox=dict(boxstyle='round,pad=0.2',
                        facecolor=self.config.text_background_color,
                        alpha=self.config.text_background_alpha,
                        edgecolor='none'),
               clip_on=True,
               zorder=10)  # 确保文本在最上层

        # 绘制中心点
        ax.plot(x, y, 'o',
               color=self.config.center_point_color,
               markersize=self.config.center_point_size,
               alpha=0.7)

    def _get_optimal_text_position(self, x: float, y: float, text: str,
                                 text_size: float, comp_width: float, comp_height: float) -> Tuple[float, float]:
        """获取最佳文本位置，避免重叠"""
        # 简单策略：如果文本较长，尝试放在元器件外部
        text_length = len(text)

        # 估算文本尺寸
        char_width = text_size * 0.6  # 近似字符宽度
        text_width = text_length * char_width

        # 如果文本宽度超过元器件宽度的80%，尝试外部定位
        if text_width > comp_width * 0.8:
            # 尝试放在右侧
            offset_x = comp_width / 2 + text_width / 2 + 1
            return (x + offset_x, y)

        # 默认居中
        return (x, y)

    def _draw_component_advanced(self, ax, component: Component, field_name: str, text_size: float):
        """高级元器件绘制，包含文本重叠避免"""
        x, y = component.x, component.y

        # 获取要显示的文本
        if field_name == 'refdes':
            text = component.refdes
        elif field_name == 'package':
            text = component.package
        elif field_name == 'value':
            text = component.value if component.value else 'N/A'
        else:
            text = component.refdes

        # 绘制元器件轮廓
        package_size = self._get_package_size(component.package)
        width, height = package_size

        # 创建矩形
        rect = patches.Rectangle(
            (x - width/2, y - height/2),
            width, height,
            angle=component.orientation,
            linewidth=0.5,
            edgecolor=self.config.component_edge_color,
            facecolor=self.config.component_face_color,
            alpha=self.config.component_alpha
        )
        ax.add_patch(rect)

        # 智能文本定位，避免重叠
        text_x, text_y = self._find_non_overlapping_position(x, y, text, text_size, width, height)

        # 绘制文本
        ax.text(text_x, text_y, text,
               fontsize=text_size,
               ha='center', va='center',
               rotation=self._get_text_rotation(component.orientation),
               bbox=dict(boxstyle='round,pad=0.2',
                        facecolor=self.config.text_background_color,
                        alpha=self.config.text_background_alpha,
                        edgecolor='none'),
               clip_on=True,
               zorder=10)

        # 记录文本位置
        self._record_text_position(text_x, text_y, text, text_size)

        # 绘制中心点
        ax.plot(x, y, 'o',
               color=self.config.center_point_color,
               markersize=self.config.center_point_size,
               alpha=0.7)

    def _find_non_overlapping_position(self, x: float, y: float, text: str,
                                     text_size: float, comp_width: float, comp_height: float) -> Tuple[float, float]:
        """寻找不重叠的文本位置"""
        # 估算文本尺寸
        char_width = text_size * 0.6
        char_height = text_size
        text_width = len(text) * char_width
        text_height = char_height

        # 候选位置（相对于元器件中心）
        candidates = [
            (0, 0),  # 中心
            (comp_width/2 + text_width/2 + 1, 0),  # 右侧
            (-comp_width/2 - text_width/2 - 1, 0),  # 左侧
            (0, comp_height/2 + text_height/2 + 1),  # 上方
            (0, -comp_height/2 - text_height/2 - 1),  # 下方
            (comp_width/2 + text_width/2 + 1, comp_height/2 + text_height/2 + 1),  # 右上
            (-comp_width/2 - text_width/2 - 1, comp_height/2 + text_height/2 + 1),  # 左上
            (comp_width/2 + text_width/2 + 1, -comp_height/2 - text_height/2 - 1),  # 右下
            (-comp_width/2 - text_width/2 - 1, -comp_height/2 - text_height/2 - 1),  # 左下
        ]

        # 检查每个候选位置
        for dx, dy in candidates:
            candidate_x = x + dx
            candidate_y = y + dy

            if not self._is_text_overlapping(candidate_x, candidate_y, text_width, text_height):
                return (candidate_x, candidate_y)

        # 如果所有位置都重叠，返回默认位置
        return (x, y)

    def _is_text_overlapping(self, x: float, y: float, width: float, height: float) -> bool:
        """检查文本是否与已有文本重叠"""
        for pos_x, pos_y, pos_width, pos_height in self.text_positions:
            # 检查矩形重叠
            if (abs(x - pos_x) < (width + pos_width) / 2 and
                abs(y - pos_y) < (height + pos_height) / 2):
                return True
        return False

    def _record_text_position(self, x: float, y: float, text: str, text_size: float):
        """记录文本位置"""
        char_width = text_size * 0.6
        char_height = text_size
        text_width = len(text) * char_width
        text_height = char_height

        self.text_positions.append((x, y, text_width, text_height))

    def _draw_component_with_smart_layout(self, ax, component: Component, field_name: str, text_size: float):
        """使用智能布局绘制元器件，只显示文字标记"""
        x, y = component.x, component.y

        # 获取要显示的文本
        if field_name == 'refdes':
            text = component.refdes
        elif field_name == 'package':
            text = component.package
        elif field_name == 'value':
            text = component.value if component.value else 'N/A'
        else:
            text = component.refdes

        # 不绘制元器件轮廓和中心点，只绘制文字
        # 文字位置就是元器件的坐标位置，确保准确对应

        # 绘制文本，中心对准坐标点
        ax.text(x, y, text,
               fontsize=text_size,
               ha='center', va='center',
               rotation=self._get_text_rotation(component.orientation),
               bbox=dict(boxstyle='round,pad=0.05',  # 减小padding
                        facecolor='white',
                        alpha=0.9,  # 增加不透明度确保可读性
                        edgecolor='black',
                        linewidth=0.2),
               clip_on=True,
               zorder=10,
               weight='bold')  # 加粗字体提高可读性

        # 记录文本位置用于重叠检测
        self._record_text_position(x, y, text, text_size)

    def _find_optimal_text_position(self, x: float, y: float, text: str,
                                   text_size: float, comp_width: float, comp_height: float) -> Tuple[float, float]:
        """寻找最优的文本位置，优先使用原始坐标"""
        # 估算文本尺寸（更精确的估算）
        char_width = text_size * 0.7  # 字符宽度
        char_height = text_size * 1.0  # 字符高度
        text_width = len(text) * char_width
        text_height = char_height

        # 首先检查原始位置是否可用
        if not self._is_position_occupied(x, y, text_width, text_height):
            return (x, y)  # 优先使用原始坐标位置

        # 如果原始位置被占用，寻找最近的可用位置
        # 使用更小的偏移量，尽量靠近原始坐标
        min_offset = max(text_width, text_height) / 2 + 0.5

        candidates = [
            # 小偏移量的位置（优先）
            (min_offset, 0),      # 右侧
            (-min_offset, 0),     # 左侧
            (0, min_offset),      # 上方
            (0, -min_offset),     # 下方

            # 对角线小偏移
            (min_offset * 0.7, min_offset * 0.7),    # 右上
            (-min_offset * 0.7, min_offset * 0.7),   # 左上
            (min_offset * 0.7, -min_offset * 0.7),   # 右下
            (-min_offset * 0.7, -min_offset * 0.7),  # 左下

            # 稍大的偏移量
            (min_offset * 1.5, 0),      # 更远右侧
            (-min_offset * 1.5, 0),     # 更远左侧
            (0, min_offset * 1.5),      # 更远上方
            (0, -min_offset * 1.5),     # 更远下方
        ]

        # 检查每个候选位置
        for dx, dy in candidates:
            candidate_x = x + dx
            candidate_y = y + dy

            if not self._is_position_occupied(candidate_x, candidate_y, text_width, text_height):
                return (candidate_x, candidate_y)

        # 如果所有位置都被占用，使用螺旋搜索
        return self._spiral_search_position(x, y, text_width, text_height, min_offset, min_offset)

    def _is_position_occupied(self, x: float, y: float, width: float, height: float) -> bool:
        """检查位置是否被占用（只检查与其他文本的重叠）"""
        # 只检查与已有文本的重叠，不再检查元器件轮廓
        for pos_x, pos_y, pos_width, pos_height in self.text_positions:
            if self._rectangles_overlap(x, y, width, height, pos_x, pos_y, pos_width, pos_height):
                return True

        return False

    def _rectangles_overlap(self, x1: float, y1: float, w1: float, h1: float,
                           x2: float, y2: float, w2: float, h2: float) -> bool:
        """检查两个矩形是否重叠（基于0201封装尺寸的缓冲区）"""
        # 基于0201封装尺寸的缓冲区
        # 0201封装宽度0.6mm，使用其50%作为缓冲区
        min_buffer = 0.3  # 最小0.3mm缓冲区
        dynamic_buffer = min(w1, h1, w2, h2) * 0.5  # 动态缓冲区
        buffer = max(min_buffer, dynamic_buffer)

        return (abs(x1 - x2) < (w1 + w2) / 2 + buffer and
                abs(y1 - y2) < (h1 + h2) / 2 + buffer)

    def _spiral_search_position(self, center_x: float, center_y: float,
                               text_width: float, text_height: float,
                               comp_width: float, comp_height: float) -> Tuple[float, float]:
        """螺旋搜索可用位置"""
        # 增加搜索范围和精度
        max_radius = max(comp_width, comp_height) * 5
        step = min(text_width, text_height) / 3

        # 更密集的角度搜索
        for radius in np.arange(step, max_radius, step):
            for angle in np.arange(0, 2 * np.pi, np.pi / 12):  # 更多角度
                test_x = center_x + radius * np.cos(angle)
                test_y = center_y + radius * np.sin(angle)

                if not self._is_position_occupied(test_x, test_y, text_width, text_height):
                    return (test_x, test_y)

        # 如果螺旋搜索失败，尝试网格搜索
        return self._grid_search_position(center_x, center_y, text_width, text_height, max_radius)

    def _grid_search_position(self, center_x: float, center_y: float,
                             text_width: float, text_height: float, max_radius: float) -> Tuple[float, float]:
        """网格搜索备用方案"""
        step = min(text_width, text_height) / 2

        for offset_x in np.arange(-max_radius, max_radius, step):
            for offset_y in np.arange(-max_radius, max_radius, step):
                test_x = center_x + offset_x
                test_y = center_y + offset_y

                if not self._is_position_occupied(test_x, test_y, text_width, text_height):
                    return (test_x, test_y)

        # 最后的备用方案：返回远离中心的位置
        return (center_x + max_radius, center_y + max_radius)
    
    def _get_package_size(self, package: str) -> Tuple[float, float]:
        """根据封装名称估算尺寸（毫米）"""
        package_lower = package.lower()
        
        # 常见封装尺寸映射
        size_map = {
            'c0201': (0.6, 0.3),
            'c0402': (1.0, 0.5),
            'c0603': (1.6, 0.8),
            'c0805': (2.0, 1.25),
            'c1206': (3.2, 1.6),
            'r0201': (0.6, 0.3),
            'r0402': (1.0, 0.5),
            'r0603': (1.6, 0.8),
            'r0805': (2.0, 1.25),
            'r1206': (3.2, 1.6),
            'sot23': (2.9, 1.3),
            'sot23-5': (2.9, 1.6),
            'sot23-6': (2.9, 1.6),
            'sop8': (5.0, 4.0),
            'qfn': (5.0, 5.0),
            'qfn16': (3.0, 3.0),
            'qfn48': (7.0, 7.0),
            'qfn64': (9.0, 9.0),
            'usb': (12.0, 8.0),
            'hdmi': (15.0, 12.0),
        }
        
        # 查找匹配的封装
        for key, size in size_map.items():
            if key in package_lower:
                return size
        
        # 默认尺寸
        return (2.0, 2.0)
    
    def _get_text_rotation(self, orientation: float) -> float:
        """计算文本旋转角度，确保文本可读"""
        # 将角度标准化到0-360度
        angle = orientation % 360
        
        # 如果角度在90-270度之间，旋转180度使文本可读
        if 90 <= angle <= 270:
            return angle - 180
        else:
            return angle
    
    def _calculate_optimal_text_size(self, components: List[Component], width: float, height: float) -> float:
        """基于0201封装尺寸计算最优文字大小"""
        if not components:
            return 2.0  # 默认很小的字体

        # 0201封装尺寸：0.6mm x 0.3mm
        # 文字应该能够放入这个尺寸内
        package_0201_width = 0.6  # mm
        package_0201_height = 0.3  # mm

        # 文字高度不应超过0201封装高度的80%
        max_text_height_mm = package_0201_height * 0.8  # 0.24mm

        # 转换为点数 (1mm ≈ 2.83 points)
        max_font_size_pt = max_text_height_mm * 2.83  # ≈ 0.68pt

        # 但这太小了，我们需要在可读性和避免重叠之间平衡
        # 使用0201封装作为基准，但允许适当放大

        # 计算最小元器件间距
        min_distance = self._calculate_min_component_distance(components)

        # 基于最小间距的字体大小限制
        # 文字高度不应超过最小间距的25%（更严格的限制）
        distance_based_size = (min_distance * 0.25) * 2.83

        # 基于0201封装的字体大小（放大2倍使其可读）
        package_based_size = max_text_height_mm * 2.83 * 2  # ≈ 1.36pt

        # 取两者中的较小值，确保既不重叠又基于0201尺寸
        optimal_size = min(distance_based_size, package_based_size)

        # 确保最小可读性
        optimal_size = max(1.5, optimal_size)  # 最小1.5pt

        # 限制最大值避免过大
        optimal_size = min(4.0, optimal_size)  # 最大4pt

        return optimal_size

    def _calculate_min_component_distance(self, components: List[Component]) -> float:
        """计算元器件之间的最小距离"""
        if len(components) < 2:
            return 5.0  # 默认间距

        min_distance = float('inf')

        for i in range(len(components)):
            for j in range(i + 1, len(components)):
                dist = ((components[i].x - components[j].x)**2 +
                       (components[i].y - components[j].y)**2)**0.5
                if dist > 0:
                    min_distance = min(min_distance, dist)

        # 如果没有找到有效距离，返回默认值
        if min_distance == float('inf'):
            return 5.0

        # 确保最小距离不会太小
        return max(1.0, min_distance)
    
    def _add_legend_and_info(self, ax, components: List[Component], field_name: str):
        """添加图例和信息"""
        # 统计信息
        total_count = len(components)

        # 根据字段类型统计
        if field_name == 'package':
            unique_items = set(comp.package for comp in components)
            info_text = f"Total: {total_count}\nPackage Types: {len(unique_items)}"
        elif field_name == 'value':
            unique_items = set(comp.value for comp in components if comp.value)
            info_text = f"Total: {total_count}\nUnique Values: {len(unique_items)}"
        else:  # refdes
            info_text = f"Total: {total_count}"

        # 添加信息框
        ax.text(0.02, 0.98, info_text,
               transform=ax.transAxes,
               fontsize=9,
               verticalalignment='top',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))


def test_generator():
    """测试PDF生成器"""
    from csv_parser import CSVParser, Component
    from config import Config
    
    # 创建测试数据
    test_components = {
        'top': [
            Component(1, 'C1', 'C0603', 10.0, 10.0, 'Top', 0, '10uF'),
            Component(2, 'R1', 'R0402', 20.0, 15.0, 'Top', 90, '1K'),
            Component(3, 'U1', 'QFN48', 30.0, 20.0, 'Top', 0, 'MCU'),
        ],
        'bottom': [
            Component(4, 'C2', 'C0805', 15.0, 25.0, 'Bottom', 180, '22uF'),
        ],
        'all': []
    }
    
    config = Config()
    generator = PDFGenerator(config)
    
    output_dir = Path('test_output')
    output_dir.mkdir(exist_ok=True)
    
    try:
        generator.generate_refdes_pdf(test_components, output_dir)
        print("测试PDF生成成功！")
    except Exception as e:
        print(f"测试失败：{e}")


if __name__ == "__main__":
    test_generator()
