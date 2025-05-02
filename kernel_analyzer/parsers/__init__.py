from kernel_analyzer.parsers.opencl_parser import OpenCLKernel
from kernel_analyzer.parsers.parser_registry import ParserRegistry

# Register all parsers
ParserRegistry.register_parser(".cl", OpenCLKernel) 