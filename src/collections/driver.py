from collections.collection import Collection


def main() -> None:
    col = Collection()
    col.add("first")
    col.add("second")
    print("Items:", col.items())


if __name__ == "__main__":
    main()