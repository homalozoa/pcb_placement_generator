#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体大小配置工具
允许用户轻松调整PDF生成器的字体大小设置
"""

import sys
from pathlib import Path
from config import Config


def show_current_settings():
    """显示当前字体设置"""
    config = Config()
    print("当前字体设置:")
    print("=" * 40)
    print(f"基础字体大小: {config.base_font_size} pt")
    print(f"最小字体大小: {config.min_font_size} pt")
    print(f"最大字体大小: {config.max_font_size} pt")
    print()


def get_font_size_recommendations():
    """获取字体大小建议"""
    recommendations = {
        "极小字体 (密集布局)": {
            "base_font_size": 4,
            "min_font_size": 2,
            "max_font_size": 6,
            "description": "适用于元器件非常密集的PCB，字体很小但仍可读"
        },
        "小字体 (默认)": {
            "base_font_size": 6,
            "min_font_size": 3,
            "max_font_size": 8,
            "description": "原始默认设置，适用于大多数PCB布局"
        },
        "中等字体 (推荐)": {
            "base_font_size": 8,
            "min_font_size": 5,
            "max_font_size": 12,
            "description": "增大的字体，更易读，适用于中等密度布局"
        },
        "大字体 (稀疏布局)": {
            "base_font_size": 10,
            "min_font_size": 7,
            "max_font_size": 15,
            "description": "大字体，适用于元器件稀疏的PCB"
        },
        "超大字体 (演示用)": {
            "base_font_size": 12,
            "min_font_size": 9,
            "max_font_size": 18,
            "description": "超大字体，适用于演示或打印大尺寸图纸"
        }
    }
    return recommendations


def apply_font_settings(base_size, min_size, max_size):
    """应用字体设置到配置文件"""
    config_file = Path("config.py")
    
    if not config_file.exists():
        print("错误: 找不到config.py文件")
        return False
    
    # 读取配置文件
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换字体设置
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if 'base_font_size:' in line and 'int' in line:
            new_lines.append(f"    base_font_size: int = {base_size}  # 基础字体大小")
        elif 'min_font_size:' in line and 'int' in line:
            new_lines.append(f"    min_font_size: int = {min_size}   # 最小字体大小")
        elif 'max_font_size:' in line and 'int' in line:
            new_lines.append(f"    max_font_size: int = {max_size}  # 最大字体大小")
        else:
            new_lines.append(line)
    
    # 写回文件
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"✓ 字体设置已更新:")
    print(f"  基础字体: {base_size} pt")
    print(f"  最小字体: {min_size} pt")
    print(f"  最大字体: {max_size} pt")
    return True


def interactive_config():
    """交互式配置字体大小"""
    print("PCB Generator 字体大小配置工具")
    print("=" * 50)
    
    show_current_settings()
    
    recommendations = get_font_size_recommendations()
    
    print("预设字体大小选项:")
    print("-" * 30)
    
    options = list(recommendations.keys())
    for i, option in enumerate(options, 1):
        settings = recommendations[option]
        print(f"{i}. {option}")
        print(f"   基础: {settings['base_font_size']} pt, "
              f"最小: {settings['min_font_size']} pt, "
              f"最大: {settings['max_font_size']} pt")
        print(f"   说明: {settings['description']}")
        print()
    
    print(f"{len(options) + 1}. 自定义设置")
    print(f"{len(options) + 2}. 退出")
    print()
    
    try:
        choice = int(input("请选择 (1-{}): ".format(len(options) + 2)))
        
        if 1 <= choice <= len(options):
            # 应用预设
            option_name = options[choice - 1]
            settings = recommendations[option_name]
            
            print(f"\n选择了: {option_name}")
            confirm = input("确认应用此设置? (y/N): ").lower()
            
            if confirm in ['y', 'yes']:
                apply_font_settings(
                    settings['base_font_size'],
                    settings['min_font_size'],
                    settings['max_font_size']
                )
                print("\n设置已应用！重新运行PDF生成器以查看效果。")
            else:
                print("取消设置。")
                
        elif choice == len(options) + 1:
            # 自定义设置
            print("\n自定义字体设置:")
            base = int(input("基础字体大小 (pt): "))
            min_size = int(input("最小字体大小 (pt): "))
            max_size = int(input("最大字体大小 (pt): "))
            
            if min_size <= base <= max_size:
                apply_font_settings(base, min_size, max_size)
                print("\n自定义设置已应用！")
            else:
                print("错误: 字体大小必须满足 最小 <= 基础 <= 最大")
                
        elif choice == len(options) + 2:
            print("退出配置工具。")
            
        else:
            print("无效选择。")
            
    except ValueError:
        print("请输入有效的数字。")
    except KeyboardInterrupt:
        print("\n\n配置已取消。")


def quick_set(preset_name):
    """快速设置预设字体大小"""
    recommendations = get_font_size_recommendations()
    
    if preset_name not in recommendations:
        print(f"错误: 未知的预设名称 '{preset_name}'")
        print("可用预设:", list(recommendations.keys()))
        return False
    
    settings = recommendations[preset_name]
    apply_font_settings(
        settings['base_font_size'],
        settings['min_font_size'],
        settings['max_font_size']
    )
    return True


def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 命令行模式
        if sys.argv[1] == "--list":
            recommendations = get_font_size_recommendations()
            print("可用的字体预设:")
            for name, settings in recommendations.items():
                print(f"  {name}: {settings['description']}")
        elif sys.argv[1] == "--set" and len(sys.argv) > 2:
            preset_name = sys.argv[2]
            if quick_set(preset_name):
                print(f"已应用预设: {preset_name}")
        elif sys.argv[1] == "--current":
            show_current_settings()
        else:
            print("用法:")
            print("  python font_config.py                # 交互式配置")
            print("  python font_config.py --list         # 列出所有预设")
            print("  python font_config.py --set <预设名>  # 快速应用预设")
            print("  python font_config.py --current      # 显示当前设置")
    else:
        # 交互式模式
        interactive_config()


if __name__ == "__main__":
    main()
