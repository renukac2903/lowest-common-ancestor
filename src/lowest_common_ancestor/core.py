"""Core implementation of the LowestCommonAncestor preprocessor.

The implementation uses the Euler tour technique together with a sparse
table over the depth array.  This gives O(n log n) preprocessing time,
O(n log n) space, and O(1) query time for a tree with n nodes.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Optional


class LowestCommonAncestor:
    """Preprocess a rooted tree for constant-time LCA queries.

    Parameters
    ----------
    parent:
        A sequence of length n describing the parent of each node.  The
        root is identified by ``parent[root] == root``.  Every other node
        must have its parent appearing earlier in the sequence, so the
        input is required to be in topological (root-to-leaf) order.
        This restriction keeps the implementation simple and avoids
        requiring an adjacency-list DFS on arbitrary input; callers who
        have an adjacency list can topologically sort it first.

    Raises
    ------
    ValueError:
        If the tree is empty, if the parent array is inconsistent (a node
        references an index outside the array or references itself in a
        non-root position), or if the parent relation does not form a
        single rooted tree.
    """

    def __init__(self, parent: Sequence[int]) -> None:
        n = len(parent)
        if n == 0:
            raise ValueError("parent array must not be empty")

        # Validate the parent array and locate the root.  Each non-root
        # node must point to an earlier index.  This guarantees that the
        # input is already a topological ordering of the rooted tree.
        root = -1
        for node, p in enumerate(parent):
            if p < 0 or p >= n:
                raise ValueError(f"parent of node {node} is out of range: {p}")
            if p == node:
                if root != -1:
                    raise ValueError("multiple roots are not supported")
                root = node
            elif p >= node:
                raise ValueError(
                    f"parent of node {node} must appear before the node"
                )
        if root == -1:
            raise ValueError("no root found in parent array")

        self._n = n
        self._root = root

        # Depth of each node.  This is also a useful validation step: if
        # the parent pointers contain a cycle not involving the root, the
        # depth computation would become inconsistent, but the topological
        # ordering check above already prevents cycles from existing.
        depth = [0] * n
        for node in range(n):
            if node != root:
                depth[node] = depth[parent[node]] + 1

        # Build an Euler tour of the tree.  We traverse children in
        # increasing node order, which makes the result deterministic and
        # easy to reason about.  For a tree on n nodes the Euler tour has
        # exactly 2n - 1 entries.
        children: list[list[int]] = [[] for _ in range(n)]
        for node in range(n):
            if node != root:
                children[parent[node]].append(node)

        tour: list[int] = []
        first_occurrence = [-1] * n

        def dfs(node: int) -> None:
            first_occurrence[node] = len(tour)
            tour.append(node)
            for child in children[node]:
                dfs(child)
                tour.append(node)

        dfs(root)

        self._first_occurrence = first_occurrence
        self._depth = depth
        self._tour = tour

        # Build a sparse table over the depth array of the Euler tour.
        # The table stores indices into the tour rather than depths so
        # that we can retrieve the actual node directly at query time.
        m = len(tour)
        log = (m).bit_length()
        sparse = [[0] * m for _ in range(log)]
        sparse[0] = list(range(m))

        for k in range(1, log):
            step = 1 << (k - 1)
            prev = sparse[k - 1]
            curr = sparse[k]
            for i in range(m - (1 << k) + 1):
                left = prev[i]
                right = prev[i + step]
                if depth[tour[left]] <= depth[tour[right]]:
                    curr[i] = left
                else:
                    curr[i] = right

        self._sparse = sparse

    def lca(self, a: int, b: int) -> int:
        """Return the lowest common ancestor of nodes ``a`` and ``b``.

        The query takes constant time after preprocessing.

        Raises
        ------
        IndexError:
            If either node index is outside the valid range.
        """
        n = self._n
        if a < 0 or a >= n or b < 0 or b >= n:
            raise IndexError("node index out of range")

        left = self._first_occurrence[a]
        right = self._first_occurrence[b]
        if left > right:
            left, right = right, left

        length = right - left + 1
        k = length.bit_length() - 1
        sparse_row = self._sparse[k]
        candidate1 = sparse_row[left]
        candidate2 = sparse_row[right - (1 << k) + 1]

        depth = self._depth
        tour = self._tour
        if depth[tour[candidate1]] <= depth[tour[candidate2]]:
            return tour[candidate1]
        return tour[candidate2]

    @property
    def root(self) -> int:
        """The root node index."""
        return self._root
