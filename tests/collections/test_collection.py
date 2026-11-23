import unittest
import importlib.util
import sys
import types
from pathlib import Path

def _get_collection(tag: str):
    src_root = Path(__file__).resolve().parents[2] / "src"
    if str(src_root) not in sys.path:
        sys.path.insert(0, str(src_root))

    pkg_name = f"_col_pkg_{tag}"
    if pkg_name not in sys.modules:
        pkg = types.ModuleType(pkg_name)
        pkg.__path__ = [str(src_root / "collections")]
        sys.modules[pkg_name] = pkg

    impl_name = f"{pkg_name}.collection_impl"
    if impl_name not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            impl_name, src_root / "collections" / "collection_impl.py"
        )
        mod = importlib.util.module_from_spec(spec)
        mod.__package__ = pkg_name
        sys.modules[impl_name] = mod
        spec.loader.exec_module(mod)

    col_name = f"{pkg_name}.collection"
    if col_name not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            col_name, src_root / "collections" / "collection.py"
        )
        mod = importlib.util.module_from_spec(spec)
        mod.__package__ = pkg_name
        sys.modules[col_name] = mod
        spec.loader.exec_module(mod)

    return sys.modules[col_name].Collection

Collection = _get_collection('main')

class TestCollection(unittest.TestCase):

    def test_contains_and_add(self):
        col = Collection()
        self.assertFalse(col.contains(1))
        self.assertIs(col.add(1), col)
        self.assertTrue(col.contains(1))
        col.add(1)
        self.assertEqual(col._items, [1, 1])

    def test_contains_and_add_in_set(self):
        col = Collection(asSet=True)
        self.assertFalse(col.contains(1))
        self.assertIs(col.add(1), col)
        self.assertTrue(col.contains(1))
        col.add(1)
        self.assertEqual(col._items, {1})

    def test_add_only_keeps_unique_set_items(self):
        collection = Collection(asSet=True)
        collection.add({1, 2}).add({1, 2})
        self.assertEqual(collection._items, {frozenset({1, 2})})

    def test_constructor_accepts_list_and_set_iterables(self):
        numbers = Collection([1, 2, 3])
        letters = Collection({"a", "b", "c"})

        self.assertEqual(numbers._items, [[1, 2, 3]])
        self.assertEqual(letters._items, [frozenset({"a", "b", "c"})])

    def test_constructor_accepts_variadic_items_and_set_mode(self):
        numbers = Collection(1, 2, 2)
        unique_numbers = Collection(1, 2, 2, asSet=True)

        self.assertEqual(numbers._items, [1, 2, 2])
        self.assertEqual(unique_numbers._items, {1, 2})

    def test_repr_displays_set_braces(self):
        self.assertEqual(repr(Collection(1, 2, asSet=True)), "{1, 2}")

    def test_zip_returns_pairs_and_stops_at_shorter_collection(self):
        zipped = Collection.zip(
            Collection("a", "b", "c"),
            Collection(1, 2),
        )

        self.assertIsInstance(zipped, Collection)
        self.assertEqual(zipped._items, [("a", 1), ("b", 2)])

    def test_zip_with_empty_collection_returns_empty_collection(self):
        self.assertEqual(Collection.zip(Collection(), Collection(1))._items, [])

    # def test_constructor_rejects_other_iterables(self):
    #     with self.assertRaisesRegex(TypeError, "elements must be a list or set"):
    #         Collection((1, 2, 3))

    def test_perm_returns_all_full_length_permutations(self):
        permutations = Collection(1, 2, 3).perm()

        self.assertEqual(
            {tuple(permutation) for permutation in permutations},
            {
                (1, 2, 3),
                (1, 3, 2),
                (2, 1, 3),
                (2, 3, 1),
                (3, 1, 2),
                (3, 2, 1),
            },
        )

    def test_perm_preserves_duplicate_positions(self):
        self.assertEqual(Collection(1, 1).perm(), [[1, 1], [1, 1]])

    def test_perm_of_empty_collection_contains_empty_permutation(self):
        self.assertEqual(Collection().perm(), [[]])

    def test_perm_gen_yields_permutations_lazily(self):
        permutations = Collection(1, 2, 3).perm_gen()

        self.assertIs(iter(permutations), permutations)
        self.assertEqual(
            {tuple(permutation) for permutation in permutations},
            {
                (1, 2, 3),
                (1, 3, 2),
                (2, 1, 3),
                (2, 3, 1),
                (3, 1, 2),
                (3, 2, 1),
            },
        )

    def test_perm_gen_preserves_duplicate_positions(self):
        self.assertEqual(list(Collection(1, 1).perm_gen()), [[1, 1], [1, 1]])

    def test_perm_gen_of_empty_collection_yields_empty_permutation(self):
        self.assertEqual(list(Collection().perm_gen()), [[]])


if __name__ == "__main__":
    unittest.main()