"""Tests for the LowestCommonAncestor class."""

import unittest

from lowest_common_ancestor import LowestCommonAncestor


class TestLowestCommonAncestor(unittest.TestCase):
    def test_single_node(self):
        lca_prep = LowestCommonAncestor([0])
        self.assertEqual(lca_prep.lca(0, 0), 0)
        self.assertEqual(lca_prep.root, 0)

    def test_simple_chain(self):
        # 0 -> 1 -> 2 -> 3
        lca_prep = LowestCommonAncestor([0, 0, 1, 2])
        self.assertEqual(lca_prep.lca(2, 3), 2)
        self.assertEqual(lca_prep.lca(0, 3), 0)
        self.assertEqual(lca_prep.lca(1, 3), 1)

    def test_two_branches(self):
        #       0
        #      / \
        #     1   2
        #    / \   \
        #   3   4   5
        parent = [0, 0, 0, 1, 1, 2]
        lca_prep = LowestCommonAncestor(parent)
        self.assertEqual(lca_prep.lca(3, 4), 1)
        self.assertEqual(lca_prep.lca(3, 5), 0)
        self.assertEqual(lca_prep.lca(4, 5), 0)
        self.assertEqual(lca_prep.lca(1, 2), 0)

    def test_deep_tree(self):
        # A binary-ish tree with 15 nodes, root 0.
        parent = [0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
        lca_prep = LowestCommonAncestor(parent)
        self.assertEqual(lca_prep.lca(7, 8), 3)
        self.assertEqual(lca_prep.lca(7, 9), 1)
        self.assertEqual(lca_prep.lca(10, 14), 0)
        self.assertEqual(lca_prep.lca(13, 14), 6)

    def test_lca_with_self(self):
        parent = [0, 0, 1, 2]
        lca_prep = LowestCommonAncestor(parent)
        self.assertEqual(lca_prep.lca(2, 2), 2)
        self.assertEqual(lca_prep.lca(3, 3), 3)

    def test_query_order_does_not_matter(self):
        parent = [0, 0, 1, 1, 2]
        lca_prep = LowestCommonAncestor(parent)
        self.assertEqual(lca_prep.lca(3, 4), lca_prep.lca(4, 3))
        self.assertEqual(lca_prep.lca(2, 3), lca_prep.lca(3, 2))

    def test_out_of_range_raises_index_error(self):
        parent = [0, 0, 1]
        lca_prep = LowestCommonAncestor(parent)
        with self.assertRaises(IndexError):
            lca_prep.lca(0, 3)
        with self.assertRaises(IndexError):
            lca_prep.lca(-1, 1)

    def test_empty_parent_raises_value_error(self):
        with self.assertRaises(ValueError):
            LowestCommonAncestor([])

    def test_parent_out_of_range_raises_value_error(self):
        with self.assertRaises(ValueError):
            LowestCommonAncestor([0, 3])
        with self.assertRaises(ValueError):
            LowestCommonAncestor([0, -1])

    def test_multiple_roots_raises_value_error(self):
        with self.assertRaises(ValueError):
            LowestCommonAncestor([0, 1])

    def test_non_topological_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            LowestCommonAncestor([0, 1, 1])

    def test_no_self_parent_raises_value_error(self):
        with self.assertRaises(ValueError):
            LowestCommonAncestor([1, 0, 0])

    def test_large_random_tree_consistency(self):
        # Build a deterministic pseudo-random tree with 200 nodes and
        # compare LCA results against a naive parent-climbing method.
        # This exercises the sparse table on a non-trivial input without
        # relying on any external randomness.
        n = 200
        parent = [0] * n
        parent[0] = 0
        for i in range(1, n):
            # Parent is (i * 7) % i, which guarantees parent < i.
            parent[i] = (i * 7) % i

        lca_prep = LowestCommonAncestor(parent)

        def naive_lca(a: int, b: int) -> int:
            ancestors_a = set()
            while True:
                ancestors_a.add(a)
                if parent[a] == a:
                    break
                a = parent[a]
            while b not in ancestors_a:
                b = parent[b]
            return b

        for i in range(0, n, 7):
            for j in range(0, n, 11):
                self.assertEqual(lca_prep.lca(i, j), naive_lca(i, j))


if __name__ == "__main__":
    unittest.main()
