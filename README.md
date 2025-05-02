# Kernel Static Analyzer for TornadoVM

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://github.com/your-organization/kernel-analyzer/docs)

A comprehensive static analysis tool for optimizing OpenCL compute kernels. This application helps identify performance bottlenecks, branch divergence issues, data type usage, and expensive operations in compute kernels to improve GPU performance.

![Analyzer Screenshot](docs/images/analyzer_screenshot.png)

## 🚀 Features

- **Performance Analysis**: Analyze compute kernels to identify bottlenecks and optimization opportunities
- **Branch Divergence Detection**: Identify potentially problematic branch conditions that cause thread divergence
- **Data Type Analysis**: Track usage of data types throughout the kernel
- **Vector Operation Analysis**: Detect and evaluate vector operations (float4, int2, etc.) for efficiency
- **Expensive Operations Profiling**: Identify computationally costly operations
- **Optimization Recommendations**: Get actionable insights to improve kernel performance

## 📋 Requirements

- Python 3.7+
- PyQt5
- matplotlib
- numpy

## 🔧 Installation

### From PyPI (Recommended)

```bash
pip install kernel-analyzer
```

### From Source

```bash
git clone https://github.com/your-organization/kernel-analyzer.git
cd kernel-analyzer
pip install -e .
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

## 🖥️ Usage

### Qt GUI Application

Run the Qt GUI for a visual interface:

```bash
# Use the wrapper script
./kernel_analyzer_gui.py

# Or through the package entry point
kernel-analyzer-gui
```

1. Select a kernel file using File > Open
2. Choose the appropriate file type (OpenCL, CUDA, etc.)
3. Click "Analyze" to perform the analysis
4. View results in the tabbed interface
5. Export results if needed

### Command Line Interface

Analyze a kernel from the command line:

```bash
# Use the wrapper script
./kernel_analyzer.py test_kernels/example.cl

# Or through the package entry point
kernel-analyzer test_kernels/example.cl
```

### Debug and Test Tools

For detailed analysis:

```bash
./scripts/debug_data_format.py test_kernels/example.cl
```

For GUI testing with pre-analyzed data:

```bash
./scripts/test_gui_with_data.py test_kernels/analysis/example_analysis.json test_kernels/example.cl
```

For testing widgets individually:

```bash
./scripts/test_branch_widget.py
```

## 📁 Project Structure

See [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) for a detailed explanation of the project's organization.

Key directories:
- `kernel_analyzer/` - Core package with analysis functionality
- `scripts/` - Utility scripts and tools
- `test_kernels/` - Example kernels and analysis results
- `docs/` - Documentation
- `tests/` - Unit tests

## 🔍 Understanding the Analysis

### Branch Divergence

The tool detects when different threads within a warp/wavefront might take different execution paths, causing performance degradation:

- Branch points in the kernel (if/else statements)
- Nesting depth of branches
- Thread-dependent conditions (using get_global_id, etc.)
- Overall divergence risk assessment

### Data Type Analysis

Tracks data types used throughout the kernel:

- Most frequently used data types
- Vector types (float4, int2, etc.)
- Memory space qualifiers (__global, __local, etc.)

### Vector Operations

Analyzes vector operations which are crucial for GPU performance:

- Vector data types (float4, int2, etc.)
- Vector load/store operations (vload, vstore)
- Vector component access (v.x, v.s0, etc.)
- Fused multiply-add operations (FMA)

### Expensive Operations

Identifies operations known to be costly on GPUs:

- Categories: Moderately Expensive, Expensive, Very Expensive
- Division, modulo, transcendental functions, etc.
- Impact on overall performance

## 📊 Example Output

```
==================================================
KERNEL ANALYSIS REPORT: matmulUnroll4WithResidual
==================================================

PERFORMANCE METRICS:
------------------------------
Total Reads:       11
Total Writes:      1
Compute Ops:       49
Arithmetic Intensity: 4.0833

BOTTLENECK ANALYSIS:
------------------------------
Primary Bottleneck: COMPUTE
Memory Bound Score: 0.2449
Compute Bound Score: 0.7551

BRANCH DIVERGENCE ANALYSIS:
------------------------------
Total Branch Points: 0
Max Branch Depth: 0
Divergence Risk: None

DATA TYPE ANALYSIS:
------------------------------
Major Types:
  • float: 9 occurrences
  • __global: 15 occurrences
  • long: 8 occurrences
  • float4: 1 occurrences

EXPENSIVE OPERATIONS:
------------------------------
Expensive Operations:
  • division: 10 occurrences
  • bit_shifts: 16 occurrences

OPTIMIZATION RECOMMENDATIONS:
------------------------------
1. Consider expanding use of vector types to more arrays for better memory coalescing
2. Consider pre-computing reciprocals instead of using division operations
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m "not slow"
pytest -m "not gui"
```

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to the project.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Documentation

For more detailed information, see the [documentation](docs/README.md). 
