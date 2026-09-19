"""Lowest common ancestor queries on static trees.

This package exports a single class, :class:`LowestCommonAncestor`,
which preprocesses a rooted tree so that LCA queries can be answered in
constant time.
"""

from .core import LowestCommonAncestor

__all__ = ["LowestCommonAncestor"]
