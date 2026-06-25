"""Utilities for working with collections."""

from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, TypeVar

T = TypeVar("T")


def flatten(nested: List) -> List:
    """Recursively flatten a nested list."""
    flat: List = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat


def chunk(items: List[T], size: int) -> List[List[T]]:
    """Split *items* into chunks of *size*."""
    if size <= 0:
        raise ValueError("Chunk size must be positive")
    return [items[i : i + size] for i in range(0, len(items), size)]


def unique(items: List[T]) -> List[T]:
    """Return *items* with duplicates removed, preserving first occurrence order."""
    seen: set = set()
    result: List[T] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def group_by(items: Iterable[T], key_fn: Callable[[T], Any]) -> Dict[Any, List[T]]:
    """Group *items* by the value returned by *key_fn*."""
    groups: Dict[Any, List[T]] = {}
    for item in items:
        k = key_fn(item)
        groups.setdefault(k, []).append(item)
    return groups


def invert_dict(d: Dict) -> Dict:
    """Swap keys and values. Raises ValueError on duplicate values."""
    inv: Dict = {}
    for k, v in d.items():
        if v in inv:
            raise ValueError(f"Duplicate value: {v!r}")
        inv[v] = k
    return inv


def deep_merge(base: Dict, override: Dict) -> Dict:
    """Recursively merge *override* into *base* (non-mutating)."""
    merged = dict(base)
    for k, v in override.items():
        if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
            merged[k] = deep_merge(merged[k], v)
        else:
            merged[k] = v
    return merged


def pluck(items: List[Dict], key: str) -> List:
    """Extract a single *key* from each dict in *items*."""
    return [item[key] for item in items if key in item]
