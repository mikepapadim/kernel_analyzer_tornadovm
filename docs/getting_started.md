# Getting Started with OpenCL Kernel Analyzer

This guide will help you get started with the OpenCL Kernel Performance Analyzer, from installation to running your first analysis.

## Installation

### Prerequisites

Before installing the analyzer, make sure you have:

- Python 3.7 or newer
- pip (Python package installer)
- Basic familiarity with OpenCL kernels

### Installing from PyPI

The simplest way to install is using pip:

```bash
pip install kernel-analyzer
```

### Installing from Source

If you prefer to install from source:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-organization/kernel-analyzer.git
   cd kernel-analyzer
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

## Running Your First Analysis

### Using the GUI

1. Launch the GUI:
   ```bash
   kernel-analyzer-gui
   (Or run `./kernel_analyzer_gui.py` if installed from source)
   ```

2. Use the File menu to open an OpenCL kernel file (e.g., `example.cl` included in the repository).

3. Select the file type (`.cl` for OpenCL) from the dropdown.

4. Click the "Analyze" button to start the analysis.

5. Review the results in the tabbed interface:
   - Performance metrics
   - Branch divergence
   - Data type usage
   - Expensive operations
   - Recommendations

### Using the Command Line

1. Analyze a kernel from the command line:
   ```bash
   kernel-analyzer example.cl
   ```
   (Or run `./analyzer_cli.py example.cl` if installed from source)

2. View the analysis report in the terminal output.

3. Add flags for more detailed output or to save the results:
   ```bash
   kernel-analyzer example.cl --format json --output analysis.json
   ```

## Understanding the Results

After running an analysis, you'll see several categories of results:

- **Performance Metrics**: Overall assessment of kernel performance characteristics
- **Branch Divergence**: Analysis of conditional branches that might cause thread divergence
- **Data Types**: Breakdown of data types used in the kernel
- **Vector Operations**: Analysis of vector operations and their efficiency
- **Expensive Operations**: Identification of computationally costly operations
- **Recommendations**: Actionable suggestions for improving kernel performance

## Next Steps

Now that you've run your first analysis, you can:

1. Learn more about [interpreting analysis results](user_guide/analyzing_results.md)
2. Explore the [GUI features](user_guide/gui_application.md) in detail
3. Check out [example kernels](examples/README.md) with annotations
4. Try [optimizing a kernel](examples/optimization_workflow.md) using the analyzer's recommendations

## Troubleshooting

If you encounter any issues:

- Check the [troubleshooting guide](user_guide/troubleshooting.md)
- Look for similar issues in the [GitHub issues](https://github.com/your-organization/kernel-analyzer/issues)
- Open a new issue if your problem hasn't been reported 