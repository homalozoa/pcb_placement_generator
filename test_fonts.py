#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体测试工具
检查系统中可用的字体，特别是Arial Narrow
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path


def list_available_fonts():
    """列出系统中所有可用的字体"""
    fonts = fm.findSystemFonts()
    font_names = []
    
    for font_path in fonts:
        try:
            font_prop = fm.FontProperties(fname=font_path)
            font_name = font_prop.get_name()
            font_names.append(font_name)
        except:
            continue
    
    return sorted(set(font_names))


def check_arial_fonts():
    """检查Arial相关字体的可用性"""
    all_fonts = list_available_fonts()
    arial_fonts = [font for font in all_fonts if 'arial' in font.lower()]
    
    print("Arial相关字体:")
    print("=" * 40)
    
    if not arial_fonts:
        print("❌ 未找到Arial字体")
        return False
    
    arial_narrow_found = False
    for font in arial_fonts:
        if 'narrow' in font.lower():
            print(f"✅ {font} (窄字体)")
            arial_narrow_found = True
        else:
            print(f"📝 {font}")
    
    return arial_narrow_found


def test_font_rendering():
    """测试字体渲染效果"""
    test_fonts = [
        'Arial Narrow',
        'Arial',
        'DejaVu Sans',
        'Liberation Sans'
    ]
    
    test_text = "R123 C456 U789"
    
    fig, axes = plt.subplots(len(test_fonts), 1, figsize=(10, 8))
    if len(test_fonts) == 1:
        axes = [axes]
    
    for i, font_name in enumerate(test_fonts):
        ax = axes[i]
        
        try:
            # 测试不同字号
            font_sizes = [6, 7, 8, 10]
            x_positions = [1, 3, 5, 7]
            
            for j, (size, x_pos) in enumerate(zip(font_sizes, x_positions)):
                ax.text(x_pos, 0.5, test_text, 
                       fontsize=size, 
                       fontfamily=font_name,
                       ha='center', va='center',
                       bbox=dict(boxstyle='round,pad=0.1', 
                                facecolor='lightblue', 
                                alpha=0.7))
                ax.text(x_pos, 0.2, f"{size}pt", 
                       fontsize=8, ha='center', va='center')
            
            ax.set_xlim(0, 8)
            ax.set_ylim(0, 1)
            ax.set_title(f"字体: {font_name}", fontsize=12, fontweight='bold')
            ax.set_xticks([])
            ax.set_yticks([])
            
        except Exception as e:
            ax.text(0.5, 0.5, f"字体 '{font_name}' 不可用\n错误: {str(e)}", 
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=10, color='red')
            ax.set_title(f"字体: {font_name} (不可用)", fontsize=12, color='red')
    
    plt.tight_layout()
    
    # 保存测试图片
    output_file = "font_test_comparison.pdf"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n字体测试图片已保存: {output_file}")
    
    plt.close()


def get_font_recommendations():
    """获取字体推荐"""
    all_fonts = list_available_fonts()
    
    # 窄字体候选
    narrow_candidates = [
        'Arial Narrow',
        'Arial Condensed', 
        'Helvetica Narrow',
        'Liberation Sans Narrow',
        'DejaVu Sans Condensed'
    ]
    
    # 检查可用的窄字体
    available_narrow = []
    for font in narrow_candidates:
        if font in all_fonts:
            available_narrow.append(font)
    
    print("\n字体推荐:")
    print("=" * 40)
    
    if available_narrow:
        print("✅ 可用的窄字体:")
        for font in available_narrow:
            print(f"   - {font}")
    else:
        print("❌ 未找到专门的窄字体")
        print("📝 备选方案:")
        backup_fonts = ['Arial', 'Helvetica', 'DejaVu Sans', 'Liberation Sans']
        for font in backup_fonts:
            if font in all_fonts:
                print(f"   - {font}")
    
    return available_narrow


def update_font_config(preferred_fonts):
    """更新字体配置建议"""
    if not preferred_fonts:
        print("\n⚠️  建议保持当前字体配置")
        return
    
    print(f"\n💡 建议的字体配置:")
    print("=" * 40)
    
    font_list = preferred_fonts + ['Arial', 'DejaVu Sans', 'Liberation Sans']
    font_config = "plt.rcParams['font.sans-serif'] = " + str(font_list)
    
    print("在 pdf_generator.py 中使用:")
    print(font_config)
    
    print(f"\n首选字体: {preferred_fonts[0]}")
    print("这将显著减少文字的水平占用空间，减少重叠问题。")


def main():
    """主函数"""
    print("PCB Generator 字体测试工具")
    print("=" * 50)
    
    # 检查Arial字体
    arial_narrow_available = check_arial_fonts()
    
    # 获取字体推荐
    narrow_fonts = get_font_recommendations()
    
    # 测试字体渲染
    print(f"\n正在生成字体对比图...")
    test_font_rendering()
    
    # 更新配置建议
    update_font_config(narrow_fonts)
    
    # 总结
    print(f"\n" + "=" * 50)
    if arial_narrow_available:
        print("✅ Arial Narrow 可用！这将显著改善文字布局。")
    elif narrow_fonts:
        print(f"✅ 找到替代窄字体: {narrow_fonts[0]}")
    else:
        print("⚠️  未找到窄字体，将使用标准字体。")
        print("💡 考虑安装Arial Narrow或其他窄字体以获得更好效果。")
    
    print("\n下一步:")
    print("1. 查看生成的字体对比图")
    print("2. 运行 PDF 生成测试")
    print("3. 如需要，手动调整字体配置")


if __name__ == "__main__":
    main()
