#!/usr/bin/env python3

import sys
import json
from pprint import pprint

from kernel_analyzer.parsers.parser_registry import ParserRegistry
from kernel_analyzer.analyzers.branch_analyzer import BranchDivergenceAnalyzer
from kernel_analyzer.analyzers.bottleneck_analyzer import BottleneckAnalyzer

def test_analysis(file_path):
    """Run a test analysis on the given kernel file"""
    print(f"Testing analysis on: {file_path}")
    
    # Get appropriate parser for file type
    parser_class = ParserRegistry.get_parser(file_path)
    if not parser_class:
        print("Error: No parser available for this file type")
        return
    
    # Read file
    try:
        with open(file_path, 'r') as f:
            source_code = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Parse kernel
    try:
        kernel = parser_class(source_code)
        kernel.parse()
    except Exception as e:
        print(f"Error parsing kernel: {e}")
        return
    
    # Run branch analysis
    branch_analyzer = BranchDivergenceAnalyzer(kernel)
    branch_analysis = branch_analyzer.analyze()
    
    # Print results
    print("\n=== BRANCH DIVERGENCE ANALYSIS ===")
    print(f"Branch Points: {branch_analysis['branch_divergence']['branch_points']}")
    print(f"Max Depth: {branch_analysis['branch_divergence']['max_branch_depth']}")
    print(f"Divergence Risk: {branch_analysis['branch_divergence']['divergence_risk']}")
    
    # Print first few branch points
    print("\nFirst 3 Branch Points:")
    for bp in branch_analysis['branch_divergence']['branch_points_detailed'][:3]:
        print(f"Line {bp['line']}: {bp['type']} - Risk: {bp.get('risk', 'Unknown')}")
    
    print("\n=== DATA TYPES ANALYSIS ===")
    pprint(branch_analysis['data_types'])
    
    print("\n=== EXPENSIVE OPERATIONS ===")
    pprint(branch_analysis['expensive_operations'])
    
    # Get recommendations
    recs = branch_analyzer.get_recommendations()
    print("\n=== RECOMMENDATIONS ===")
    for i, rec in enumerate(recs, 1):
        print(f"{i}. {rec}")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_branch_analysis.py <kernel_file>")
        sys.exit(1)
    
    test_analysis(sys.argv[1]) 