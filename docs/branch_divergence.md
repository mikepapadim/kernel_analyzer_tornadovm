# Branch Divergence Analysis

## Overview

Branch divergence is a critical performance consideration in GPU programming. When different threads within the same warp/wavefront take different execution paths due to conditional statements, the GPU must execute both paths serially, which can significantly degrade performance.

The Kernel Analyzer's branch divergence analyzer identifies potential sources of divergence in your compute kernels and provides recommendations to address them.

## What We Analyze

1. **Branch Points**: Locations in the code where execution can diverge (if, else, switch, ternary operators)
2. **Branch Depth**: How deeply nested conditional statements are
3. **Context Analysis**: Whether branches are inside loops or dependent on thread IDs
4. **Risk Assessment**: Classification of each branch point by its potential performance impact

## Risk Classification

Each branch point is classified according to its potential for causing performance degradation:

- **Low Risk**: Branches that are likely uniform across threads or outside performance-critical regions
- **Medium Risk**: Branches that could cause some divergence, especially if inside loops
- **High Risk**: Branches that are likely to cause significant divergence, such as those dependent on thread IDs within critical loops

## Output Fields

The branch divergence analysis provides the following information:

```json
"branch_divergence": {
  "branch_points": 12,               // Total number of branch points
  "max_branch_depth": 3,             // Maximum nesting depth
  "nested_branch_count": 5,          // Number of nested branches
  "branch_points_detailed": [        // Details for each branch point
    {
      "line": 45,                    // Line number
      "type": "if",                  // Type of branch
      "depth": 1,                    // Nesting depth
      "thread_dependent": false,     // Whether it depends on thread ID
      "in_loop": false,              // Whether it's inside a loop
      "risk": "Low"                  // Risk classification
    },
    // More branch points...
  ],
  "divergence_risk": "Medium"        // Overall risk assessment
}
```

## Optimization Strategies

Based on the analysis, the tool recommends appropriate optimization strategies, which may include:

1. **Branch Elimination**: Removing branches by using arithmetic or bitwise operations
2. **Branch Flattening**: Reducing nesting depth to minimize divergence impact
3. **Predication**: Using predicated execution for short conditional blocks
4. **Warp-Level Synchronization**: Ensuring uniform execution across warps
5. **Loop Restructuring**: Moving conditional statements outside of loops when possible

## Example Optimizations

### Before Optimization

```c
if (threadIdx.x % 2 == 0) {  // High risk - thread dependent in loop
  for (int i = 0; i < n; i++) {
    result[i] = a[i] + b[i];
  }
} else {
  for (int i = 0; i < n; i++) {
    result[i] = a[i] * b[i];
  }
}
```

### After Optimization

```c
// Restructured to minimize divergence
for (int i = 0; i < n; i++) {
  if (threadIdx.x % 2 == 0) {
    result[i] = a[i] + b[i];
  } else {
    result[i] = a[i] * b[i];
  }
}

// Or even better, using predication
bool is_even = (threadIdx.x % 2 == 0);
for (int i = 0; i < n; i++) {
  result[i] = is_even ? a[i] + b[i] : a[i] * b[i];
}
```

## Using the Analysis

To get branch divergence analysis:

1. **CLI**: Run `python -m kernel_analyzer.cli.analyzer_cli your_kernel.cl`
2. **GUI**: Open your kernel in either GUI and navigate to the "Branch Divergence" tab

## Further Reading

- [NVIDIA's Guide to Control Flow](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#control-flow-instructions)
- [AMD's Optimization Guide](https://developer.amd.com/resources/developer-guides-manuals/)
- [Intel's GPU Optimization Guide](https://software.intel.com/content/www/us/en/develop/documentation/oneapi-gpu-optimization-guide/top.html) 