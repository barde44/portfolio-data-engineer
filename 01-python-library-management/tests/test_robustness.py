
import json

import pytest

from src.library import Library


@pytest.fixture
def library(tmp_path):
    return Library(tmp_path / "books.json")


def test_empty_title(library):
    with pytest.raises(ValueError):
        library.add_book("", "Author", "Science")


def test_empty_author(library):
    with pytest.raises(ValueError):
        library.add_book("Python", "   ", "Programming")


def test_duplicate_book(library):
    library.add_book("Clean Code", "Martin", "Programming")

    with pytest.raises(ValueError):
        library.add_book("clean code", "Martin", "Programming")

    assert len(library.get_all_books()) == 1


def test_corrupted_json(tmp_path):
    file_path = tmp_path / "books.json"
    file_path.write_text("{ invalid json", encoding="utf-8")

    with pytest.raises(ValueError):
        Library(file_path)

    assert file_path.read_text(encoding="utf-8") == "{ invalid json"


def test_invalid_json_structure(tmp_path):
    file_path = tmp_path / "books.json"
    file_path.write_text(
        json.dumps({"books": []}), encoding="utf-8"
    )

    with pytest.raises(ValueError):
        Library(file_path)


def test_duplicate_title_update(library):
    library.add_book("Python", "Author A", "Programming")
    library.add_book("SQL", "Author B", "Databases")

    with pytest.raises(ValueError):
        library.update_book("Python", new_title="SQL")

    assert library.find_book("Python") is not None


def test_invalid_update_preserves_book(library):
    library.add_book("Python", "Author A", "Programming")

    with pytest.raises(ValueError):
        library.update_book("Python", new_author=" ")

    assert library.find_book("Python")["author"] == "Author A"


def test_missing_json_file(tmp_path):
    file_path = tmp_path / "nonexistent.json"

    library = Library(file_path)

    assert library.get_all_books() == []
