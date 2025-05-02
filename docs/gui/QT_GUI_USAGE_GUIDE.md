# Kernel Analyzer Qt GUI Usage Guide

## Overview

The Kernel Analyzer Qt GUI provides a stable, user-friendly interface for analyzing compute kernels without the matplotlib dependency that can cause segmentation faults in some environments.

## Getting Started

Launch the application:
```bash
./kernel_analyzer_gui.py
```

The GUI will open with a split view: 
- Left panel: Code editor for viewing kernel code
- Right panel: Analysis results display with progress bar visualizations

## Analyzing a Kernel

Follow these steps to analyze a kernel:

1. Click the **Open Kernel** button in the toolbar.
2. Browse and select an OpenCL kernel file (*.cl) or other supported formats.
3. The kernel code will be loaded into the code editor panel.
4. Verify the correct file type is selected in the dropdown (e.g., .cl for OpenCL).
5. Click the **Analyze Kernel** button.
6. The analysis results will appear in the right panel, including:
   - Summary information (kernel name, bottleneck type, arithmetic intensity)
   - Operation statistics (read/write operations, compute operations)
   - Visual progress bar charts showing operation distribution and bottleneck analysis
   - Optimization recommendations

## Exporting Results

To save the analysis results:

1. Click the **Export Results** button.
2. Choose a location and format (JSON or text).
3. Click Save.

## Understanding the Analysis Results

### Summary Section
- **Kernel Name**: The name of the analyzed kernel
- **Primary Bottleneck**: Whether the kernel is MEMORY or COMPUTE bound
- **Arithmetic Intensity**: The ratio of compute operations to memory operations

### Operation Statistics
- **Total Reads**: Number of memory read operations
- **Total Writes**: Number of memory write operations  
- **Compute Operations**: Number of arithmetic operations (add, mul, etc.)
- **Memory/Compute Bound Score**: Scores between 0-1 indicating how memory or compute bound the kernel is

### Visual Charts
- **Operation Types**: Shows the percentage breakdown of compute vs memory operations
- **Bottleneck Analysis**: Shows the relative memory-bound vs compute-bound scores

### Optimization Recommendations
Customized suggestions based on the detected bottleneck to improve kernel performance.

## Troubleshooting

- The Qt-only version should be more stable than the matplotlib version.
- Currently, only OpenCL (.cl) files are fully supported. PTX and SPIRV support is planned for future releases.
- Make sure the kernel code is syntactically correct.

## Differences from the Matplotlib Version

The Qt-only version:
- Uses progress bars instead of pie/bar charts for visualization
- Has a more stable interface without matplotlib dependencies
- Shows the same analysis results but with a different visual style
- Should avoid segmentation faults on systems where Qt and matplotlib integration is problematic 