from typing import Dict, List, Any
from kernel_analyzer.core.kernel import Kernel, KernelMetrics

class BottleneckAnalyzer:
    """
    Analyzes kernels to identify performance bottlenecks.
    """

    @staticmethod
    def analyze(kernel: Kernel) -> Dict[str, Any]:
        """
        Analyze a kernel and provide detailed bottleneck information.
        
        Args:
            kernel: The parsed kernel to analyze
            
        Returns:
            Dictionary with bottleneck analysis and recommendations
        """
        # Ensure metrics are calculated
        metrics = kernel.calculate_metrics()
        
        # Get bottleneck type
        bottleneck_type = metrics.bottleneck
        recommendations = []
        
        if bottleneck_type == "memory":
            recommendations = BottleneckAnalyzer._get_memory_recommendations(kernel, metrics)
        else:  # compute bound
            recommendations = BottleneckAnalyzer._get_compute_recommendations(kernel, metrics)
            
        return {
            "bottleneck_type": bottleneck_type,
            "memory_bound_score": metrics.memory_bound_score,
            "compute_bound_score": metrics.compute_bound_score,
            "arithmetic_intensity": metrics.arithmetic_intensity,
            "recommendations": recommendations
        }
    
    @staticmethod
    def _get_memory_recommendations(kernel: Kernel, metrics: KernelMetrics) -> List[str]:
        """Generate recommendations for memory-bound kernels"""
        recommendations = []
        
        # Check global memory access patterns
        if metrics.total_reads + metrics.total_writes > 0:
            recommendations.append(
                "Consider using local memory for frequently accessed data"
            )
            recommendations.append(
                "Check for memory coalescing to improve memory bandwidth utilization"
            )
            recommendations.append(
                "Consider using vector data types to reduce memory access instructions"
            )
        
        # Check if we have a high ratio of reads to writes
        if metrics.total_reads > 3 * metrics.total_writes:
            recommendations.append(
                "High read-to-write ratio: consider caching frequently read values"
            )
            
        return recommendations
            
    @staticmethod
    def _get_compute_recommendations(kernel: Kernel, metrics: KernelMetrics) -> List[str]:
        """Generate recommendations for compute-bound kernels"""
        recommendations = []
        
        if metrics.total_compute_ops > 0:
            recommendations.append(
                "Consider using built-in math functions for better performance"
            )
            recommendations.append(
                "Look for opportunities to use vector operations or SIMD instructions"
            )
            recommendations.append(
                "Check for loop unrolling opportunities to increase instruction-level parallelism"
            )
            
        return recommendations 