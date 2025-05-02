import argparse
import os
import sys
import json
from typing import Optional

from kernel_analyzer.parsers.parser_registry import ParserRegistry
from kernel_analyzer.analyzers.bottleneck_analyzer import BottleneckAnalyzer
from kernel_analyzer.analyzers.branch_analyzer import BranchDivergenceAnalyzer
from kernel_analyzer.utils.visualizer import KernelVisualizer

def analyze_kernel(file_path: str, output_format: str = "text", output_file: Optional[str] = None) -> None:
    """
    Analyze a kernel file and output the results.
    
    Args:
        file_path: Path to the kernel file
        output_format: Format for the output ('text' or 'json')
        output_file: Optional file to write the output to
    """
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found", file=sys.stderr)
        sys.exit(1)
    
    # Get appropriate parser for file type
    parser_class = ParserRegistry.get_parser(file_path)
    if not parser_class:
        print(f"Error: No parser available for file type {os.path.splitext(file_path)[1]}", file=sys.stderr)
        sys.exit(1)
    
    # Read file
    try:
        with open(file_path, 'r') as f:
            source_code = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Parse kernel
    try:
        kernel = parser_class(source_code)
        kernel.parse()
    except Exception as e:
        print(f"Error parsing kernel: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Analyze kernel - compute intensity and bottleneck
    analysis = kernel.get_summary()
    
    # Add bottleneck recommendations
    bottleneck_analysis = BottleneckAnalyzer.analyze(kernel)
    analysis['recommendations'] = bottleneck_analysis['recommendations']
    
    # Add branch divergence and type analysis
    branch_analyzer = BranchDivergenceAnalyzer(kernel)
    branch_analysis = branch_analyzer.analyze()
    analysis['branch_divergence'] = branch_analysis['branch_divergence']
    analysis['data_types'] = branch_analysis['data_types']
    analysis['expensive_operations'] = branch_analysis['expensive_operations']
    
    # Add branch divergence recommendations
    branch_recommendations = branch_analyzer.get_recommendations()
    if branch_recommendations:
        if 'recommendations' not in analysis:
            analysis['recommendations'] = []
        analysis['recommendations'].extend(branch_recommendations)
    
    # Generate output
    if output_format == 'json':
        output = KernelVisualizer.to_json(analysis)
    else:  # text
        output = KernelVisualizer.generate_text_report(analysis)
    
    # Write or print output
    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(output)
            print(f"Analysis written to {output_file}")
        except Exception as e:
            print(f"Error writing to output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)

def main():
    parser = argparse.ArgumentParser(description="Analyze compute kernels to identify bottlenecks")
    parser.add_argument("file", help="Path to the kernel file to analyze")
    parser.add_argument("--format", choices=["text", "json"], default="text", 
                        help="Output format (default: text)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    
    args = parser.parse_args()
    analyze_kernel(args.file, args.format, args.output)

if __name__ == "__main__":
    main() 