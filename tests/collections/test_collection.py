import importlib.util
import sys
import types
from pathlib import Path


def _load_collection_class():
    src_root = Path(__file__).resolve().parents[2] / "src"
    if str(src_root) not in sys.path:
        sys.path.insert(0, str(src_root))

    pkg_name = "_test_collections_pkg"
    if pkg_name not in sys.modules:
        pkg = types.ModuleType(pkg_name)
        pkg.__path__ = [str(src_root / "collections")]
        sys.modules[pkg_name] = pkg

    impl_name = f"{pkg_name}.collection_impl"
    if impl_name not in sys.modules:
        impl_path = src_root / "collections" / "collection_impl.py"
        impl_spec = importlib.util.spec_from_file_location(impl_name, impl_path)
        impl_mod = importlib.util.module_from_spec(impl_spec)
        impl_mod.__package__ = pkg_name
        sys.modules[impl_name] = impl_mod
        impl_spec.loader.exec_module(impl_mod)

    col_name = f"{pkg_name}.collection"
    col_path = src_root / "collections" / "collection.py"
    col_spec = importlib.util.spec_from_file_location(col_name, col_path)
    col_mod = importlib.util.module_from_spec(col_spec)
    col_mod.__package__ = pkg_name
    sys.modules[col_name] = col_mod
    col_spec.loader.exec_module(col_mod)
    return col_mod.Collection


def test_collection_init_size_and_contains():
    Collection = _load_collection_class()
    col = Collection(1, 2, 3)
    assert col.size() == 3
    assert len(col) == 3
    assert col.contains(2) is True
    assert col.contains(99) is False


def test_collection_add_and_as_set():
    Collection = _load_collection_class()
    col = Collection(asSet=True).add(1).add(1).add(2)
    assert col.size() == 2
    assert col.contains(1) is True


def test_collection_zip():
    Collection = _load_collection_class()
    left = Collection("a", "b")
    right = Collection(1, 2)
    zipped = Collection.zip(left, right)
    assert list(zipped) == [("a", 1), ("b", 2)]


def test_collection_pset_and_perm():
    Collection = _load_collection_class()
    col = Collection(1, 2)
    assert col.pset() == {frozenset(), frozenset({1}), frozenset({2}), frozenset({1, 2})}
    assert col.perm() == [[1, 2], [2, 1]]
