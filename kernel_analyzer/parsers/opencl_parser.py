import re
from typing import List, Tuple, Dict, Optional
from kernel_analyzer.core.kernel import Kernel, MemoryOperation, ComputeOperation

class OpenCLKernel(Kernel):
    """Kernel parser for OpenCL kernels"""
    
    # Memory access patterns for OpenCL
    GLOBAL_MEM_READ_PATTERN = r'\*\(\(__global\s+([a-zA-Z0-9_]+)\s*\*\)\s*(.*?)\)'
    GLOBAL_MEM_WRITE_PATTERN = r'\*\(\(__global\s+([a-zA-Z0-9_]+)\s*\*\)\s*(.*?)\)\s*=\s*(.*?);'
    
    # Compute operation patterns
    ARITHMETIC_PATTERNS = {
        'add': r'([a-zA-Z0-9_]+)\s*\+\s*([a-zA-Z0-9_]+)',
        'sub': r'([a-zA-Z0-9_]+)\s*\-\s*([a-zA-Z0-9_]+)',
        'mul': r'([a-zA-Z0-9_]+)\s*\*\s*([a-zA-Z0-9_]+)',
        'div': r'([a-zA-Z0-9_]+)\s*\/\s*([a-zA-Z0-9_]+)',
        'fma': r'fma\s*\(\s*([a-zA-Z0-9_]+)\s*,\s*([a-zA-Z0-9_]+)\s*,\s*([a-zA-Z0-9_]+)\s*\)',
    }
    
    # Variable declaration patterns
    VARIABLE_PATTERN = r'(float|int|long|ulong|bool)\s+([a-zA-Z0-9_,\s]+);'
    
    # Type size mapping (in bytes)
    TYPE_SIZES = {
        'float': 4,
        'int': 4,
        'long': 8,
        'ulong': 8,
        'bool': 1,
    }
    
    def __init__(self, source_code: str, name: str = None):
        super().__init__(source_code, name)
        self.variable_types: Dict[str, str] = {}  # Maps variable names to their types
        
    def parse(self) -> None:
        """Parse the OpenCL kernel to identify memory and compute operations"""
        # First extract kernel name if not provided
        if not self.name:
            kernel_match = re.search(r'__kernel\s+void\s+([a-zA-Z0-9_]+)', self.source_code)
            self.name = kernel_match.group(1) if kernel_match else "unknown_kernel"
        
        # Extract variable declarations and types
        self._extract_variable_types()
        
        # Process each line to find memory operations and compute operations
        for line_num, line in enumerate(self.lines, 1):
            # Skip pragma and comment lines
            if line.strip().startswith('#pragma') or line.strip().startswith('//'):
                continue
                
            # Find memory operations
            self._extract_memory_operations(line, line_num)
            
            # Find compute operations
            self._extract_compute_operations(line, line_num)
        
        # Calculate performance metrics
        self.calculate_metrics()
            
    def _extract_variable_types(self) -> None:
        """Extract variable declarations and their types"""
        for line in self.lines:
            var_matches = re.findall(self.VARIABLE_PATTERN, line)
            for var_type, var_names in var_matches:
                for var_name in var_names.split(','):
                    var_name = var_name.strip()
                    self.variable_types[var_name] = var_type
    
    def _extract_memory_operations(self, line: str, line_num: int) -> None:
        """Extract memory operations from a line of code"""
        # Extract global memory reads
        read_matches = re.finditer(self.GLOBAL_MEM_READ_PATTERN, line)
        for match in read_matches:
            data_type = match.group(1)
            address = match.group(2)
            size = self.TYPE_SIZES.get(data_type, 4)  # Default to 4 bytes if type unknown
            
            self.memory_operations.append(MemoryOperation(
                address=address,
                is_read=True,
                data_type=data_type,
                size=size,
                location="global",
                line_number=line_num
            ))
        
        # Extract global memory writes
        write_matches = re.finditer(self.GLOBAL_MEM_WRITE_PATTERN, line)
        for match in write_matches:
            data_type = match.group(1)
            address = match.group(2)
            size = self.TYPE_SIZES.get(data_type, 4)  # Default to 4 bytes if type unknown
            
            self.memory_operations.append(MemoryOperation(
                address=address,
                is_read=False,
                data_type=data_type,
                size=size,
                location="global",
                line_number=line_num
            ))
    
    def _extract_compute_operations(self, line: str, line_num: int) -> None:
        """Extract compute operations from a line of code"""
        for op_type, pattern in self.ARITHMETIC_PATTERNS.items():
            matches = re.finditer(pattern, line)
            for match in matches:
                # Determine data type based on operands
                operands = match.groups()
                data_type = self._infer_operation_type(operands)
                
                self.compute_operations.append(ComputeOperation(
                    operation_type=op_type,
                    data_type=data_type,
                    line_number=line_num
                ))
                
                # FMA counts as 2 operations (multiplication and addition)
                if op_type == 'fma':
                    self.compute_operations.append(ComputeOperation(
                        operation_type='add',
                        data_type=data_type,
                        line_number=line_num
                    ))
    
    def _infer_operation_type(self, operands: Tuple[str, ...]) -> str:
        """Infer the data type of an operation based on its operands"""
        for operand in operands:
            operand = operand.strip()
            if operand in self.variable_types:
                return self.variable_types[operand]
                
        # Default to float if we couldn't determine type
        return "float"
        
    def get_detailed_analysis(self) -> Dict:
        """Get a detailed analysis of the kernel"""
        global_mem_reads = sum(1 for op in self.memory_operations if op.is_read and op.location == "global")
        global_mem_writes = sum(1 for op in self.memory_operations if not op.is_read and op.location == "global")
        
        op_counts = {}
        for op in self.compute_operations:
            op_counts[op.operation_type] = op_counts.get(op.operation_type, 0) + 1
            
        return {
            "name": self.name,
            "memory_access": {
                "global_reads": global_mem_reads,
                "global_writes": global_mem_writes,
                "total_global_accesses": global_mem_reads + global_mem_writes,
            },
            "compute_operations": op_counts,
            "arithmetic_intensity": self.metrics.arithmetic_intensity,
            "bottleneck": self.metrics.bottleneck,
            "memory_bound_score": self.metrics.memory_bound_score,
            "compute_bound_score": self.metrics.compute_bound_score
        } 