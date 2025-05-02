from abc import ABC, abstractmethod
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class MemoryOperation:
    address: str  # Address or variable name
    is_read: bool  # True for read, False for write
    data_type: str  # Type of data being accessed (float, int, etc.)
    size: int  # Size in bytes
    location: str  # Global, local, private memory
    line_number: int  # Line number in the source code

@dataclass
class ComputeOperation:
    operation_type: str  # add, mul, etc.
    data_type: str  # Type of data being operated on
    line_number: int  # Line number in the source code

@dataclass
class KernelMetrics:
    total_reads: int = 0
    total_writes: int = 0
    total_compute_ops: int = 0
    arithmetic_intensity: float = 0.0  # Compute ops per memory operation
    memory_bound_score: float = 0.0  # Closer to 1 = more memory bound
    compute_bound_score: float = 0.0  # Closer to 1 = more compute bound
    bottleneck: str = ""  # "memory" or "compute"

class Kernel(ABC):
    def __init__(self, source_code: str, name: str = None):
        self.source_code = source_code
        self.name = name
        self.lines = source_code.splitlines()
        self.memory_operations: List[MemoryOperation] = []
        self.compute_operations: List[ComputeOperation] = []
        self.metrics: KernelMetrics = KernelMetrics()
        
    @abstractmethod
    def parse(self) -> None:
        """Parse the kernel code to identify memory and compute operations"""
        pass
        
    def calculate_metrics(self) -> KernelMetrics:
        """Calculate performance metrics based on parsed operations"""
        # Count operations
        reads = len([op for op in self.memory_operations if op.is_read])
        writes = len([op for op in self.memory_operations if not op.is_read])
        compute_ops = len(self.compute_operations)
        
        # Update metrics
        self.metrics.total_reads = reads
        self.metrics.total_writes = writes
        self.metrics.total_compute_ops = compute_ops
        
        # Calculate arithmetic intensity (compute ops per memory access)
        total_memory_ops = reads + writes
        if total_memory_ops > 0:
            self.metrics.arithmetic_intensity = compute_ops / total_memory_ops
        
        # Determine if kernel is likely memory or compute bound
        # This is a simple heuristic - can be refined with more sophisticated models
        if self.metrics.arithmetic_intensity < 1.0:
            self.metrics.memory_bound_score = 1.0 - self.metrics.arithmetic_intensity
            self.metrics.compute_bound_score = self.metrics.arithmetic_intensity
            self.metrics.bottleneck = "memory"
        else:
            self.metrics.memory_bound_score = 1.0 / self.metrics.arithmetic_intensity
            self.metrics.compute_bound_score = 1.0 - self.metrics.memory_bound_score
            self.metrics.bottleneck = "compute"
            
        return self.metrics
    
    def get_summary(self) -> Dict[str, Any]:
        """Return a summary of the kernel analysis"""
        return {
            "name": self.name,
            "metrics": {
                "total_reads": self.metrics.total_reads,
                "total_writes": self.metrics.total_writes,
                "total_compute_ops": self.metrics.total_compute_ops,
                "arithmetic_intensity": self.metrics.arithmetic_intensity,
                "bottleneck": self.metrics.bottleneck,
                "memory_bound_score": self.metrics.memory_bound_score,
                "compute_bound_score": self.metrics.compute_bound_score
            }
        } 