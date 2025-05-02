#!/usr/bin/env python3
"""
OpenCL Kernel Analyzer Debug Tool

This script provides a standalone utility for analyzing OpenCL kernel files
and generating detailed reports on branch divergence, data type usage, and
expensive operations. It outputs both to the console and to JSON files.

Example usage:
    ./scripts/debug_data_format.py test_kernels/example.cl
    ./scripts/debug_data_format.py test_kernels/example.cl test_kernels/complex.cl --verbose
"""

import sys
import os
import json
import argparse
import traceback
from pprint import pprint
from typing import Dict, Any, Optional, List

# Add the project directory to the path so we can import from the project
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from kernel_analyzer.parsers import ParserRegistry
    from kernel_analyzer.analyzers import BranchDivergenceAnalyzer
except ImportError:
    print("ERROR: Could not import kernel_analyzer modules.")
    print("Make sure you're running this script from the project root directory.")
    sys.exit(1)

def read_kernel_file(file_path: str) -> Optional[str]:
    """
    Read a kernel file and return its contents.
    
    Args:
        file_path: Path to the kernel file
        
    Returns:
        String containing the file contents, or None if an error occurred
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def analyze_kernel(file_path: str, verbose: bool = False, output_dir: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Analyze a kernel file and print the results.
    
    Args:
        file_path: Path to the kernel file
        verbose: Whether to print verbose output
        output_dir: Directory to save analysis results
        
    Returns:
        Dictionary containing the analysis results, or None if analysis failed
    """
    print(f"\n{'='*80}")
    print(f"ANALYZING: {file_path}")
    print(f"{'='*80}\n")
    
    # Read the kernel file
    kernel_code = read_kernel_file(file_path)
    if not kernel_code:
        return None
    
    # Get the file extension
    file_ext = os.path.splitext(file_path)[1]
    
    # Get the appropriate parser
    parser_class = ParserRegistry.get_parser(f"dummy{file_ext}")
    if not parser_class:
        print(f"No parser available for {file_ext} files.")
        return None
    
    # Parse the kernel
    try:
        kernel = parser_class(kernel_code)
        kernel.parse()
    except Exception as e:
        print(f"Error parsing kernel: {e}")
        if verbose:
            traceback.print_exc()
        return None
    
    # Analyze branch divergence
    try:
        branch_analyzer = BranchDivergenceAnalyzer(kernel)
        branch_analysis = branch_analyzer.analyze()
    except Exception as e:
        print(f"Error in branch analysis: {e}")
        if verbose:
            traceback.print_exc()
        return None
    
    # Print results
    print_analysis_results(branch_analysis, verbose)
    
    # Generate recommendations
    recommendations = branch_analyzer.get_recommendations()
    if recommendations:
        print("\n>> RECOMMENDATIONS")
        for rec in recommendations:
            print(f"- {rec}")
    
    # Save results to a JSON file
    save_analysis_json(file_path, branch_analysis, output_dir)
    
    return branch_analysis

def save_analysis_json(file_path: str, analysis: Dict[str, Any], output_dir: Optional[str] = None) -> None:
    """
    Save analysis results to a JSON file.
    
    Args:
        file_path: Original kernel file path (used to generate output filename)
        analysis: Analysis results dictionary
        output_dir: Directory to save analysis results
    """
    # Determine output filename and path
    base_filename = os.path.basename(file_path)
    base_name_without_ext = os.path.splitext(base_filename)[0]
    
    if output_dir:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{base_name_without_ext}_analysis.json")
    else:
        # By default, save to test_kernels/analysis directory
        analysis_dir = os.path.join(project_root, "test_kernels", "analysis")
        os.makedirs(analysis_dir, exist_ok=True)
        output_file = os.path.join(analysis_dir, f"{base_name_without_ext}_analysis.json")
    
    try:
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"\nAnalysis saved to {output_file}")
    except Exception as e:
        print(f"Error saving analysis to file: {e}")

def print_analysis_results(analysis: Dict[str, Any], verbose: bool = False) -> None:
    """
    Print formatted analysis results to the console.
    
    Args:
        analysis: Analysis results dictionary
        verbose: Whether to print verbose output
    """
    print("\n>> BRANCH ANALYSIS RESULTS")
    print(f"Root keys: {list(analysis.keys())}")
    
    # Print branch divergence information
    if 'branch_divergence' in analysis:
        bd = analysis['branch_divergence']
        print("\n>> BRANCH DIVERGENCE")
        print(f"Type: {type(bd)}")
        print(f"Keys: {list(bd.keys())}")
        print(f"Branch points: {bd.get('branch_points', 0)}")
        print(f"Max branch depth: {bd.get('max_branch_depth', 0)}")
        print(f"Divergence risk: {bd.get('divergence_risk', 'N/A')}")
        
        # Print details of branch points
        branch_points = bd.get('branch_points_detailed', [])
        if branch_points:
            print(f"\nDetailed branch points ({len(branch_points)}):")
            # Limit to 5 points in standard output, show all in verbose mode
            points_to_show = branch_points if verbose else branch_points[:5]
            for i, point in enumerate(points_to_show):
                print(f"  Point {i+1}: Line {point.get('line')}, Type: {point.get('type')}, Risk: {point.get('risk')}")
            if not verbose and len(branch_points) > 5:
                print(f"  ... and {len(branch_points) - 5} more points")
    
    # Print data type information
    if 'data_types' in analysis:
        dt = analysis['data_types']
        print("\n>> DATA TYPES")
        print(f"Type: {type(dt)}")
        if isinstance(dt, dict):
            print(f"Count: {len(dt)} unique data types")
            # Get top 5 types by occurrence
            sorted_types = sorted(dt.items(), key=lambda x: x[1], reverse=True)
            top_types = sorted_types[:5]
            print("Top 5 data types:")
            for type_name, count in top_types:
                print(f"  {type_name}: {count} occurrences")
            
            # In verbose mode, show all data types
            if verbose and len(sorted_types) > 5:
                print("\nAll data types:")
                for type_name, count in sorted_types:
                    print(f"  {type_name}: {count} occurrences")
    
    # Print expensive operations information
    if 'expensive_operations' in analysis:
        eo = analysis['expensive_operations']
        print("\n>> EXPENSIVE OPERATIONS")
        print(f"Type: {type(eo)}")
        print(f"Keys: {list(eo.keys()) if isinstance(eo, dict) else 'Not a dict'}")
        
        if 'operations' in eo:
            ops = eo['operations']
            print("Categories:")
            for category, op_dict in ops.items():
                print(f"  {category}: {len(op_dict)} operation types")
                for op, count in op_dict.items():
                    print(f"    {op}: {count} occurrences")
        
        if 'summary' in eo:
            print(f"\nSummary: {eo['summary']}")
    
    # In verbose mode, print the full JSON structure
    if verbose:
        print("\n>> FULL ANALYSIS JSON")
        print(json.dumps(analysis, indent=2))

def main():
    """
    Parse command line arguments and analyze specified kernel files.
    """
    parser = argparse.ArgumentParser(
        description='Analyze kernel files for branch divergence and data types.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('files', nargs='+', help='Kernel files to analyze')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show more detailed output')
    parser.add_argument('--output', '-o', help='Directory to save analysis files (default: test_kernels/analysis)')
    
    args = parser.parse_args()
    
    # Process each file
    results = {}
    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        
        result = analyze_kernel(file_path, args.verbose, args.output)
        if result:
            results[file_path] = result
    
    # Return success if we analyzed at least one file
    return 0 if results else 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./scripts/debug_data_format.py <kernel_file> [<kernel_file2> ...]")
        print("Example: ./scripts/debug_data_format.py test_kernels/example.cl test_kernels/complex.cl")
        sys.exit(1)
    
    sys.exit(main()) 