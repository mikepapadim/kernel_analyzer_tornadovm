#!/usr/bin/env python3
"""
Script to launch the Kernel Analyzer GUI and take a screenshot of it.
"""

import os
import sys
import time
from pathlib import Path

# Add the project directory to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Create the images directory if it doesn't exist
os.makedirs(os.path.join(project_root, "docs", "images"), exist_ok=True)

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QTimer
    from PyQt5.QtGui import QPixmap
    from scripts.gui.kernel_analyzer_qt import KernelAnalyzerApp
except ImportError as e:
    print(f"Error importing required modules: {e}")
    sys.exit(1)

def capture_screenshot():
    """Capture a screenshot of the application."""
    print("Taking screenshot...")
    global window
    
    # Give the window some time to fully render
    time.sleep(1)
    
    # Take a screenshot of the window
    screenshot = window.grab()
    
    # Save the screenshot
    screenshot_path = os.path.join(project_root, "docs", "images", "home.png")
    screenshot.save(screenshot_path, "PNG")
    print(f"Screenshot saved to {screenshot_path}")
    
    # Exit the application
    QApplication.quit()

def main():
    """Launch the application and take a screenshot."""
    global window
    
    # Create the application
    app = QApplication(sys.argv)
    
    # Create the window
    window = KernelAnalyzerApp()
    
    # Load a kernel file if it exists
    kernel_file = os.path.join(project_root, "test_kernels", "complex.cl")
    if os.path.exists(kernel_file):
        with open(kernel_file, 'r') as f:
            window.code_editor.setText(f.read())
            window.current_file_path = kernel_file
    
    # Perform an analysis to populate the results
    window.analyze_current_kernel()
    
    # Show the window
    window.show()
    
    # Schedule the screenshot capture
    QTimer.singleShot(2000, capture_screenshot)
    
    # Run the application
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main()) 