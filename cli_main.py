#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PCB元器件位号图生成器 - 命令行版本
支持从CSV文件生成PCB正反面的位号图PDF文件
"""

import argparse
import os
import sys
from pathlib import Path

# 导入自定义模块
from csv_parser import CSVParser
from pdf_generator import PDFGenerator
from config import Config
from error_handler import (
    get_error_handler, ValidationError, 
    validate_csv_file, validate_output_directory
)


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='PCB元器件位号图生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s input.csv                    # 在当前目录生成所有类型的PDF
  %(prog)s input.csv -o output_dir      # 指定输出目录
  %(prog)s input.csv --refdes-only      # 只生成编号图
  %(prog)s input.csv --package-only     # 只生成封装图
  %(prog)s input.csv --value-only       # 只生成值图
  %(prog)s input.csv -r -p              # 生成编号图和封装图

CSV文件格式要求:
  第一行为标题行：Num,RefDes,PartDecal,X,Y,Layer,Orient.,value
  数据行包含：序号、编号、封装、X坐标、Y坐标、层面、角度、值
  层面字段支持：Top（正面）、Bottom（反面）

生成的文件:
  RefDes_Top.pdf / RefDes_Bottom.pdf（编号图）
  Package_Top.pdf / Package_Bottom.pdf（封装图）  
  Value_Top.pdf / Value_Bottom.pdf（值图）
        """
    )
    
    parser.add_argument(
        'csv_file',
        help='输入的CSV文件路径'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='.',
        help='输出目录路径（默认为当前目录）'
    )
    
    # 生成选项
    generation_group = parser.add_argument_group('生成选项')
    generation_group.add_argument(
        '-r', '--refdes',
        action='store_true',
        help='生成编号图'
    )
    generation_group.add_argument(
        '-p', '--package',
        action='store_true',
        help='生成封装图'
    )
    generation_group.add_argument(
        '-v', '--value',
        action='store_true',
        help='生成值图'
    )
    
    # 便捷选项
    convenience_group = parser.add_argument_group('便捷选项')
    convenience_group.add_argument(
        '--refdes-only',
        action='store_true',
        help='只生成编号图'
    )
    convenience_group.add_argument(
        '--package-only',
        action='store_true',
        help='只生成封装图'
    )
    convenience_group.add_argument(
        '--value-only',
        action='store_true',
        help='只生成值图'
    )
    convenience_group.add_argument(
        '--all',
        action='store_true',
        help='生成所有类型的图（默认行为）'
    )
    
    # 其他选项
    parser.add_argument(
        '--quality',
        choices=['low', 'medium', 'high'],
        default='high',
        help='PDF质量（默认：high）'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细信息'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='PCB位号图生成器 v1.0'
    )
    
    return parser.parse_args()


def determine_generation_options(args):
    """确定生成选项"""
    # 如果指定了only选项，优先使用
    if args.refdes_only:
        return True, False, False
    elif args.package_only:
        return False, True, False
    elif args.value_only:
        return False, False, True
    
    # 如果指定了具体选项
    if args.refdes or args.package or args.value:
        return args.refdes, args.package, args.value
    
    # 默认生成所有类型
    return True, True, True


def print_progress(message, verbose=True):
    """打印进度信息"""
    if verbose:
        print(f"[INFO] {message}")


def main():
    """主函数"""
    try:
        # 设置错误处理器
        error_handler = get_error_handler()
        
        # 解析命令行参数
        args = parse_arguments()
        
        print_progress("PCB元器件位号图生成器 v1.0", args.verbose)
        print_progress("=" * 50, args.verbose)
        
        # 验证输入参数
        print_progress("验证输入参数...", args.verbose)
        validate_csv_file(args.csv_file)
        validate_output_directory(args.output)
        
        # 确定生成选项
        generate_refdes, generate_package, generate_value = determine_generation_options(args)
        
        if not (generate_refdes or generate_package or generate_value):
            raise ValidationError("请至少选择一种生成选项")
        
        print_progress(f"输入文件: {args.csv_file}", args.verbose)
        print_progress(f"输出目录: {args.output}", args.verbose)
        print_progress(f"生成选项: 编号图={generate_refdes}, 封装图={generate_package}, 值图={generate_value}", args.verbose)
        
        # 解析CSV文件
        print_progress("正在解析CSV文件...", args.verbose)
        parser = CSVParser()
        components = parser.parse_file(args.csv_file)
        
        stats = parser.get_statistics()
        print_progress(f"解析完成: 总计{stats['total']}个元器件，正面{stats['top']}个，反面{stats['bottom']}个", args.verbose)
        
        # 创建输出目录
        csv_filename = Path(args.csv_file).stem
        output_dir = Path(args.output) / csv_filename
        output_dir.mkdir(exist_ok=True)
        print_progress(f"输出目录: {output_dir}", args.verbose)
        
        # 初始化PDF生成器
        config = Config()
        config.pdf_quality = args.quality
        generator = PDFGenerator(config)
        
        generated_files = []
        
        # 生成编号图
        if generate_refdes:
            print_progress("正在生成编号图...", args.verbose)
            generator.generate_refdes_pdf(components, output_dir)
            generated_files.extend(['RefDes_Top.pdf', 'RefDes_Bottom.pdf'])
        
        # 生成封装图
        if generate_package:
            print_progress("正在生成封装图...", args.verbose)
            generator.generate_package_pdf(components, output_dir)
            generated_files.extend(['Package_Top.pdf', 'Package_Bottom.pdf'])
        
        # 生成值图
        if generate_value:
            print_progress("正在生成值图...", args.verbose)
            generator.generate_value_pdf(components, output_dir)
            generated_files.extend(['Value_Top.pdf', 'Value_Bottom.pdf'])
        
        print_progress("生成完成！", args.verbose)
        print_progress("", args.verbose)
        print("生成的文件:")
        for filename in generated_files:
            filepath = output_dir / filename
            if filepath.exists():
                file_size = filepath.stat().st_size / 1024  # KB
                print(f"  ✓ {filepath} ({file_size:.1f} KB)")
            else:
                print(f"  ✗ {filepath} (文件不存在)")
        
        print(f"\n所有文件已保存到: {output_dir.absolute()}")
        
        return 0
        
    except ValidationError as e:
        print(f"验证错误: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"文件错误: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"程序错误: {e}", file=sys.stderr)
        if args.verbose if 'args' in locals() else False:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
