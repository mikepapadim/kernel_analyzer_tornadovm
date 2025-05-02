"""
Kernel Analyzer - A tool for analyzing compute kernels for performance characteristics.

This package provides functionality to:
- Parse various compute kernel formats (OpenCL, CUDA, etc.)
- Analyze memory usage and compute patterns
- Identify potential performance bottlenecks
- Provide optimization recommendations
"""

__version__ = '0.1.0'

from kernel_analyzer.core.kernel import Kernel, MemoryOperation, ComputeOperation, KernelMetrics
from kernel_analyzer.parsers.opencl_parser import OpenCLKernel
from kernel_analyzer.analyzers.bottleneck_analyzer import BottleneckAnalyzer
from kernel_analyzer.utils.visualizer import KernelVisualizer 