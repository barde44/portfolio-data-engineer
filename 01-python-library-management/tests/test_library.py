
import pytest

from src.library import Library


@pytest.fixture
def library(tmp_path):
    """Create an isolated library for each test."""

    test_file = tmp_path / "test_books.json"

    return Library(file_path=test_file)


def test_empty_library(library):
    """A new library should be empty."""

    assert library.get_all_books() == []


def test_add_book(library):
    """A book should be added successfully."""

    book = library.add_book(
        "Python Crash Course",
        "Eric Matthes",
        "Programming"
    )

    assert book["title"] == "Python Crash Course"
    assert book["author"] == "Eric Matthes"
    assert len(library.get_all_books()) == 1


def test_save_and_load_books(library):
    """Books should persist in the JSON file."""

    library.add_book(
        "Clean Code",
        "Robert C. Martin",
        "Software Engineering"
    )

    new_library = Library(file_path=library.file_path)

    assert len(new_library.get_all_books()) == 1
    assert new_library.get_all_books()[0]["title"] == "Clean Code"


def test_search_by_title(library):
    """Search should find books by title."""

    library.add_book(
        "Learning SQL",
        "Alan Beaulieu",
        "Databases"
    )

    results = library.search_books("sql")

    assert len(results) == 1
    assert results[0]["title"] == "Learning SQL"


def test_search_by_author(library):
    """Search should find books by author."""

    library.add_book(
        "Clean Code",
        "Robert C. Martin",
        "Programming"
    )

    results = library.search_books("martin")

    assert len(results) == 1
    assert results[0]["author"] == "Robert C. Martin"


def test_search_unknown_book(library):
    """Unknown books should return no results."""

    assert library.search_books("Unknown Book") == []


def test_update_book(library):
    """Book details should be updated."""

    original = library.add_book(
        "Python Crash Course",
        "Eric Matthes",
        "Programming"
    )

    updated = library.update_book(
        "Python Crash Course",
        new_category="Software Development"
    )

    assert updated["category"] == "Software Development"
    assert updated["date_added"] == original["date_added"]


def test_update_unknown_book(library):
    """Updating an unknown book should return None."""

    result = library.update_book(
        "Unknown Book",
        new_category="Technology"
    )

    assert result is None


def test_delete_book(library):
    """An existing book should be deleted."""

    library.add_book(
        "Clean Code",
        "Robert C. Martin",
        "Programming"
    )

    result = library.delete_book("Clean Code")

    assert result is True
    assert library.get_all_books() == []


def test_delete_unknown_book(library):
    """Deleting an unknown book should return False."""

    assert library.delete_book("Unknown Book") is False


def test_sort_books_by_title(library):
    """Books should be sorted alphabetically."""

    library.add_book("Z Book", "Author A", "Technology")
    library.add_book("A Book", "Author B", "Programming")

    sorted_books = library.sort_books("title")

    assert sorted_books[0]["title"] == "A Book"
    assert sorted_books[1]["title"] == "Z Book"


def test_sort_books_by_category(library):
    """Books should be sorted by category."""

    library.add_book("Book One", "Author A", "Science")
    library.add_book("Book Two", "Author B", "Business")

    sorted_books = library.sort_books("category")

    assert sorted_books[0]["category"] == "Business"


def test_sort_books_descending(library):
    """Descending sorting should reverse the order."""

    library.add_book("A Book", "Author A", "Science")
    library.add_book("Z Book", "Author B", "Science")

    sorted_books = library.sort_books(
        "title",
        descending=True
    )

    assert sorted_books[0]["title"] == "Z Book"


def test_invalid_sort_field(library):
    """Invalid sorting fields should raise an error."""

    with pytest.raises(ValueError):
        library.sort_books("price")
