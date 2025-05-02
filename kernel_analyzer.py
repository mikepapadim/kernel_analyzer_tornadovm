#!/usr/bin/env python3
"""
Main entry point for the OpenCL Kernel Analyzer.
This script is a shortcut to run the kernel analyzer from the project root.
"""

import sys
import os
from pathlib import Path

# Add the project directory to the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import the CLI module
try:
    from kernel_analyzer.cli.analyzer_cli import main
except ImportError:
    print("ERROR: Could not import kernel_analyzer.cli.analyzer_cli.")
    print("Make sure you're running this script from the project root directory.")
    sys.exit(1)

if __name__ == "__main__":
    # Execute the CLI main function
    sys.exit(main()) 