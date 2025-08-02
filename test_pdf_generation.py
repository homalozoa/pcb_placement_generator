#!/usr/bin/env python3

from pdf_generator import PDFGenerator
from csv_parser import Component
from config import Config

def test_pdf_generation():
    # 创建更密集的测试数据，模拟真实PCB布局
    components = {
        'top': [
            # 密集排列的0201元器件
            Component(1, "R1", "0201", 10.0, 20.0, "Top", 0, "10K"),
            Component(2, "R2", "0201", 10.5, 20.0, "Top", 0, "1K"),
            Component(3, "R3", "0201", 11.0, 20.0, "Top", 0, "100"),
            Component(4, "R4", "0201", 11.5, 20.0, "Top", 0, "47K"),
            Component(5, "R5", "0201", 12.0, 20.0, "Top", 0, "2.2K"),

            Component(6, "C1", "0201", 10.0, 20.5, "Top", 0, "100nF"),
            Component(7, "C2", "0201", 10.5, 20.5, "Top", 0, "10uF"),
            Component(8, "C3", "0201", 11.0, 20.5, "Top", 0, "1nF"),
            Component(9, "C4", "0201", 11.5, 20.5, "Top", 0, "22pF"),
            Component(10, "C5", "0201", 12.0, 20.5, "Top", 0, "100pF"),

            # 一些较大的元器件
            Component(11, "U1", "QFN-32", 25.0, 30.0, "Top", 0, "MCU"),
            Component(12, "U2", "SOT-23", 15.0, 25.0, "Top", 0, "LDO"),
            Component(13, "L1", "0805", 35.0, 30.0, "Top", 0, "10uH"),

            # 更多密集的小元器件
            Component(14, "R10", "0201", 13.0, 21.0, "Top", 0, "0R"),
            Component(15, "R11", "0201", 13.5, 21.0, "Top", 0, "33R"),
            Component(16, "R12", "0201", 14.0, 21.0, "Top", 0, "75R"),
            Component(17, "C10", "0201", 13.0, 21.5, "Top", 0, "4.7uF"),
            Component(18, "C11", "0201", 13.5, 21.5, "Top", 0, "220nF"),
            Component(19, "C12", "0201", 14.0, 21.5, "Top", 0, "47nF"),
        ],
        'bottom': [],
        'all': []
    }

    # 创建配置和PDF生成器
    config = Config()
    generator = PDFGenerator(config)

    # 创建输出目录
    from pathlib import Path
    output_dir = Path('test_optimized_output')
    output_dir.mkdir(exist_ok=True)

    # 生成PDF
    generator.generate_refdes_pdf(components, output_dir)
    
    print(f"PDF generated in: {output_dir}")
    print(f"Generated layout for {len(components['top'])} components")
    print("Features:")
    print("- Text centered on component coordinates")
    print("- No component outlines or center dots")
    print("- Font size optimized for 0201 components")
    print("- Improved overlap avoidance")

    # 列出生成的文件
    for pdf_file in output_dir.glob('*.pdf'):
        print(f"  Generated: {pdf_file}")

if __name__ == "__main__":
    test_pdf_generation()
