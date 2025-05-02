#!/usr/bin/env python3
"""
Tests for the BranchDivergenceAnalyzer class.

This module contains tests for the branch divergence analyzer, ensuring that
it correctly identifies branch points, data types, and expensive operations in
OpenCL kernels.
"""

import os
import sys
import unittest
from typing import Dict, Any

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kernel_analyzer.parsers.opencl_parser import OpenCLKernel
from kernel_analyzer.analyzers.branch_analyzer import BranchDivergenceAnalyzer


class TestBranchDivergenceAnalyzer(unittest.TestCase):
    """Test cases for the BranchDivergenceAnalyzer class."""

    def setUp(self):
        """Set up test cases."""
        # Simple kernel with branches and vector operations
        self.simple_kernel = """
        __kernel void simple(__global float *output, __global float *input, int n)
        {
            int gid = get_global_id(0);
            if (gid < n) {
                output[gid] = input[gid] * 2.0f;
            }
        }
        """
        
        # Kernel with vector types and operations
        self.vector_kernel = """
        __kernel void vector_ops(__global float *output, __global float *input, int n)
        {
            int gid = get_global_id(0);
            if (gid < n / 4) {
                float4 in_vec = vload4(gid, input);
                float4 result = in_vec * 2.0f;
                vstore4(result, gid, output);
            }
        }
        """
        
        # Complex kernel with nested branches and expensive operations
        self.complex_kernel = """
        __kernel void complex(__global float *output, __global float *input, int n)
        {
            int gid = get_global_id(0);
            if (gid < n) {
                float value = input[gid];
                if (value > 0.0f) {
                    if (value < 1.0f) {
                        output[gid] = value / 2.0f;  // Division (expensive)
                    } else {
                        output[gid] = sqrt(value);  // Very expensive
                    }
                } else {
                    output[gid] = 0.0f;
                }
            }
        }
        """

    def _parse_and_analyze(self, code: str) -> Dict[str, Any]:
        """
        Helper method to parse a kernel and run the branch divergence analyzer.
        
        Args:
            code: OpenCL kernel code string
            
        Returns:
            Analysis results dictionary
        """
        kernel = OpenCLKernel(code)
        kernel.parse()
        analyzer = BranchDivergenceAnalyzer(kernel)
        return analyzer.analyze()

    def test_branch_point_detection(self):
        """Test that branch points are correctly detected."""
        result = self._parse_and_analyze(self.simple_kernel)
        
        # Check branch divergence results
        self.assertIn('branch_divergence', result)
        branch_div = result['branch_divergence']
        
        # Simple kernel should have 1 branch point
        self.assertEqual(branch_div['branch_points'], 1)
        self.assertEqual(len(branch_div['branch_points_detailed']), 1)
        
        # The branch should be thread-dependent (uses get_global_id)
        first_branch = branch_div['branch_points_detailed'][0]
        self.assertTrue(first_branch['thread_dependent'])
        self.assertEqual(first_branch['type'], 'if')

    def test_vector_type_detection(self):
        """Test that vector types and operations are correctly detected."""
        result = self._parse_and_analyze(self.vector_kernel)
        
        # Check data types
        self.assertIn('data_types', result)
        data_types = result['data_types']
        
        # Should detect float4 type
        self.assertIn('float4', data_types)
        self.assertTrue(data_types['float4'] >= 1)
        
        # Should detect vector load/store operations
        self.assertTrue(
            data_types.get('vload4', 0) >= 1 or 
            data_types.get('vector_load', 0) >= 1
        )
        self.assertTrue(
            data_types.get('vstore4', 0) >= 1 or 
            data_types.get('vector_store', 0) >= 1
        )

    def test_expensive_operations_detection(self):
        """Test that expensive operations are correctly detected."""
        result = self._parse_and_analyze(self.complex_kernel)
        
        # Check expensive operations
        self.assertIn('expensive_operations', result)
        exp_ops = result['expensive_operations']
        self.assertIn('operations', exp_ops)
        
        # Should detect division (expensive)
        self.assertIn('Expensive', exp_ops['operations'])
        self.assertIn('division', exp_ops['operations']['Expensive'])
        self.assertTrue(exp_ops['operations']['Expensive']['division'] >= 1)
        
        # Should detect sqrt (very expensive)
        self.assertIn('Very Expensive', exp_ops['operations'])
        self.assertTrue(
            'sqrt' in exp_ops['operations']['Very Expensive'] or
            'transcendental' in exp_ops['operations']['Very Expensive']
        )

    def test_nested_branches_detection(self):
        """Test that nested branches are correctly detected."""
        result = self._parse_and_analyze(self.complex_kernel)
        
        # Check branch nesting
        branch_div = result['branch_divergence']
        self.assertTrue(branch_div['max_branch_depth'] >= 2)
        self.assertTrue(branch_div['nested_branch_count'] >= 1)

    def test_divergence_risk_assessment(self):
        """Test that divergence risk is correctly assessed."""
        # Simple kernel should have medium risk (thread-dependent branch)
        simple_result = self._parse_and_analyze(self.simple_kernel)
        self.assertIn('divergence_risk', simple_result['branch_divergence'])
        simple_risk = simple_result['branch_divergence']['divergence_risk']
        self.assertIn(simple_risk, ['Low', 'Medium'])  # Should be at least Low
        
        # Complex kernel should have higher risk (nested thread-dependent branches)
        complex_result = self._parse_and_analyze(self.complex_kernel)
        complex_risk = complex_result['branch_divergence']['divergence_risk']
        self.assertIn(complex_risk, ['Medium', 'High'])  # Should be at least Medium

    def test_recommendations_generation(self):
        """Test that recommendations are generated based on analysis."""
        # Use complex kernel which has multiple issues to generate recommendations
        kernel = OpenCLKernel(self.complex_kernel)
        kernel.parse()
        analyzer = BranchDivergenceAnalyzer(kernel)
        
        # Analyze and get recommendations
        analyzer.analyze()
        recommendations = analyzer.get_recommendations()
        
        # Should generate at least one recommendation
        self.assertTrue(len(recommendations) > 0)
        
        # Should include recommendation about branches
        has_branch_rec = any('branch' in rec.lower() for rec in recommendations)
        self.assertTrue(has_branch_rec)
        
        # Should include recommendation about expensive operations
        has_expensive_rec = any(
            'division' in rec.lower() or 
            'expensive' in rec.lower() or
            'transcendental' in rec.lower()
            for rec in recommendations
        )
        self.assertTrue(has_expensive_rec)


if __name__ == '__main__':
    unittest.main() 