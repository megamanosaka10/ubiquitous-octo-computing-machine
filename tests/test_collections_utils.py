"""Tests for collections_utils module."""

import pytest

from octo_compute.collections_utils import (
    chunk,
    deep_merge,
    flatten,
    group_by,
    invert_dict,
    pluck,
    unique,
)


class TestFlatten:
    def test_already_flat(self):
        assert flatten([1, 2, 3]) == [1, 2, 3]

    def test_nested(self):
        assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]

    def test_empty(self):
        assert flatten([]) == []

    def test_deeply_nested(self):
        assert flatten([[[1]], [[2]]]) == [1, 2]


class TestChunk:
    def test_even_split(self):
        assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

    def test_uneven_split(self):
        assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    def test_size_larger_than_list(self):
        assert chunk([1, 2], 10) == [[1, 2]]

    def test_empty_list(self):
        assert chunk([], 3) == []

    def test_invalid_size_raises(self):
        with pytest.raises(ValueError, match="Chunk size must be positive"):
            chunk([1], 0)


class TestUnique:
    def test_removes_duplicates(self):
        assert unique([1, 2, 2, 3, 1]) == [1, 2, 3]

    def test_preserves_order(self):
        assert unique([3, 1, 2, 1, 3]) == [3, 1, 2]

    def test_empty(self):
        assert unique([]) == []

    def test_no_duplicates(self):
        assert unique([1, 2, 3]) == [1, 2, 3]


class TestGroupBy:
    def test_group_by_length(self):
        result = group_by(["hi", "hey", "yo", "yes"], len)
        assert result == {2: ["hi", "yo"], 3: ["hey", "yes"]}

    def test_group_by_parity(self):
        result = group_by([1, 2, 3, 4], lambda x: x % 2)
        assert result == {1: [1, 3], 0: [2, 4]}

    def test_empty(self):
        assert group_by([], str) == {}


class TestInvertDict:
    def test_basic_invert(self):
        assert invert_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}

    def test_empty(self):
        assert invert_dict({}) == {}

    def test_duplicate_values_raise(self):
        with pytest.raises(ValueError, match="Duplicate value"):
            invert_dict({"a": 1, "b": 1})


class TestDeepMerge:
    def test_flat_merge(self):
        assert deep_merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}

    def test_override(self):
        assert deep_merge({"a": 1}, {"a": 2}) == {"a": 2}

    def test_nested_merge(self):
        base = {"a": {"x": 1, "y": 2}}
        override = {"a": {"y": 3, "z": 4}}
        assert deep_merge(base, override) == {"a": {"x": 1, "y": 3, "z": 4}}

    def test_non_mutating(self):
        base = {"a": 1}
        deep_merge(base, {"b": 2})
        assert base == {"a": 1}


class TestPluck:
    def test_basic_pluck(self):
        items = [{"name": "a", "val": 1}, {"name": "b", "val": 2}]
        assert pluck(items, "name") == ["a", "b"]

    def test_missing_key_skipped(self):
        items = [{"name": "a"}, {"val": 2}]
        assert pluck(items, "name") == ["a"]

    def test_empty(self):
        assert pluck([], "key") == []
