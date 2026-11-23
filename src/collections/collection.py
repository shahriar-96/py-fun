from typing import Any, Generic, Iterator, Self, TypeVar

from .collection_impl import CollectionImpl

# restrict generic type T to only accept given types
T = TypeVar("T", str, int, "Collection[int]", "Collection[str]")


class Collection(CollectionImpl, Generic[T]):
    """
    Generic collection class of type T with basic collection operations.
    See: https://sgra64.github.io/py-fun.github.io/src.collections.html.
    """

    def __init__(self, *args, asSet=False):
        """
        Constructor of a Collection.

        Args:
            args: elements added to the Collection including
            number or string literals, sets and lists.
        """
        super().__init__()
        self._items = set() if asSet else list()
        for arg in args:
            self.add(arg)

    def add(self, item: T) -> Self:
        """
        Add an element of type T to the collection.

        Args:
            item: element to add to the collection.

        Returns:
            Chainable self-reference to the collection with the element added.
        """
        item = item if not isinstance(item, set | dict) else frozenset(item)
        if isinstance(self._items, list):
            self._items.append(item)
        else:
            # list cannot be added to a set since lists are mutable and therefore unhashable.
            self._items.add(item if not isinstance(item, list) else tuple(item))
        return self

    def contains(self, item: Any) -> bool:
        """
        Test that an item or subset exists in the collection.

        Args:
            item: element to test that it is in the collection.

        Returns:
            True if element is in the collection, False otherwise.
        """
        if item in self._items:
            return True
        if isinstance(item, (set, frozenset, list, tuple)):
            target = set(item)
            current = {x for x in self._items if not isinstance(x, (set, frozenset, list, tuple))}
            return target.issubset(current)
        return False

    def size(self) -> int:
        """
        Returns the number of items in the collection.

        Returns:
            the number of items in the collection.
        """
        return len(self._items)

    @classmethod
    def zip(cls, l1: "Collection[list]", l2: "Collection[list]") -> "Collection[tuple]":
        """
        Return a new collection of two-item tuples zipped from the input collections.

        Args:
            c1: input Collection from which the left element is taken.
            c2: input Collection from which the right element is taken

        Returns:
            Collection of pairs zipped from each input Collection.
        """
        result = cls()
        for a, b in zip(l1, l2):
            result.add((a, b))
        return result

    def pset_gen(self) -> Iterator[set[T]]:
        """
        Generator that yields each subset using backtracking.

        Returns:
            Generator object for the power set of this Collection.
        """
        items = list(self._items)

        def _backtrack(index: int, current: list[T]) -> Iterator[set[T]]:
            if index == len(items):
                yield set(current)
                return
            yield from _backtrack(index + 1, current)
            current.append(items[index])
            yield from _backtrack(index + 1, current)
            current.pop()

        return _backtrack(0, [])

    def pset(_self) -> set[frozenset[T]]:
        """
        Return the power set of this Collection using backtracking.

        Returns:
            The power set of this Collection.
        """
        return {frozenset(subset) for subset in _self.pset_gen()}

    def perm_gen(self) -> Iterator[list[T]]:
        """
        Generator that yields permutations using backtracking.

        Returns:
            Generator object for the list of permutations of this Collection.
        """
        items = list(self._items)
        used = [False] * len(items)

        def _backtrack(path: list[T]) -> Iterator[list[T]]:
            if len(path) == len(items):
                yield list(path)
                return
            for i in range(len(items)):
                if not used[i]:
                    used[i] = True
                    path.append(items[i])
                    yield from _backtrack(path)
                    path.pop()
                    used[i] = False

        return _backtrack([])

    def perm(self) -> list[list[T]]:
        """
        Return all permutations of this Collection.

        Returns:
            The list of permutations of this Collection.
        """
        return list(self.perm_gen())

    def __contains__(self, item: Any) -> bool:
        """Checks if an item or subset exists in the collection (in-operator)."""
        return item in self._items

    def __len__(self) -> int:
        """Returns the number of items in the collection, invoked by len()."""
        return len(self._items)

    def __iter__(self) -> Iterator[Any]:
        """Returns an iterator over the items in the collection, invoked in loops."""
        return iter(self._items)

    def __repr__(self):
        """Custom representation for str() that formats inner frozenSets as { }."""
        elements = []
        for item in self._items:
            if isinstance(item, set | frozenset):
                elements.append(f"{{{', '.join(repr(e) for e in item)}}}")
            else:
                elements.append(repr(item))
        r = f"{', '.join(elements)}"
        return f"[{r}]" if isinstance(self._items, list) else f"{{{r}}}"
