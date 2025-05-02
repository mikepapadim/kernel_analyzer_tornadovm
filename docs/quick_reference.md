# OpenCL Kernel Analyzer Quick Reference Card

## Analysis Results at a Glance

| Metric Category | What to Look For | Common Issues | Quick Fixes |
|----------------|------------------|---------------|-------------|
| **Branch Divergence** | ↑ branch points<br>↑ max depth<br>↑ divergence risk | Thread divergence slowing execution | Use `select()` instead of if-else<br>Move conditionals outside of kernels<br>Make branches work-group uniform |
| **Data Types** | Many different types<br>Double precision | Type conversion overhead<br>Slow double precision ops | Standardize on float/int32<br>Use float instead of double<br>Use appropriate vector types |
| **Vector Operations** | Low vector usage | Underutilized SIMD units | Use explicit vector types (float4)<br>Use vector load/store (vload/vstore)<br>Reorganize data for vectorization |
| **Expensive Operations** | Division<br>Modulo<br>Transcendental functions | High cycle count operations | Replace division with multiplication by reciprocal<br>Use bitwise ops for powers of 2<br>Use native_* functions |
| **Memory Access** | Non-coalesced reads/writes<br>Bank conflicts | Memory bandwidth bottleneck | Ensure sequential access patterns<br>Use local memory effectively<br>Avoid strided access |
| **Arithmetic Intensity** | < 1.0 | Memory-bound kernel | Increase compute per memory op<br>Use local memory caching<br>Reduce redundant memory access |
| **Compute Efficiency** | Low op/byte ratio | Inefficient compute | Fuse operations (use mad/fma)<br>Unroll loops<br>Reduce control flow |

## Quick Decision Guide

### Memory or Compute Bound?

- **Memory Bound** (Arithmetic Intensity < 1.0)
  - Focus on: Memory access patterns, data locality, reducing memory traffic
  - Key metrics: Memory efficiency, coalescing, bank conflicts

- **Compute Bound** (Arithmetic Intensity > 1.0)
  - Focus on: Instruction optimization, vector operations, avoiding expensive ops
  - Key metrics: SIMD efficiency, operation counts, branch divergence

### Branch Divergence Risk Levels

- **Low Risk** (0-2): No significant impact
- **Medium Risk** (3-5): Consider optimizing frequently executed branches
- **High Risk** (6+): Critical issue - prioritize branch optimization

### Expensive Operations Priority

1. **Very Expensive** (div, mod, pow): Highest priority to replace
2. **Expensive** (log, exp, sqrt): High priority to optimize
3. **Moderately Expensive** (sin, cos, tan): Optimize if frequently used

## Common Optimizations by Problem Type

### Memory Bandwidth Limited

```c
// Before: Non-coalesced
for (int i = 0; i < N; i++) {
    result[get_global_id(0)] += input[i * get_global_size(0) + get_global_id(0)];
}

// After: Coalesced
for (int i = 0; i < N; i++) {
    result[get_global_id(0)] += input[get_global_id(0) * N + i];
}
```

### Compute Limited

```c
// Before: Scalar operations
float a = data_a[gid];
float b = data_b[gid];
float c = data_c[gid];
float d = data_d[gid];
result[gid] = a + b + c + d;

// After: Vector operations
float4 vec = vload4(gid/4, data);
float4 sum_vec = vec.x + vec.y + vec.z + vec.w;
vstore4(sum_vec, gid/4, result);
```

### Branch Heavy

```c
// Before: Branching
if (x < threshold) {
    result = value_a;
} else {
    result = value_b;
}

// After: Branch-free
result = select(value_b, value_a, x < threshold);
```

## Common Performance Patterns

| Pattern | Characteristics | Solution Approach |
|---------|-----------------|-------------------|
| Memory Wall | High memory ops<br>Low arithmetic intensity | Local memory caching<br>Data reuse<br>Reduce precision |
| Thread Divergence | Many branches<br>High divergence risk | Branch elimination<br>Branch uniformity<br>Kernel splitting |
| Instruction Bottleneck | Expensive operations<br>Low vectorization | Replace costly ops<br>Increase vectorization<br>Operation fusion |
| Resource Contention | High register usage<br>High local memory usage | Reduce variables<br>Optimize work-group size<br>Split kernels |
| Work Imbalance | Varied execution paths<br>Non-uniform work distribution | Uniform work distribution<br>Dynamic workload balancing |

## Key Commands & Quick Actions

| When You See | Quick Action |
|--------------|--------------|
| High branch divergence | `grep -r "if\|for\|while" --include="*.cl" .` to find branches |
| Low vector usage | `grep -r "float[2-8]\|double[2-8]" --include="*.cl" .` to check vector usage |
| Memory access issues | Check array indexing with `[get_global_id(0)]` vs `[get_global_id(0) * stride]` |
| Expensive operations | Search for `/ % pow sin cos exp log sqrt` and replace with faster alternatives |
| Optimization validation | Re-run analyzer after each major change to measure improvement |

## Interpretation Examples

```
Branch Divergence Risk: HIGH (8)
→ Significant thread divergence detected, prioritize branch optimization

Data Types: float (23), double (7), int (12)
→ Consider replacing double with float where precision allows

Expensive Operations: div (14), sqrt (5), log (2)
→ Replace divisions with multiplication by reciprocal

Arithmetic Intensity: 0.4 operations per byte
→ Memory-bound kernel, focus on memory access patterns
```

## Next Steps After Analysis

1. Address highest-risk issues first (based on analysis results)
2. Apply targeted optimizations (see "Common Optimizations")
3. Re-analyze kernel after changes to measure improvement
4. Iterate optimization process until performance goals are met
5. Validate correctness of optimized kernel against reference implementation 