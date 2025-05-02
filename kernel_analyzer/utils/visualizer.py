import json
from typing import Dict, Any

class KernelVisualizer:
    """
    Utility to visualize kernel analysis results.
    """

    @staticmethod
    def generate_text_report(analysis: Dict[str, Any]) -> str:
        """
        Generate a text-based report of the kernel analysis.
        
        Args:
            analysis: The analysis results
            
        Returns:
            A formatted text report
        """
        report = []
        
        # Add header
        report.append("=" * 50)
        report.append(f"KERNEL ANALYSIS REPORT: {analysis.get('name', 'Unknown Kernel')}")
        report.append("=" * 50)
        report.append("")
        
        # Add metrics
        metrics = analysis.get('metrics', {})
        report.append("PERFORMANCE METRICS:")
        report.append("-" * 30)
        report.append(f"Total Reads:       {metrics.get('total_reads', 0)}")
        report.append(f"Total Writes:      {metrics.get('total_writes', 0)}")
        report.append(f"Compute Ops:       {metrics.get('total_compute_ops', 0)}")
        report.append(f"Arithmetic Intensity: {metrics.get('arithmetic_intensity', 0):.4f}")
        report.append("")
        
        # Add bottleneck analysis
        bottleneck = metrics.get('bottleneck', 'unknown')
        report.append("BOTTLENECK ANALYSIS:")
        report.append("-" * 30)
        report.append(f"Primary Bottleneck: {bottleneck.upper()}")
        report.append(f"Memory Bound Score: {metrics.get('memory_bound_score', 0):.4f}")
        report.append(f"Compute Bound Score: {metrics.get('compute_bound_score', 0):.4f}")
        report.append("")
        
        # Add branch divergence analysis if available
        if 'branch_divergence' in analysis:
            report.append("BRANCH DIVERGENCE ANALYSIS:")
            report.append("-" * 30)
            branch_div = analysis['branch_divergence']
            report.append(f"Total Branch Points: {branch_div.get('total_branch_points', 0)}")
            report.append(f"Max Branch Depth: {branch_div.get('max_branch_depth', 0)}")
            report.append(f"Divergence Risk: {branch_div.get('divergence_risk', 'Unknown')}")
            
            # Add branch locations if available
            if 'branch_locations' in branch_div and branch_div['branch_locations']:
                report.append("\nBranch Locations:")
                for location in branch_div['branch_locations'][:5]:  # Show top 5
                    report.append(f"  • Line {location['line']}: {location['type']}")
                if len(branch_div['branch_locations']) > 5:
                    report.append(f"  ... and {len(branch_div['branch_locations']) - 5} more")
            report.append("")
        
        # Add data type analysis if available
        if 'data_types' in analysis:
            report.append("DATA TYPE ANALYSIS:")
            report.append("-" * 30)
            types = analysis['data_types']
            
            if 'major_types' in types and types['major_types']:
                report.append("Major Types:")
                for type_name, count in types['major_types'].items():
                    report.append(f"  • {type_name}: {count} occurrences")
            
            if 'minor_types' in types and types['minor_types']:
                report.append("\nMinor Types:")
                for type_name, count in types['minor_types'].items():
                    report.append(f"  • {type_name}: {count} occurrences")
            report.append("")
        
        # Add expensive operations analysis if available
        if 'expensive_operations' in analysis:
            report.append("EXPENSIVE OPERATIONS:")
            report.append("-" * 30)
            exp_ops = analysis['expensive_operations']
            
            if 'operations' in exp_ops:
                for category, ops in exp_ops['operations'].items():
                    if ops:
                        report.append(f"{category} Operations:")
                        for op, count in ops.items():
                            report.append(f"  • {op}: {count} occurrences")
            report.append("")
        
        # Add recommendations if available
        if 'recommendations' in analysis:
            report.append("OPTIMIZATION RECOMMENDATIONS:")
            report.append("-" * 30)
            for i, rec in enumerate(analysis['recommendations'], 1):
                report.append(f"{i}. {rec}")
                
        return "\n".join(report)
    
    @staticmethod
    def to_json(analysis: Dict[str, Any], pretty: bool = True) -> str:
        """
        Convert analysis results to JSON format.
        
        Args:
            analysis: The analysis results
            pretty: Whether to format the JSON with indentation
            
        Returns:
            JSON string
        """
        if pretty:
            return json.dumps(analysis, indent=2)
        return json.dumps(analysis) 