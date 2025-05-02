# Branch Analysis Usage Guide

This guide explains how to use the branch divergence, data type, and expensive operations analysis features in the Kernel Analyzer.

## Running the Analysis from the Command Line

To analyze a kernel using the CLI:

```bash
# Basic analysis - shows all information including branch divergence
python -m kernel_analyzer.cli.analyzer_cli path/to/your/kernel.cl

# Save the result to a file
python -m kernel_analyzer.cli.analyzer_cli path/to/your/kernel.cl -o results.txt

# Get JSON output for further processing
python -m kernel_analyzer.cli.analyzer_cli path/to/your/kernel.cl --format json > result.json
```

## Using the GUI for Analysis

### Qt-Based GUI (Recommended on Linux)

```bash
# Launch the Qt GUI
./kernel_analyzer_gui.py
```

1. Click "Open Kernel" to select your kernel file
2. Ensure the correct file type is selected in the dropdown
3. Click "Analyze Kernel" to perform the analysis
4. Navigate to the different tabs to view the results:
   - **Branch Divergence**: Shows branch points and divergence risk
   - **Data Types**: Lists all data types used in the kernel
   - **Expensive Operations**: Shows operations that may impact performance
   - **Recommendations**: Lists optimization suggestions

### Interpreting Branch Divergence Results

The branch divergence tab shows:

- **Total Branch Points**: The number of if/else statements in the code
- **Max Branch Depth**: The maximum nesting level of branching
- **Divergence Risk**: Overall risk assessment (Low/Medium/High)
- **Branch Locations**: Details of where branches occur, including:
  - Line number
  - Branch type (if, switch, etc.)
  - Risk level
  - Whether it's in a loop (higher risk)
  - Whether it depends on thread ID (highest risk)

### Interpreting Data Type Results

The data types tab shows:

- All data types used in the kernel
- The frequency of each type
- This helps identify potential type conversion issues or opportunities for using more efficient types

### Interpreting Expensive Operations Results

The expensive operations tab shows:

- **Moderately Expensive Operations**: Operations with moderate performance impact
- **Expensive Operations**: Operations with significant performance impact
- **Very Expensive Operations**: Operations with severe performance impact
- **Summary**: Total count of expensive operations

## Understanding Branch Divergence in GPU Programming

Branch divergence occurs when threads in the same warp/wavefront take different execution paths. When this happens, the GPU must execute all paths serially, significantly reducing parallelism and performance.

### Risk Factors

- **Thread-Dependent Branches**: Branches that depend on thread IDs are most likely to cause divergence
- **Branches in Loops**: Divergence in loops has a multiplied performance impact
- **Nested Branches**: Deeply nested branches increase divergence complexity
- **Branches in Critical Sections**: Divergence in performance-critical code has greater impact

### Optimization Strategies

Based on branch analysis, consider these optimization techniques:

1. **Predication**: Use arithmetic instead of branching for simple conditions
2. **Branch Flattening**: Reduce nesting depth
3. **Loop Restructuring**: Move branches outside of loops when possible
4. **Warp-Aware Programming**: Organize work to minimize divergence within warps

## Example

```c
// Before optimization (high divergence risk)
if (threadIdx.x % 2 == 0) {
    for (int i = 0; i < n; i++) {
        result[i] = a[i] + b[i];
    }
} else {
    for (int i = 0; i < n; i++) {
        result[i] = a[i] * b[i];
    }
}

// After optimization (lower divergence risk)
for (int i = 0; i < n; i++) {
    result[i] = (threadIdx.x % 2 == 0) ? a[i] + b[i] : a[i] * b[i];
}
``` 