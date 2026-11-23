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

Collection = _get_collection('perm')

class TestCollection(unittest.TestCase):

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