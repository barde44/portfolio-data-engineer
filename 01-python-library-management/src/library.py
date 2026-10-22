
import json
import os
import tempfile
from pathlib import Path

from src.book import Book


class Library:
    REQUIRED_FIELDS = (
        "title", "author", "category", "date_added"
    )

    def __init__(self, file_path="data/books.json"):
        self.file_path = Path(file_path)
        self.books = []
        self.load_books()

    @staticmethod
    def validate_text(value, field_name):
        """Validate and normalize text input."""

        if not isinstance(value, str):
            raise ValueError(
                f"{field_name} must be a string."
            )

        value = value.strip()

        if not value:
            raise ValueError(
                f"{field_name} cannot be empty."
            )

        return value

    def load_books(self):
        """Load and validate JSON data."""

        if not self.file_path.exists():
            self.books = []
            return

        try:
            with self.file_path.open(
                "r", encoding="utf-8"
            ) as file:
                data = json.load(file)

        except (json.JSONDecodeError, UnicodeError) as exc:
            raise ValueError(
                "Invalid JSON data. "
                "The original file was not modified."
            ) from exc

        if not isinstance(data, list):
            raise ValueError(
                "Invalid library format: expected a list."
            )

        seen_titles = set()

        for index, book in enumerate(data):
            if not isinstance(book, dict):
                raise ValueError(
                    f"Invalid book at index {index}."
                )

            for field in self.REQUIRED_FIELDS:
                if field not in book:
                    raise ValueError(
                        f"Missing field '{field}' "
                        f"at index {index}."
                    )

                self.validate_text(book[field], field)

            normalized_title = book["title"].strip().casefold()

            if normalized_title in seen_titles:
                raise ValueError(
                    f"Duplicate title in JSON: {book['title']}"
                )

            seen_titles.add(normalized_title)

        self.books = data

    def save_books(self):
        """Save data using an atomic file replacement."""

        self.file_path.parent.mkdir(
            parents=True, exist_ok=True
        )

        temporary_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.file_path.parent,
                prefix=".books_",
                suffix=".tmp",
                delete=False
            ) as file:
                temporary_path = Path(file.name)

                json.dump(
                    self.books,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

                file.flush()
                os.fsync(file.fileno())

            os.replace(temporary_path, self.file_path)

        finally:
            if (
                temporary_path is not None
                and temporary_path.exists()
            ):
                temporary_path.unlink()

    def find_book(self, title):
        """Find a book by its exact title."""

        title = self.validate_text(title, "Title")
        normalized = title.casefold()

        for book in self.books:
            if book["title"].casefold() == normalized:
                return book

        return None

    def add_book(self, title, author, category):
        """Add a validated book."""

        title = self.validate_text(title, "Title")
        author = self.validate_text(author, "Author")
        category = self.validate_text(category, "Category")

        if self.find_book(title):
            raise ValueError(
                f"Book '{title}' already exists."
            )

        book = Book(title, author, category)
        record = book.to_dict()

        self.books.append(record)

        try:
            self.save_books()
        except OSError:
            self.books.pop()
            raise

        return record

    def get_all_books(self):
        """Return the list of books."""

        return self.books

    def search_books(self, keyword):
        """Search by title or author."""

        keyword = self.validate_text(
            keyword, "Search keyword"
        ).casefold()

        return [
            book for book in self.books
            if keyword in book["title"].casefold()
            or keyword in book["author"].casefold()
        ]

    def update_book(
        self, title, new_title=None,
        new_author=None, new_category=None
    ):
        """Update a book while preserving its date."""

        book = self.find_book(title)

        if book is None:
            return None

        updated = book.copy()

        if new_title is not None:
            updated["title"] = self.validate_text(
                new_title, "Title"
            )

            existing = self.find_book(updated["title"])

            if existing is not None and existing is not book:
                raise ValueError(
                    "Another book already has this title."
                )

        if new_author is not None:
            updated["author"] = self.validate_text(
                new_author, "Author"
            )

        if new_category is not None:
            updated["category"] = self.validate_text(
                new_category, "Category"
            )

        old_value = book.copy()
        book.update(updated)

        try:
            self.save_books()
        except OSError:
            book.clear()
            book.update(old_value)
            raise

        return book

    def delete_book(self, title):
        """Delete a book if it exists."""

        book = self.find_book(title)

        if book is None:
            return False

        index = self.books.index(book)
        self.books.pop(index)

        try:
            self.save_books()
        except OSError:
            self.books.insert(index, book)
            raise

        return True

    def sort_books(
        self, sort_by="title", descending=False
    ):
        """Return sorted books without modifying storage."""

        allowed_fields = [
            "title", "category", "date_added"
        ]

        if sort_by not in allowed_fields:
            raise ValueError(
                f"Invalid sorting field: {sort_by}. "
                f"Choose from {allowed_fields}"
            )

        return sorted(
            self.books,
            key=lambda book: (
                book[sort_by].casefold()
                if sort_by != "date_added"
                else book[sort_by]
            ),
            reverse=descending
        )
