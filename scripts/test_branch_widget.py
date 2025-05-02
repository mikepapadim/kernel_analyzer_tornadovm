#!/usr/bin/env python3
"""
Test script for the branch divergence, data type, and expensive operations widgets.

This script creates a test window with the widgets and loads sample data to verify
their functionality independently of the main application.

Example usage:
    ./scripts/test_branch_widget.py
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

# Add the project directory to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import widgets from the GUI module
from scripts.gui.kernel_analyzer_qt import BranchDivergenceWidget, TypeAnalysisWidget, ExpensiveOperationsWidget

# Create sample data that matches the expected structure
sample_data = {
    'branch_divergence': {
        'branch_points': 5,
        'max_branch_depth': 3,
        'nested_branch_count': 2,
        'divergence_risk': 'Medium',
        'branch_points_detailed': [
            {
                'line': 10,
                'type': 'if',
                'depth': 1,
                'thread_dependent': False,
                'in_loop': False,
                'risk': 'Low'
            },
            {
                'line': 20,
                'type': 'if',
                'depth': 2,
                'thread_dependent': True,
                'in_loop': True,
                'risk': 'High'
            }
        ]
    },
    'data_types': {
        'float': 15,
        'int': 10,
        '__global': 5,
        'double': 2
    },
    'expensive_operations': {
        'operations': {
            'Moderately Expensive': {
                'int_mul': 5,
                'bit_shifts': 3
            },
            'Expensive': {
                'division': 10,
                'modulo': 2
            },
            'Very Expensive': {
                'sqrt': 3,
                'log': 1
            }
        },
        'summary': 'Kernel contains 24 expensive operations that may impact performance'
    }
}

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Branch Widget Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create the widgets to test
        branch_widget = BranchDivergenceWidget()
        type_widget = TypeAnalysisWidget()
        ops_widget = ExpensiveOperationsWidget()
        
        # Add widgets to layout
        layout.addWidget(branch_widget)
        layout.addWidget(type_widget)
        layout.addWidget(ops_widget)
        
        # Load the data
        print("Loading branch divergence data...")
        branch_widget.update_results(sample_data['branch_divergence'])
        
        print("Loading data types data...")
        type_widget.update_results(sample_data['data_types'])
        
        print("Loading expensive operations data...")
        ops_widget.update_results(sample_data['expensive_operations'])

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 