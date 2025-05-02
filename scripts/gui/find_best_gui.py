#!/usr/bin/env python3

"""
Utility to find the best available GUI backend for the OpenCL Kernel Analyzer.

This script checks for available GUI backends (PyQt5, PySide2, Tkinter)
and provides guidance on which one to use.
"""

import importlib
import sys

def check_module(module_name):
    """Check if a module can be imported."""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def main():
    """Check for available GUI backends and recommend the best one."""
    print("Checking available GUI backends for OpenCL Kernel Analyzer...")
    
    # Check for PyQt5
    if check_module("PyQt5"):
        print("\nPyQt5 is available (Recommended).")
        print("You can run the PyQt5-based GUI with:")
        print("    ./kernel_analyzer_gui.py")
        return 0
    
    # Check for PySide2
    if check_module("PySide2"):
        print("\nPySide2 is available (Alternative to PyQt5).")
        print("PyQt5 is not available, but PySide2 can be used instead.")
        print("You can run the PySide2-based GUI with:")
        print("    ./kernel_analyzer_gui.py")
        print("\nNote: Some features may have differences compared to the PyQt5 version.")
        return 0
    
    # Check for Tkinter
    if check_module("tkinter"):
        print("\nOnly Tkinter is available (Limited functionality).")
        print("Neither PyQt5 nor PySide2 are available.")
        print("You can run the Tkinter-based GUI with:")
        print("    ./kernel_analyzer_gui.py")
        print("\nNote: The Tkinter GUI has limited functionality compared to the Qt version.")
        print("      Consider installing PyQt5 for the full experience:")
        print("      pip install PyQt5")
        return 0
    
    # No GUI backend available
    print("\nNo GUI backend available.")
    print("Please install one of the following packages:")
    print("    pip install PyQt5 (Recommended)")
    print("    pip install PySide2")
    print("    pip install tkinter")
    
    print("\nAfter installing a GUI backend, you can run the GUI with:")
    print(f"    ./kernel_analyzer_gui.py")
    
    return 1

if __name__ == "__main__":
    sys.exit(main()) 