#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
布局测试脚本
创建密集排列的元器件来测试文字重叠避免算法
"""

import csv
from pathlib import Path
from csv_parser import CSVParser
from pdf_generator import PDFGenerator
from config import Config


def create_dense_test_csv():
    """创建密集排列的测试CSV文件"""
    test_data = [
        ['Num', 'RefDes', 'PartDecal', 'X', 'Y', 'Layer', 'Orient.', 'value']
    ]
    
    # 创建密集的网格布局
    component_id = 1
    for x in range(0, 50, 5):  # X坐标：0, 5, 10, ..., 45
        for y in range(0, 30, 3):  # Y坐标：0, 3, 6, ..., 27
            layer = 'Top' if (x + y) % 2 == 0 else 'Bottom'
            
            # 不同类型的元器件
            if component_id % 3 == 0:
                refdes = f'C{component_id}'
                package = 'C0603'
                value = '10uF'
            elif component_id % 3 == 1:
                refdes = f'R{component_id}'
                package = 'R0402'
                value = '1K'
            else:
                refdes = f'U{component_id}'
                package = 'QFN48'
                value = 'IC'
            
            test_data.append([
                component_id, refdes, package, x, y, layer, 0, value
            ])
            component_id += 1
    
    # 保存到CSV文件
    with open('dense_test.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(test_data)
    
    print(f"创建了包含 {component_id-1} 个元器件的密集测试文件: dense_test.csv")
    return 'dense_test.csv'


def test_layout_algorithm():
    """测试布局算法"""
    print("布局算法测试")
    print("=" * 50)
    
    # 创建测试文件
    csv_file = create_dense_test_csv()
    
    # 解析CSV
    parser = CSVParser()
    components = parser.parse_file(csv_file)
    
    stats = parser.get_statistics()
    print(f"解析结果: {stats}")
    
    # 创建输出目录
    output_dir = Path('layout_test_output')
    output_dir.mkdir(exist_ok=True)
    
    # 生成PDF
    config = Config()
    generator = PDFGenerator(config)
    
    print("正在生成测试PDF...")
    generator.generate_refdes_pdf(components, output_dir)
    
    print("测试完成！")
    print(f"生成的文件:")
    for pdf_file in output_dir.glob('*.pdf'):
        print(f"  {pdf_file}")
    
    # 清理测试文件
    Path(csv_file).unlink()


def create_overlap_test_csv():
    """创建重叠测试CSV文件"""
    test_data = [
        ['Num', 'RefDes', 'PartDecal', 'X', 'Y', 'Layer', 'Orient.', 'value'],
        # 在同一位置放置多个元器件（测试极端情况）
        [1, 'C1', 'C0603', 10.0, 10.0, 'Top', 0, '10uF'],
        [2, 'C2', 'C0603', 10.1, 10.1, 'Top', 0, '22uF'],
        [3, 'C3', 'C0603', 10.2, 10.2, 'Top', 0, '100nF'],
        [4, 'R1', 'R0402', 10.0, 10.5, 'Top', 0, '1K'],
        [5, 'R2', 'R0402', 10.5, 10.0, 'Top', 0, '2.2K'],
        [6, 'U1', 'QFN48', 15.0, 15.0, 'Top', 0, 'MCU'],
        [7, 'U2', 'QFN48', 15.1, 15.1, 'Top', 0, 'FPGA'],
        # 添加一些正常间距的元器件作为对比
        [8, 'C10', 'C0603', 30.0, 30.0, 'Top', 0, '10uF'],
        [9, 'R10', 'R0402', 40.0, 40.0, 'Top', 0, '1K'],
        [10, 'U10', 'QFN48', 50.0, 50.0, 'Top', 0, 'IC'],
    ]
    
    with open('overlap_test.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(test_data)
    
    print("创建了重叠测试文件: overlap_test.csv")
    return 'overlap_test.csv'


def test_overlap_handling():
    """测试重叠处理"""
    print("\n重叠处理测试")
    print("=" * 50)
    
    # 创建测试文件
    csv_file = create_overlap_test_csv()
    
    # 解析CSV
    parser = CSVParser()
    components = parser.parse_file(csv_file)
    
    # 创建输出目录
    output_dir = Path('overlap_test_output')
    output_dir.mkdir(exist_ok=True)
    
    # 生成PDF
    config = Config()
    generator = PDFGenerator(config)
    
    print("正在生成重叠测试PDF...")
    generator.generate_refdes_pdf(components, output_dir)
    generator.generate_package_pdf(components, output_dir)
    generator.generate_value_pdf(components, output_dir)
    
    print("重叠测试完成！")
    print(f"生成的文件:")
    for pdf_file in output_dir.glob('*.pdf'):
        print(f"  {pdf_file}")
    
    # 清理测试文件
    Path(csv_file).unlink()


def main():
    """主函数"""
    try:
        # 测试密集布局
        test_layout_algorithm()
        
        # 测试重叠处理
        test_overlap_handling()
        
        print("\n所有测试完成！")
        print("请检查生成的PDF文件，验证：")
        print("1. 文字是否清晰可读")
        print("2. 文字是否有重叠")
        print("3. 布局是否合理")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
