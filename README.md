# lowest_common_ancestor

Preprocess a rooted tree to answer lowest common ancestor (LCA) queries in constant time.

```python
from lowest_common_ancestor import LowestCommonAncestor

# parent[i] is the parent of node i; the root is its own parent.
# The array must be in topological order (parents before children).
parent = [0, 0, 1, 1, 2]
tree = LowestCommonAncestor(parent)

assert tree.lca(2, 3) == 1
assert tree.lca(3, 4) == 1
assert tree.lca(0, 4) == 0
```

## Why this library exists

Computing the LCA of two nodes is a fundamental operation on trees, used in
network routing, version control, and phylogenetic analysis. A naive
implementation climbs parent pointers and takes O(n) time per query in the
worst case. This library preprocesses the tree once using an Euler tour and a
sparse table, giving O(n log n) preprocessing time and O(n log n) space, after
which each query runs in O(1).

The trade-off is that the input must be a parent array already in topological
order (each non-root parent appears before its child). This avoids an
expensive adjacency-list DFS during construction and keeps the implementation
predictable. If you only have an adjacency list, topologically sort it first.

## Edge cases

- The root must have `parent[root] == root`.
- Every non-root node must have `parent[node] < node`.
- The constructor raises `ValueError` for empty input, out-of-range parent
  indices, multiple roots, or non-topological order.
- `lca()` raises `IndexError` if either node index is outside the valid
  range.

Exports: `LowestCommonAncestor`.
