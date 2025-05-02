#!/usr/bin/env python3

"""
Main entry point for the OpenCL Kernel Analyzer GUI.
This script is a shortcut to run the GUI from the project root.
"""

import sys
import os
from pathlib import Path

# Add the project directory to the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import the GUI module
try:
    from scripts.gui.kernel_analyzer_qt import main
except ImportError:
    print("ERROR: Could not import scripts.gui.kernel_analyzer_qt.")
    print("Make sure you're running this script from the project root directory.")
    sys.exit(1)

if __name__ == "__main__":
    # Execute the GUI main function
    sys.exit(main()) 