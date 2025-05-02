# User Guide

This section provides comprehensive documentation for using the OpenCL Kernel Performance Analyzer.

## Contents

- [GUI Application](gui_application.md): How to use the graphical user interface
- [Command Line Interface](cli.md): How to use the command-line tools
- [Analyzing Results](analyzing_results.md): How to interpret analysis results
- [Optimization Workflow](optimization_workflow.md): A step-by-step process for optimizing kernels
- [Troubleshooting](troubleshooting.md): Common issues and solutions

## Interface Options

The OpenCL Kernel Performance Analyzer offers several interfaces to accommodate different workflows:

### Graphical User Interface (GUI)

The Qt-based GUI provides an interactive experience with visualizations and detailed analysis views. This is ideal for:

- Exploring kernel characteristics
- Visualizing performance metrics
- Interactive optimization

### Command Line Interface (CLI)

The CLI tools are perfect for:

- Batch processing multiple kernels
- Integration into automated workflows
- CI/CD pipelines for performance testing

### Debug and Testing Tools

Specialized tools for debugging and testing include:

- `debug_data_format.py`: For detailed dump of analysis data
- `test_gui_with_data.py`: For testing GUI with pre-analyzed data

## Common Workflows

1. **Quick Analysis**:
   - Load a kernel in the GUI
   - Run analysis
   - View recommendations

2. **Batch Processing**:
   - Use CLI to analyze multiple kernels
   - Generate JSON reports
   - Compare results

3. **Optimization Cycle**:
   - Analyze kernel
   - Apply recommendations
   - Re-analyze to verify improvements
   - Repeat until performance goals are met 