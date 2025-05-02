"""
Branch Divergence and Type Analyzer Module

This module provides the BranchDivergenceAnalyzer class which analyzes OpenCL compute kernels
for branch divergence, data type usage patterns, and computationally expensive operations.
These aspects are critical for optimizing performance on GPU architectures.
"""

from typing import Dict, List, Any, Tuple, Set, Counter as CounterType
from collections import Counter
import re

from kernel_analyzer.core.kernel import Kernel

class BranchDivergenceAnalyzer:
    """
    Analyzer for detecting branch divergence and data type usage in compute kernels.
    
    This class identifies potential performance bottlenecks in GPU code, including:
    - Branch divergence (if/else statements that cause threads to take different paths)
    - Data type usage patterns and vector operations
    - Computationally expensive operations
    
    Attributes:
        kernel (Kernel): The kernel object to be analyzed
        branch_points (list): Collection of branch points found in the kernel
        branch_depth (int): Current branch nesting depth during analysis
        max_branch_depth (int): Maximum branch nesting depth found
        nested_branch_count (int): Count of nested branches (depth > 1)
        datatype_usage (Counter): Counter of data types used in the kernel
        expensive_ops (Counter): Counter of expensive operations found
    """

    def __init__(self, kernel: Kernel):
        """
        Initialize the BranchDivergenceAnalyzer.
        
        Args:
            kernel (Kernel): The parsed kernel object to analyze
        """
        self.kernel = kernel
        self.branch_points = []
        self.branch_depth = 0
        self.max_branch_depth = 0
        self.nested_branch_count = 0
        self.datatype_usage = Counter()
        self.expensive_ops = Counter()
        
    def analyze(self) -> Dict[str, Any]:
        """
        Analyze the kernel for branch divergence and data type usage.
        
        This method performs a comprehensive analysis of the kernel code, identifying:
        1. Branch points and their potential for causing thread divergence
        2. Data types used throughout the kernel, including vector types
        3. Computationally expensive operations that may impact performance
        
        Returns:
            Dict[str, Any]: A dictionary containing detailed analysis results with the following structure:
                {
                    "branch_divergence": {
                        "branch_points": int,
                        "max_branch_depth": int,
                        "nested_branch_count": int,
                        "branch_points_detailed": List[Dict],
                        "divergence_risk": str
                    },
                    "data_types": Dict[str, int],
                    "expensive_operations": {
                        "operations": Dict[str, Dict[str, int]],
                        "summary": str
                    }
                }
        """
        # Handle empty or invalid kernels
        if not hasattr(self.kernel, 'lines') or not self.kernel.lines:
            return {
                "branch_divergence": {
                    "branch_points": 0,
                    "max_branch_depth": 0,
                    "nested_branch_count": 0,
                    "divergence_risk": "Low"
                },
                "data_types": {},
                "expensive_operations": {
                    "operations": {}
                }
            }
        
        # Perform the core analysis steps
        self._analyze_branch_divergence()
        self._analyze_data_types()
        self._analyze_expensive_operations()
        
        # Calculate overall divergence risk based on analysis results
        divergence_risk = self._calculate_divergence_risk()
        
        # Organize expensive operations by category for better readability
        operations = self._categorize_expensive_operations()
        
        # Calculate total expensive operations for summary
        total_expensive = sum(self.expensive_ops.values())
        
        # Build and return the complete analysis results dictionary
        return {
            "branch_divergence": {
                "branch_points": len(self.branch_points),
                "max_branch_depth": self.max_branch_depth,
                "nested_branch_count": self.nested_branch_count,
                "branch_points_detailed": self.branch_points,
                "divergence_risk": divergence_risk
            },
            "data_types": dict(self.datatype_usage),
            "expensive_operations": {
                "operations": operations,
                "summary": f"Kernel contains {total_expensive} expensive operations that may impact performance"
            }
        }
    
    def _categorize_expensive_operations(self) -> Dict[str, Dict[str, int]]:
        """
        Categorize expensive operations by their performance impact level.
        
        Returns:
            Dict[str, Dict[str, int]]: Operations organized by category
        """
        # Initialize result containers
        operations = {}
        moderate_ops = {}
        expensive_ops = {}
        very_expensive_ops = {}
        
        # Map operation types to their categories
        op_categories = {
            "Moderately Expensive": ["int_mul", "bit_shifts", "atomic_read"],
            "Expensive": ["division", "modulo", "integer_division"],
            "Very Expensive": ["sqrt", "rsqrt", "pow", "exp", "log", "sin_cos", 
                             "barrier", "atomic_write", "transcendental"]
        }
        
        # Build category dictionaries
        for category, op_types in op_categories.items():
            category_ops = {}
            for op in op_types:
                if op in self.expensive_ops and self.expensive_ops[op] > 0:
                    category_ops[op] = self.expensive_ops[op]
            
            if category_ops:
                operations[category] = category_ops
        
        return operations
    
    def _analyze_branch_divergence(self) -> None:
        """
        Analyze the kernel code for branch divergence.
        
        This method identifies branch points (if/else statements) and evaluates
        their potential impact on thread divergence, which can significantly 
        impact performance on GPU architectures.
        """
        # Reset analysis state
        self.branch_points = []
        self.branch_depth = 0
        self.max_branch_depth = 0
        self.nested_branch_count = 0
        
        in_loop = False
        loop_depths = []
        
        # Process each line of code to identify and analyze branches
        for line_num, line in enumerate(self.kernel.lines, 1):
            line = line.strip()
            
            # Detect if/else branches
            if re.search(r'\bif\s*\(', line):
                self.branch_depth += 1
                self.max_branch_depth = max(self.max_branch_depth, self.branch_depth)
                
                # Check if the branch condition involves thread ID - these are more likely
                # to cause divergence as different threads may take different paths
                has_thread_id = bool(re.search(r'get_(local|global)_id|get_(local|global)_size|threadIdx|blockIdx', line))
                
                # Create a detailed record of this branch point
                branch_point = {
                    "line": line_num,
                    "type": "if",
                    "depth": self.branch_depth,
                    "thread_dependent": has_thread_id,
                    "in_loop": in_loop
                }
                
                # Assess the risk level of this branch point
                if in_loop and has_thread_id:
                    branch_point["risk"] = "High"  # Thread-dependent branches in loops are highest risk
                elif has_thread_id:
                    branch_point["risk"] = "Medium"  # Thread-dependent branches outside loops
                elif in_loop:
                    branch_point["risk"] = "Medium"  # Any branch in a loop has medium risk
                else:
                    branch_point["risk"] = "Low"  # Other branches have low risk
                
                self.branch_points.append(branch_point)
                
                # Count nested branches (depth > 1)
                if self.branch_depth > 1:
                    self.nested_branch_count += 1
                    
            # Detect loops, which affect branch risk assessment
            elif re.search(r'\bfor\s*\(', line) or re.search(r'\bwhile\s*\(', line):
                in_loop = True
                loop_depths.append(self.branch_depth)
                
            # Detect end of blocks (track nesting depth)
            elif line.startswith('}'):
                # Check if we're exiting a loop
                if in_loop and loop_depths and self.branch_depth == loop_depths[-1]:
                    in_loop = False
                    loop_depths.pop()
                    
                # Decrease branch depth when exiting a branch block
                if self.branch_depth > 0:
                    self.branch_depth -= 1
    
    def _analyze_data_types(self) -> None:
        """
        Analyze the kernel code for data type usage.
        
        This method identifies all data types used in the kernel, including basic types,
        vector types, and memory space qualifiers. Vector type usage is particularly 
        important for optimizing GPU performance.
        """
        # Reset counter
        self.datatype_usage = Counter()
        
        # Define regex patterns for data type detection
        
        # Pattern for basic data types (float, int, etc.)
        type_pattern = r'\b(float|double|int|char|uint|uchar|long|ulong|short|ushort|bool|half)(\d*)\b'
        
        # Pattern for memory space qualifiers (__global, __local, etc.)
        memory_space_pattern = r'\b(__global|__local|__private|__constant)\b'
        
        # Enhanced pattern for vector types (float4, int2, etc.)
        # Captures declarations like "float4 v4f_52;"
        vector_pattern = r'\b(float|int|uint|char|uchar|long|ulong|short|ushort)(\d+)\b'
        
        # Pattern for vector component access (v.x, v.s0, etc.)
        vector_access_pattern = r'(\w+)\.(s[0-9]|x|y|z|w|lo|hi)'
        
        # Pattern for vector-specific operations (vload, vstore, etc.)
        vector_ops_pattern = r'\b(vload\d+|vstore\d+|vec_type_hint)\b'
        
        # Process each line to identify data types
        for line in self.kernel.lines:
            # Count basic types
            for match in re.finditer(type_pattern, line):
                base_type = match.group(1)
                self.datatype_usage[base_type] += 1
                
            # Count vector types (float4, int2, etc.)
            for match in re.finditer(vector_pattern, line):
                vector_type = f"{match.group(1)}{match.group(2)}"
                self.datatype_usage[vector_type] += 1
                
            # Count memory space qualifiers
            for match in re.finditer(memory_space_pattern, line):
                mem_space = match.group(1)
                self.datatype_usage[mem_space] += 1
                
            # Count vector access operations
            for match in re.finditer(vector_access_pattern, line):
                # Count vector component access as vector usage
                self.datatype_usage["vector_access"] += 1
                
            # Count vector-specific operations
            for match in re.finditer(vector_ops_pattern, line):
                op_name = match.group(1)
                self.datatype_usage[op_name] += 1
    
    def _analyze_expensive_operations(self) -> None:
        """
        Analyze the kernel code for computationally expensive operations.
        
        This method identifies operations that are known to be expensive on GPU architectures,
        such as division, transcendental functions, and synchronization barriers. It also
        tracks efficient vector operations.
        """
        # Reset counter
        self.expensive_ops = Counter()
        
        # Define patterns for different categories of operations
        
        # Moderately expensive operations
        moderate_patterns = {
            "int_mul": r'\b(mul24|mad24)\b',
            "bit_shifts": r'(<<|>>)',
            "atomic_read": r'\batomic_(add|or|xor|and|min|max)\b'
        }
        
        # Expensive operations
        expensive_patterns = {
            "division": r'(\s|^|\()(\/|\bdiv\b)',
            "modulo": r'(\s|^|\()(%|\bmod\b)',
            "integer_division": r'\b(idiv|udiv)\b',
        }
        
        # Very expensive operations
        very_expensive_patterns = {
            "sqrt": r'\bsqrt\b',
            "rsqrt": r'\brsqrt\b',
            "pow": r'\bpow\b',
            "exp": r'\bexp\b',
            "log": r'\blog\b',
            "sin_cos": r'\b(sin|cos|tan)\b',
            "barrier": r'\b(barrier|mem_fence)\b',
            "atomic_write": r'\batomic_(xchg|cmpxchg)\b',
            "transcendental": r'\b(exp|log|pow|sqrt|sin|cos|tan|asin|acos|atan|sinh|cosh|tanh)\b'
        }
        
        # Vector operations - these are generally efficient on GPUs
        vector_patterns = {
            "vector_load": r'\bvload\d+\b',
            "vector_store": r'\bvstore\d+\b',
            "fma": r'\bfma\b'   # Fused multiply-add is very efficient on most GPUs
        }
        
        # Process each line to count expensive operations
        for line in self.kernel.lines:
            # Check for moderately expensive operations
            for op_name, pattern in moderate_patterns.items():
                if re.search(pattern, line):
                    self.expensive_ops[op_name] += 1
            
            # Check for expensive operations
            for op_name, pattern in expensive_patterns.items():
                if re.search(pattern, line):
                    self.expensive_ops[op_name] += 1
                
            # Check for very expensive operations
            for op_name, pattern in very_expensive_patterns.items():
                if re.search(pattern, line):
                    self.expensive_ops[op_name] += 1
                    
            # Track vector operations (these are efficient, not counted as expensive)
            for op_name, pattern in vector_patterns.items():
                matches = re.findall(pattern, line)
                if matches:
                    self.datatype_usage[op_name] += len(matches)
    
    def _calculate_divergence_risk(self) -> str:
        """
        Calculate the overall branch divergence risk level for the kernel.
        
        This evaluates the severity of potential performance impacts from branch divergence
        based on the number, depth, and context of branch points.
        
        Returns:
            str: Risk level as "None", "Low", "Medium", or "High"
        """
        # Count high-risk branches (those marked as "High" risk)
        high_risk_count = sum(1 for bp in self.branch_points if bp.get("risk") == "High")
        
        # Calculate risk level based on multiple factors
        if self.max_branch_depth > 3 and high_risk_count > 0:
            return "High"  # Deep nesting with high-risk branches
        elif self.max_branch_depth > 2 or high_risk_count > 0 or self.nested_branch_count > 3:
            return "Medium"  # Moderate nesting or some high-risk branches
        elif len(self.branch_points) > 0:
            return "Low"  # Some branches but not deeply nested or high-risk
        else:
            return "None"  # No branches detected
    
    def get_recommendations(self) -> List[str]:
        """
        Generate optimization recommendations based on the analysis results.
        
        This method provides actionable insights to improve kernel performance by
        addressing branch divergence, data type usage, and expensive operations.
        
        Returns:
            List[str]: A list of recommendation strings
        """
        recommendations = []
        
        # Branch divergence recommendations
        if self.max_branch_depth > 3:
            recommendations.append(
                "High branch nesting depth detected. Consider refactoring to reduce branch complexity."
            )
            
        high_risk_branches = [bp for bp in self.branch_points if bp.get("risk") == "High"]
        if high_risk_branches:
            recommendations.append(
                "Thread-dependent branches inside loops detected. This can cause severe warp divergence."
            )
            
        if self.nested_branch_count > 3:
            recommendations.append(
                "Multiple nested branches detected. Consider flattening control flow where possible."
            )
            
        # Data type recommendations
        if self.datatype_usage.get('double', 0) > 0:
            recommendations.append(
                "Double precision floating point operations detected. Consider using single precision "
                "for better performance when precision requirements allow."
            )
            
        # Vector type recommendations
        has_scalar_float = self.datatype_usage.get('float', 0) > 5
        has_vector_types = any(vt in self.datatype_usage for vt in ['float2', 'float4', 'float8', 'float16'])
        has_vector_ops = self.datatype_usage.get('vector_access', 0) > 0 or self.datatype_usage.get('vload4', 0) > 0
            
        if has_scalar_float and not has_vector_types and not has_vector_ops:
            # Kernel uses floats but no vector types - recommend vectorization
            recommendations.append(
                "Consider using vector types (float2, float4) to improve memory throughput and computational efficiency."
            )
        elif has_scalar_float and has_vector_types:
            # Kernel uses both scalar and vector types - check if vectors could be used more extensively
            vector_usage = sum(self.datatype_usage.get(vt, 0) for vt in ['float2', 'float4', 'float8', 'float16'])
            if self.datatype_usage.get('float', 0) > vector_usage * 4:
                recommendations.append(
                    "Consider expanding use of vector types to more arrays for better memory coalescing."
                )
                
        # FMA operation recommendations
        if self.datatype_usage.get('fma', 0) > 0:
            # If fma is already being used, this is good practice
            pass
        elif self.datatype_usage.get('float', 0) > 10:
            recommendations.append(
                "Consider using fused multiply-add (fma) operations for better arithmetic throughput."
            )
            
        # Expensive operations recommendations
        if self.expensive_ops.get('division', 0) > 5:
            recommendations.append(
                "Multiple division operations detected. Consider pre-computing reciprocals when possible."
            )
            
        if self.expensive_ops.get('transcendental', 0) > 0:
            recommendations.append(
                "Transcendental functions (sin, cos, exp, log) are expensive. "
                "Consider lookup tables or polynomial approximations for performance-critical code."
            )
            
        if self.expensive_ops.get('barrier', 0) > 3:
            recommendations.append(
                "Multiple synchronization barriers detected. Minimize synchronization points to improve parallelism."
            )
            
        return recommendations 