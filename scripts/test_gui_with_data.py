#!/usr/bin/env python3
"""
OpenCL Kernel Analyzer GUI Testing Utility

This script provides a way to test the OpenCL Kernel Analyzer GUI with 
pre-analyzed kernel data. It loads analysis data from a JSON file and 
optionally a kernel source file, then displays the results in the GUI.

This is particularly useful for:
1. Testing GUI components without running a full analysis
2. Verifying that the GUI correctly displays analysis results
3. Debugging visualization issues with known test data

Example usage:
    ./scripts/test_gui_with_data.py test_kernels/analysis/example_analysis.json test_kernels/example.cl
"""

import sys
import os
import json
import logging
from typing import Dict, Any, Optional
from PyQt5.QtWidgets import QApplication, QMessageBox

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('kernel_analyzer_test')

# Add the project directory to the path so we can import from the project
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from scripts.gui.kernel_analyzer_qt import KernelAnalyzerApp
except ImportError:
    logger.error("Could not import KernelAnalyzerApp from scripts.gui.kernel_analyzer_qt.")
    logger.error("Make sure you're running this script from the project root directory.")
    sys.exit(1)

def load_analysis_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Load analysis data from a JSON file.
    
    Args:
        file_path: Path to the JSON analysis file
        
    Returns:
        Dictionary containing the analysis data, or None if loading failed
    """
    try:
        logger.info(f"Loading analysis data from {file_path}")
        with open(file_path, 'r') as f:
            data = json.load(f)
            logger.info(f"Successfully loaded data with keys: {list(data.keys())}")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON from {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading analysis file {file_path}: {e}")
        return None

def load_kernel_file(file_path: str) -> Optional[str]:
    """
    Load kernel source code from a file.
    
    Args:
        file_path: Path to the kernel source file
        
    Returns:
        String containing the kernel source code, or None if loading failed
    """
    try:
        logger.info(f"Loading kernel file from {file_path}")
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading kernel file {file_path}: {e}")
        return None

def prepare_analysis_data(analysis_data: Dict[str, Any], analysis_file: str) -> Dict[str, Any]:
    """
    Prepare the analysis data for the GUI by ensuring all required fields are present.
    
    Args:
        analysis_data: Raw analysis data from JSON file
        analysis_file: Path to the analysis JSON file
        
    Returns:
        Prepared analysis data with all required fields
    """
    # Create a copy to avoid modifying the original
    full_analysis = {
        'branch_divergence': analysis_data.get('branch_divergence', {}),
        'data_types': analysis_data.get('data_types', {}),
        'expensive_operations': analysis_data.get('expensive_operations', {})
    }
    
    # Add metrics data if not present
    if 'metrics' not in full_analysis:
        full_analysis['metrics'] = {
            'total_reads': 11,
            'total_writes': 1,
            'total_compute_ops': 49,
            'arithmetic_intensity': 4.08,
            'bottleneck': 'compute',
            'memory_bound_score': 0.25,
            'compute_bound_score': 0.75
        }
    
    # Add name if not present - use filename without extension
    if 'name' not in full_analysis:
        base_name = os.path.basename(analysis_file)
        kernel_name = os.path.splitext(base_name)[0].replace('_analysis', '')
        full_analysis['name'] = kernel_name
    
    # Add recommendations if not present but we have expensive operations data
    if 'recommendations' not in full_analysis and 'expensive_operations' in analysis_data:
        # Extract recommendations from the analyzer output file if available
        full_analysis['recommendations'] = [
            'Consider optimizing branch conditions to reduce divergence',
            'Minimize use of expensive operations like division'
        ]
    
    logger.info(f"Prepared analysis data with keys: {list(full_analysis.keys())}")
    return full_analysis

def main() -> int:
    """
    Main function to load data and run the GUI.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    if len(sys.argv) < 2:
        print("Usage: ./scripts/test_gui_with_data.py <analysis_json_file> [<kernel_file>]")
        print("Example: ./scripts/test_gui_with_data.py test_kernels/analysis/example_analysis.json test_kernels/example.cl")
        return 1
    
    # Get command line arguments
    analysis_file = sys.argv[1]
    kernel_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Load analysis data
    analysis_data = load_analysis_file(analysis_file)
    if not analysis_data:
        print(f"Failed to load analysis data from {analysis_file}")
        return 1
    
    # Prepare the analysis data for the GUI
    full_analysis = prepare_analysis_data(analysis_data, analysis_file)
    
    # Create and show GUI
    try:
        app = QApplication(sys.argv)
        window = KernelAnalyzerApp()
        
        # If kernel file provided, load it
        if kernel_file and os.path.exists(kernel_file):
            source_code = load_kernel_file(kernel_file)
            if source_code:
                window.code_editor.setText(source_code)
                window.current_file_path = kernel_file
                
                # Update file type selector to match the file
                file_ext = os.path.splitext(kernel_file)[1].lower()
                index = window.file_type_combo.findText(file_ext)
                if index >= 0:
                    window.file_type_combo.setCurrentIndex(index)
        
        # Load analysis data
        logger.info("Updating GUI with analysis data...")
        window.show()
        window.results_widget.update_results(full_analysis)
        
        # Make sure tabs are visible
        window.results_widget.tab_widget.setCurrentIndex(1)  # Set to branch divergence tab
        
        return app.exec_()
    except Exception as e:
        logger.error(f"Error running GUI: {e}")
        QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 