---
name: optimize
description: Performance optimization mode - analyzes and improves performance, scalability, and resource usage
---

# Optimization Mode

Optimize performance for: $ARGUMENTS

## Optimization Framework

### Analysis Areas
1. **Algorithm Complexity**
   - Time complexity (O(n) analysis)
   - Space complexity
   - Better algorithm alternatives

2. **Database Performance**
   - Query optimization
   - Index analysis
   - N+1 query detection
   - Connection pooling

3. **Async Patterns**
   - Blocking I/O detection
   - Concurrency opportunities
   - Batching potential

4. **Caching**
   - Cache hit ratio
   - Cache invalidation strategy
   - Cache key design

5. **Resource Usage**
   - Memory allocation
   - CPU usage
   - Network calls

### Optimization Process

#### Phase 1: Measure
```python
# Add timing instrumentation
with TimingContext(metrics, "operation_name"):
    result = expensive_operation()

# Profile memory
import tracemalloc
tracemalloc.start()
result = operation()
current, peak = tracemalloc.get_traced_memory()
print(f"Memory: {peak / 10**6:.1f} MB")
```

#### Phase 2: Identify Bottlenecks
- Find slowest operations
- Identify most frequent calls
- Locate memory leaks
- Detect blocking I/O

#### Phase 3: Optimize
```python
# BEFORE: O(n²) nested loops
for user in users:
    for order in orders:
        if order.user_id == user.id:
            process(user, order)

# AFTER: O(n) with hash map
orders_by_user = {}
for order in orders:
    orders_by_user.setdefault(order.user_id, []).append(order)

for user in users:
    for order in orders_by_user.get(user.id, []):
        process(user, order)
```

#### Phase 4: Verify
- Benchmark before/after
- Monitor in production
- A/B test if possible

### Output Format
```markdown
# Performance Optimization Report

## Summary
- **Target**: [What was optimized]
- **Improvement**: [X% faster / Y% less memory]
- **Impact**: [Production implications]

## Bottleneck Analysis

### Bottleneck 1: [Description]
**Current Performance**: X ms / Y operations
**Root Cause**: [Explanation]
**Proposed Fix**: [Solution]
**Expected Improvement**: [Estimated gain]

## Optimizations Applied

### Optimization 1: [Name]
**Before**:
```python
# Slow version
```

**After**:
```python
# Fast version
```

**Benchmark Results**:
- Before: X ms
- After: Y ms
- Improvement: Z% faster

## Recommendations
1. [High priority optimization]
2. [Medium priority]
3. [Low priority / future consideration]
```

### Integration
- Auto-load: `production-patterns` skill (async patterns)
- Use: Profiling tools (cProfile, memory_profiler)
- Use: Benchmarking (timeit, pytest-benchmark)

## Best Practices

✅ **DO**:
- Measure before optimizing (no premature optimization)
- Benchmark improvements
- Document tradeoffs
- Consider maintainability impact
- Test correctness after optimization
- Profile in production-like conditions

❌ **DON'T**:
- Optimize without measuring first
- Sacrifice correctness for speed
- Ignore algorithm complexity
- Forget to benchmark
- Optimize non-bottlenecks
- Skip testing after optimization
