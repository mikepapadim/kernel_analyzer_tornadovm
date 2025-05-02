# Installation Guide

This guide provides detailed instructions for installing the OpenCL Kernel Performance Analyzer on various platforms.

## Prerequisites

Before installing, ensure you have the following:

- Python 3.7 or newer
- pip (Python package installer)
- Git (optional, for cloning the repository)

## Option 1: Installation from PyPI (Recommended)

The simplest way to install is using pip:

```bash
pip install kernel-analyzer
```

For development installation with additional tools:

```bash
pip install kernel-analyzer[dev]
```

## Option 2: Installation from Source

1. Clone the repository:

```bash
git clone https://github.com/your-organization/kernel-analyzer.git
cd kernel-analyzer
```

2. Install the package:

```bash
# For regular installation
pip install .

# For development installation
pip install -e .[dev]
```

## Platform-Specific Notes

### Linux

On some Linux distributions, you may need to install PyQt5 dependencies separately:

```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt5

# Fedora
sudo dnf install python3-qt5
```

### macOS

If you encounter issues with matplotlib or PyQt5, consider using Conda:

```bash
conda create -n kernel-analyzer python=3.9
conda activate kernel-analyzer
pip install kernel-analyzer
```

### Windows

On Windows, ensure you have the Microsoft Visual C++ Build Tools installed if you're installing from source.

## Verifying Installation

To verify the installation:

```bash
# Check CLI tool
kernel-analyzer --version

# Launch GUI
kernel-analyzer-gui
```

## Troubleshooting

If you encounter issues:

1. Ensure all dependencies are installed correctly
2. Check that your Python version is 3.7 or newer
3. For GUI issues, verify PyQt5 is installed properly

If problems persist, please [open an issue](https://github.com/your-organization/kernel-analyzer/issues) with details about your environment and the error messages you're seeing. 