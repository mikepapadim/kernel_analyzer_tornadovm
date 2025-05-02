#!/usr/bin/env python3

"""
Example script to analyze the provided OpenCL kernel.

Example usage:
    ./scripts/analyze_example_kernel.py test_kernels/example.cl
"""

import os
import sys
import argparse

# Add the project directory to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from kernel_analyzer.parsers.opencl_parser import OpenCLKernel
from kernel_analyzer.analyzers.bottleneck_analyzer import BottleneckAnalyzer
from kernel_analyzer.utils.visualizer import KernelVisualizer

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Analyze an OpenCL kernel file.')
    parser.add_argument('kernel_file', nargs='?', default='test_kernels/example.cl',
                        help='Path to the OpenCL kernel file (default: test_kernels/example.cl)')
    parser.add_argument('--output', '-o', default='test_kernels/analysis',
                        help='Directory to save analysis results (default: test_kernels/analysis)')
    args = parser.parse_args()
    
    file_path = args.kernel_file
    output_dir = args.output
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.", file=sys.stderr)
        sys.exit(1)
        
    # Read the kernel source
    with open(file_path, "r") as f:
        source_code = f.read()
        
    # Parse the kernel
    kernel = OpenCLKernel(source_code)
    print(f"Parsing kernel: {file_path}")
    kernel.parse()
    print(f"Kernel name identified: {kernel.name}")
    
    # Calculate metrics
    metrics = kernel.calculate_metrics()
    print(f"\nArithmetic Intensity: {metrics.arithmetic_intensity:.4f}")
    print(f"Likely bottleneck: {metrics.bottleneck.upper()}")
    
    # Get detailed bottleneck analysis with recommendations
    bottleneck_analysis = BottleneckAnalyzer.analyze(kernel)
    
    # Get kernel summary
    summary = kernel.get_summary()
    summary['recommendations'] = bottleneck_analysis['recommendations']
    
    # Generate and display a text report
    report = KernelVisualizer.generate_text_report(summary)
    print("\n" + report)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename based on kernel filename
    base_name = os.path.basename(file_path)
    base_name_without_ext = os.path.splitext(base_name)[0]
    output_file = os.path.join(output_dir, f"{base_name_without_ext}_analysis.json")
    
    # Write JSON output to file
    json_output = KernelVisualizer.to_json(summary)
    with open(output_file, "w") as f:
        f.write(json_output)
    print(f"\nDetailed analysis written to {output_file}")
    
if __name__ == "__main__":
    main() 