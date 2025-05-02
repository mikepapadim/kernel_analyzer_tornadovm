# OpenCL Kernel Analyzer - Directory Structure

This document explains the organization of the OpenCL Kernel Analyzer project directory structure.

## Root Directory

- `kernel_analyzer.py` - Main entry point for the CLI tool
- `kernel_analyzer_gui.py` - Main entry point for the GUI tool
- `setup.py` - Package installation configuration
- `pytest.ini` - Test configuration
- `LICENSE` - MIT license file
- `README.md` - Project overview and documentation
- `INSTALL.md` - Installation instructions
- `CONTRIBUTING.md` - Guidelines for contributors
- `CODEBASE_CLEANUP.md` - Documentation of code cleanup activities
- `.gitignore` - Git ignore configuration

## Main Directories

### `kernel_analyzer/` 

Core package containing the main functionality:

- `analyzers/` - Analysis modules (branch divergence, bottleneck, etc.)
- `parsers/` - Code to parse different types of kernel files
- `utils/` - Utility functions and classes
- `cli/` - Command-line interface
- `gui/` - Core GUI components (if any)
- `core/` - Core functionality shared across modules
- `backends/` - Backend implementations for different platforms

### `scripts/`

Utility scripts and tools:

- `debug_data_format.py` - Debug tool for data format analysis
- `test_gui_with_data.py` - Utility to test GUI with pre-analyzed data
- `test_branch_widget.py` - Test script for the branch divergence widget
- `analyze_example_kernel.py` - Example script to analyze a kernel
- `gui/` - GUI implementation files
  - `kernel_analyzer_qt.py` - PyQt5 implementation of the GUI
  - `kernel_analyzer_gui.py` - Simplified GUI launcher
  - `find_best_gui.py` - Utility to find the best available GUI backend

### `test_kernels/`

Test kernel files and analysis results:

- `example.cl` - Simple example kernel
- `complex.cl` - Complex example kernel
- `vectotypes.cl` - Kernel showcasing vector types
- `analysis/` - Analysis results in JSON format
  - `example_analysis.json`
  - `complex_analysis.json`
  - `vectotypes_analysis.json`

### `docs/`

Project documentation:

- `README.md` - Documentation index
- `user_guide/` - User guides
- `analysis/` - Analysis documentation
  - `SUMMARY.md` - Analysis summary
  - `vectotypes_summary.md` - Vector types analysis
- `gui/` - GUI documentation
  - `QT_GUI_USAGE_GUIDE.md` - Qt GUI usage guide
  - `QT_GUI_SCREENSHOT.txt` - Screenshots of the Qt GUI
  - `GUI_USAGE_GUIDE.md` - General GUI usage guide
  - `GUI_SCREENSHOT.txt` - General GUI screenshots

### `tests/`

Unit tests and testing utilities:

- `__init__.py` - Package initialization file
- `test_branch_analyzer.py` - Tests for the branch analyzer

### `examples/`

Example use cases and demos:

- (Various example scripts and kernel files)

## Installation and Usage

1. Install the package:
```
pip install -e .
```

2. Run the CLI tool:
```
./kernel_analyzer.py test_kernels/example.cl
```

3. Run the GUI tool:
```
./kernel_analyzer_gui.py
```

4. Run specific scripts:
```
./scripts/debug_data_format.py test_kernels/example.cl
./scripts/test_gui_with_data.py test_kernels/analysis/example_analysis.json test_kernels/example.cl
```

## Development

For development, refer to the `CONTRIBUTING.md` file for guidelines and the `INSTALL.md` file for setup instructions. 