#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PCB位号图生成器演示脚本
展示程序的各种功能和优化效果
"""

import os
import sys
from pathlib import Path
import time


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_step(step, description):
    """打印步骤"""
    print(f"\n[步骤 {step}] {description}")
    print("-" * 40)


def run_command(cmd, description=""):
    """运行命令并显示结果"""
    if description:
        print(f"执行: {description}")
    print(f"命令: {cmd}")
    
    result = os.system(cmd)
    if result == 0:
        print("✅ 成功")
    else:
        print("❌ 失败")
    return result == 0


def demo_basic_usage():
    """演示基本用法"""
    print_header("基本用法演示")
    
    print_step(1, "生成所有类型的PDF")
    run_command("python cli_main.py test_position.csv -o demo_output --verbose", 
                "使用测试数据生成完整的PDF文档")
    
    print_step(2, "只生成编号图")
    run_command("python cli_main.py test_position.csv -o demo_output --refdes-only", 
                "只生成Reference Designator图")
    
    print_step(3, "只生成封装图")
    run_command("python cli_main.py test_position.csv -o demo_output --package-only", 
                "只生成Package Layout图")
    
    print_step(4, "只生成值图")
    run_command("python cli_main.py test_position.csv -o demo_output --value-only", 
                "只生成Component Value图")


def demo_layout_optimization():
    """演示布局优化"""
    print_header("布局优化演示")
    
    print_step(1, "密集布局测试")
    run_command("python test_layout.py", 
                "测试密集排列元器件的布局算法")
    
    print_step(2, "检查生成的文件")
    output_dirs = ["demo_output", "layout_test_output", "overlap_test_output"]
    
    for dir_name in output_dirs:
        if os.path.exists(dir_name):
            print(f"\n📁 {dir_name}:")
            for file in Path(dir_name).rglob("*.pdf"):
                size_kb = file.stat().st_size / 1024
                print(f"  📄 {file.name} ({size_kb:.1f} KB)")


def demo_quality_options():
    """演示质量选项"""
    print_header("质量选项演示")
    
    qualities = ["low", "medium", "high"]
    
    for quality in qualities:
        print_step(qualities.index(quality) + 1, f"生成{quality}质量PDF")
        output_dir = f"demo_quality_{quality}"
        run_command(f"python cli_main.py test_position.csv -o {output_dir} --quality {quality} --refdes-only", 
                    f"生成{quality}质量的PDF文件")
        
        # 检查文件大小
        pdf_files = list(Path(output_dir).rglob("*.pdf"))
        if pdf_files:
            for pdf_file in pdf_files:
                size_kb = pdf_file.stat().st_size / 1024
                print(f"  📄 {pdf_file.name}: {size_kb:.1f} KB")


def demo_help_and_options():
    """演示帮助和选项"""
    print_header("帮助和选项演示")
    
    print_step(1, "显示帮助信息")
    run_command("python cli_main.py --help", "查看所有可用选项")
    
    print_step(2, "显示版本信息")
    run_command("python cli_main.py --version", "查看程序版本")


def show_file_summary():
    """显示生成文件总结"""
    print_header("生成文件总结")
    
    all_pdfs = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".pdf"):
                file_path = Path(root) / file
                all_pdfs.append(file_path)
    
    if all_pdfs:
        print(f"总共生成了 {len(all_pdfs)} 个PDF文件:")
        
        total_size = 0
        for pdf_file in sorted(all_pdfs):
            size_kb = pdf_file.stat().st_size / 1024
            total_size += size_kb
            print(f"  📄 {pdf_file}: {size_kb:.1f} KB")
        
        print(f"\n总大小: {total_size:.1f} KB ({total_size/1024:.1f} MB)")
    else:
        print("没有找到PDF文件")


def demo_features():
    """演示主要特性"""
    print_header("主要特性演示")
    
    features = [
        "✅ 智能文字重叠避免算法",
        "✅ 统一字体大小确保美观",
        "✅ 英文字体完美支持",
        "✅ A3尺寸提供充足空间",
        "✅ 高分辨率300DPI输出",
        "✅ 自适应元器件密度",
        "✅ 多种质量选项",
        "✅ 命令行和图形界面",
        "✅ 跨平台支持",
        "✅ 独立可执行文件"
    ]
    
    for feature in features:
        print(f"  {feature}")
        time.sleep(0.1)  # 动画效果


def cleanup_demo_files():
    """清理演示文件"""
    print_header("清理演示文件")
    
    demo_dirs = [
        "demo_output", "demo_quality_low", "demo_quality_medium", "demo_quality_high",
        "layout_test_output", "overlap_test_output", "final_test", "optimized_output",
        "cli_test_output", "test_output", "layout_test"
    ]
    
    cleaned = 0
    for dir_name in demo_dirs:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)
            print(f"🗑️  删除目录: {dir_name}")
            cleaned += 1
    
    if cleaned > 0:
        print(f"\n清理完成，删除了 {cleaned} 个目录")
    else:
        print("没有需要清理的文件")


def main():
    """主演示函数"""
    print_header("PCB元器件位号图生成器 - 完整演示")
    print("这个演示将展示程序的所有功能和优化效果")
    
    # 检查必要文件
    if not os.path.exists("test_position.csv"):
        print("❌ 错误: 找不到测试文件 test_position.csv")
        return
    
    # 创建必要的目录
    demo_dirs = ["demo_output", "demo_quality_low", "demo_quality_medium", "demo_quality_high"]
    for dir_name in demo_dirs:
        os.makedirs(dir_name, exist_ok=True)
    
    try:
        # 演示主要特性
        demo_features()
        
        # 演示基本用法
        demo_basic_usage()
        
        # 演示布局优化
        demo_layout_optimization()
        
        # 演示质量选项
        demo_quality_options()
        
        # 演示帮助和选项
        demo_help_and_options()
        
        # 显示文件总结
        show_file_summary()
        
        print_header("演示完成")
        print("🎉 所有功能演示完成！")
        print("\n主要改进:")
        print("  • 完全解决了文字重叠问题")
        print("  • 统一字体大小确保美观")
        print("  • 移除中文避免字体问题")
        print("  • 智能布局算法优化")
        print("  • A3尺寸提供更多空间")
        
        print("\n使用建议:")
        print("  • 使用命令行版本获得最佳兼容性")
        print("  • 选择合适的质量设置平衡文件大小")
        print("  • 对于密集PCB使用--refdes-only等单独生成")
        
        # 询问是否清理
        response = input("\n是否清理演示生成的文件? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            cleanup_demo_files()
        else:
            print("保留演示文件，您可以查看生成的PDF效果")
            
    except KeyboardInterrupt:
        print("\n\n演示被用户中断")
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
