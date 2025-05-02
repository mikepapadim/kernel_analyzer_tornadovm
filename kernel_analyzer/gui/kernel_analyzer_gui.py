import sys
import os
import json
import traceback
from typing import Dict, Any, Optional

# Set matplotlib backend before importing PyQt5
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid segfaults

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                            QFileDialog, QComboBox, QTabWidget, QSplitter,
                            QGroupBox, QFormLayout, QStatusBar, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QTextCursor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Import kernel analyzer components with error handling
try:
    from kernel_analyzer.parsers.parser_registry import ParserRegistry
    from kernel_analyzer.analyzers.bottleneck_analyzer import BottleneckAnalyzer
    from kernel_analyzer.analyzers.branch_analyzer import BranchDivergenceAnalyzer
    from kernel_analyzer.utils.visualizer import KernelVisualizer
except ImportError as e:
    print(f"Error importing kernel analyzer modules: {e}")
    sys.exit(1)

class KernelCodeEditor(QTextEdit):
    """Text editor for displaying kernel code"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        font = QFont("Courier New", 10)
        self.setFont(font)
        self.setLineWrapMode(QTextEdit.NoWrap)

class AnalysisResultsWidget(QWidget):
    """Widget for displaying analysis results"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Summary section
        self.summary_group = QGroupBox("Summary")
        self.summary_layout = QFormLayout()
        self.kernel_name_label = QLabel("-")
        self.bottleneck_label = QLabel("-")
        self.arithmetic_intensity_label = QLabel("-")
        
        self.summary_layout.addRow("Kernel Name:", self.kernel_name_label)
        self.summary_layout.addRow("Primary Bottleneck:", self.bottleneck_label)
        self.summary_layout.addRow("Arithmetic Intensity:", self.arithmetic_intensity_label)
        self.summary_group.setLayout(self.summary_layout)
        
        # Statistics section
        self.stats_group = QGroupBox("Operation Statistics")
        self.stats_layout = QFormLayout()
        self.reads_label = QLabel("0")
        self.writes_label = QLabel("0")
        self.compute_ops_label = QLabel("0")
        self.memory_bound_label = QLabel("0.00")
        self.compute_bound_label = QLabel("0.00")
        
        self.stats_layout.addRow("Total Reads:", self.reads_label)
        self.stats_layout.addRow("Total Writes:", self.writes_label)
        self.stats_layout.addRow("Compute Operations:", self.compute_ops_label)
        self.stats_layout.addRow("Memory Bound Score:", self.memory_bound_label)
        self.stats_layout.addRow("Compute Bound Score:", self.compute_bound_label)
        self.stats_group.setLayout(self.stats_layout)
        
        # Add chart (with error handling)
        try:
            self.figure = Figure(figsize=(5, 4), dpi=100)
            self.canvas = FigureCanvas(self.figure)
            self.canvas.setMinimumHeight(200)
        except Exception as e:
            print(f"Error initializing matplotlib: {e}")
            self.figure = None
            self.canvas = QLabel("Chart initialization failed")
            self.canvas.setAlignment(Qt.AlignCenter)
            self.canvas.setMinimumHeight(200)
            self.canvas.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        
        # Recommendations section
        self.recommendations_group = QGroupBox("Optimization Recommendations")
        self.recommendations_layout = QVBoxLayout()
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setReadOnly(True)
        self.recommendations_layout.addWidget(self.recommendations_text)
        self.recommendations_group.setLayout(self.recommendations_layout)
        
        # Add all sections to the main layout
        self.layout.addWidget(self.summary_group)
        self.layout.addWidget(self.stats_group)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.recommendations_group)
        self.setLayout(self.layout)
        
    def update_results(self, analysis: Dict[str, Any]) -> None:
        """Update the results display with the given analysis"""
        metrics = analysis.get('metrics', {})
        
        # Update summary section
        self.kernel_name_label.setText(analysis.get('name', '-'))
        self.bottleneck_label.setText(metrics.get('bottleneck', '-').upper())
        self.arithmetic_intensity_label.setText(f"{metrics.get('arithmetic_intensity', 0):.4f}")
        
        # Update statistics section
        self.reads_label.setText(str(metrics.get('total_reads', 0)))
        self.writes_label.setText(str(metrics.get('total_writes', 0)))
        self.compute_ops_label.setText(str(metrics.get('total_compute_ops', 0)))
        self.memory_bound_label.setText(f"{metrics.get('memory_bound_score', 0):.4f}")
        self.compute_bound_label.setText(f"{metrics.get('compute_bound_score', 0):.4f}")
        
        # Update recommendations
        self.recommendations_text.clear()
        if 'recommendations' in analysis:
            for i, rec in enumerate(analysis['recommendations'], 1):
                self.recommendations_text.append(f"{i}. {rec}")
                
        # Update charts
        if hasattr(self, 'figure') and self.figure is not None:
            try:
                self.update_charts(metrics)
            except Exception as e:
                print(f"Error updating charts: {e}")
        
    def update_charts(self, metrics: Dict[str, Any]) -> None:
        """Update the visualization charts"""
        if not hasattr(self, 'figure') or self.figure is None:
            return
            
        try:
            self.figure.clear()
            
            # Create metrics chart
            ax1 = self.figure.add_subplot(121)
            
            # Compute vs Memory Operation ratio
            labels = ['Compute Ops', 'Memory Ops']
            compute_ops = metrics.get('total_compute_ops', 0)
            memory_ops = metrics.get('total_reads', 0) + metrics.get('total_writes', 0)
            sizes = [compute_ops, memory_ops]
            explode = (0.1, 0)  # Explode the compute slice
            
            ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            ax1.set_title('Operation Types')
            
            # Bottleneck chart
            ax2 = self.figure.add_subplot(122)
            
            bottleneck_data = [
                metrics.get('memory_bound_score', 0) * 100,
                metrics.get('compute_bound_score', 0) * 100
            ]
            bottleneck_labels = ['Memory Bound', 'Compute Bound']
            bar_colors = ['tab:red', 'tab:blue']
            
            ax2.bar(bottleneck_labels, bottleneck_data, color=bar_colors)
            ax2.set_ylim(0, 100)
            ax2.set_ylabel('Score (%)')
            ax2.set_title('Bottleneck Analysis')
            
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Error in chart rendering: {e}")
        
class KernelAnalyzerApp(QMainWindow):
    """Main application window for the Kernel Analyzer GUI"""
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Kernel Analyzer")
        self.setMinimumSize(900, 700)
        
        # Initialize instance variables
        self.current_kernel = None
        self.current_analysis = None
        self.current_file_path = None
        
        # Set up the main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main content area with splitter
        self.splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Code viewer
        self.code_editor = KernelCodeEditor()
        self.splitter.addWidget(self.code_editor)
        
        # Right side - Analysis results
        self.results_widget = AnalysisResultsWidget()
        self.splitter.addWidget(self.results_widget)
        
        # Set the initial sizes for the splitter
        self.splitter.setSizes([400, 500])
        
        # Add splitter to main layout
        self.main_layout.addWidget(self.splitter)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def create_toolbar(self):
        """Create the application toolbar"""
        toolbar_layout = QHBoxLayout()
        
        # File open button
        self.open_button = QPushButton("Open Kernel")
        self.open_button.clicked.connect(self.open_file)
        toolbar_layout.addWidget(self.open_button)
        
        # File type selector
        self.file_type_label = QLabel("File Type:")
        toolbar_layout.addWidget(self.file_type_label)
        
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems([".cl", ".ptx", ".spv"])
        toolbar_layout.addWidget(self.file_type_combo)
        
        # Analyze button
        self.analyze_button = QPushButton("Analyze Kernel")
        self.analyze_button.clicked.connect(self.analyze_current_kernel)
        self.analyze_button.setEnabled(False)
        toolbar_layout.addWidget(self.analyze_button)
        
        # Export button
        self.export_button = QPushButton("Export Results")
        self.export_button.clicked.connect(self.export_results)
        self.export_button.setEnabled(False)
        toolbar_layout.addWidget(self.export_button)
        
        # Add spacer to push buttons to the left
        toolbar_layout.addStretch()
        
        self.main_layout.addLayout(toolbar_layout)
        
    def open_file(self):
        """Open a kernel file"""
        options = QFileDialog.Options()
        file_filter = "OpenCL Kernels (*.cl);;PTX Files (*.ptx);;SPIR-V Files (*.spv);;All Files (*)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Kernel File", "", file_filter, options=options
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    source_code = f.read()
                
                self.current_file_path = file_path
                self.code_editor.setText(source_code)
                self.analyze_button.setEnabled(True)
                
                # Update file type selector to match the file
                file_ext = os.path.splitext(file_path)[1].lower()
                index = self.file_type_combo.findText(file_ext)
                if index >= 0:
                    self.file_type_combo.setCurrentIndex(index)
                
                self.status_bar.showMessage(f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")
                self.status_bar.showMessage("Error loading file")
    
    def analyze_current_kernel(self):
        """Analyze the currently loaded kernel"""
        if not self.current_file_path:
            QMessageBox.warning(self, "No Kernel Loaded", "Please load a kernel file first.")
            return
            
        try:
            # Show busy status
            self.status_bar.showMessage("Analyzing kernel...")
            QApplication.processEvents()
            
            # Get appropriate parser for file type
            file_ext = self.file_type_combo.currentText()
            parser_class = ParserRegistry.get_parser(f"dummy{file_ext}")
            
            if not parser_class:
                QMessageBox.warning(self, "Unsupported Format", 
                                   f"No parser available for {file_ext} files yet.")
                return
            
            # Read the kernel code from the editor
            source_code = self.code_editor.toPlainText()
            
            # Parse kernel
            kernel = parser_class(source_code)
            kernel.parse()
            self.current_kernel = kernel
            
            # Get analysis results
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
            
            # Store the analysis results
            self.current_analysis = analysis
            
            # Update results display
            self.results_widget.update_results(analysis)
            
            # Enable export button
            self.export_button.setEnabled(True)
            
            self.status_bar.showMessage("Analysis complete")
            
        except Exception as e:
            QMessageBox.critical(self, "Analysis Error", f"Failed to analyze kernel: {str(e)}\n{traceback.format_exc()}")
            self.status_bar.showMessage("Analysis failed")
    
    def export_results(self):
        """Export the analysis results to a file"""
        if not self.current_analysis:
            return
            
        options = QFileDialog.Options()
        file_filter = "JSON Files (*.json);;Text Files (*.txt);;All Files (*)"
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self, "Save Analysis Results", "", file_filter, options=options
        )
        
        if not file_path:
            return
            
        try:
            # Determine format based on selected filter or file extension
            if "JSON" in selected_filter or file_path.lower().endswith('.json'):
                output = KernelVisualizer.to_json(self.current_analysis)
            else:
                output = KernelVisualizer.generate_text_report(self.current_analysis)
                
            with open(file_path, 'w') as f:
                f.write(output)
                
            self.status_bar.showMessage(f"Results saved to {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export results: {str(e)}")
            self.status_bar.showMessage("Export failed")

def main():
    # Enable exception tracking
    sys.excepthook = traceback.print_exception
    
    try:
        app = QApplication(sys.argv)
        window = KernelAnalyzerApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Fatal error starting application: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 