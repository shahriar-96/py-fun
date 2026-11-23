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

Collection = _get_collection('pset')

class TestCollection(unittest.TestCase):

    def test_pset_returns_all_subsets_without_duplicate_values(self):
        powerset = Collection(1, 2, 2).pset()
        self.assertEqual(
            {frozenset(subset) for subset in powerset},
            {frozenset(), frozenset({1}), frozenset({2}), frozenset({1, 2})},
        )
        self.assertEqual(len(powerset), 4)

    def test_pset_backtracks_over_each_set_item(self):
        powerset = Collection(1, 2, asSet=True).pset()
        self.assertEqual(
            {frozenset(subset) for subset in powerset},
            {frozenset(), frozenset({1}), frozenset({2}), frozenset({1, 2})},
        )

    def test_pset_of_empty_collection_contains_empty_set(self):
        self.assertEqual(Collection().pset(), {frozenset()})

    def test_pset_gen_yields_all_subsets_without_duplicate_values(self):
        powerset = Collection(1, 2, 2).pset_gen()

        self.assertIs(iter(powerset), powerset)
        self.assertEqual(
            {frozenset(subset) for subset in powerset},
            {frozenset(), frozenset({1}), frozenset({2}), frozenset({1, 2})},
        )

    def test_pset_gen_of_empty_collection_yields_empty_set(self):
        self.assertEqual(list(Collection().pset_gen()), [set()])


if __name__ == "__main__":
    unittest.main()
