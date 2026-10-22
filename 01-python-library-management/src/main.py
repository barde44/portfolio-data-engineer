
from src.library import Library


def display_menu():
    """Display the main menu."""

    print("\n" + "=" * 50)
    print("       PERSONAL LIBRARY MANAGEMENT SYSTEM")
    print("=" * 50)

    print("1. Add a new book")
    print("2. View all books")
    print("3. Search for a book")
    print("4. Update a book")
    print("5. Delete a book")
    print("6. Sort books")
    print("0. Exit")

    print("-" * 50)


def display_books(books):
    """Display a list of books."""

    if not books:
        print("\nNo books found.")
        return

    print(f"\nTotal books: {len(books)}")

    for index, book in enumerate(books, start=1):
        print(f"\nBook {index}")
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Category: {book['category']}")
        print(f"Date added: {book['date_added']}")
        print("-" * 30)


def add_book_menu(library):
    """Handle book creation."""

    print("\n--- ADD A NEW BOOK ---")

    title = input("Enter title: ").strip()
    author = input("Enter author: ").strip()
    category = input("Enter category: ").strip()

    if not title or not author or not category:
        print("Error: All fields are required.")
        return

    book = library.add_book(title, author, category)

    print(f"\nBook '{book['title']}' added successfully!")


def view_books_menu(library):
    """Display all stored books."""

    print("\n--- ALL BOOKS ---")

    books = library.get_all_books()

    display_books(books)


def search_book_menu(library):
    """Search books by title or author."""

    print("\n--- SEARCH BOOKS ---")

    keyword = input("Enter title or author: ").strip()

    if not keyword:
        print("Error: Search keyword cannot be empty.")
        return

    results = library.search_books(keyword)

    display_books(results)


def update_book_menu(library):
    """Update an existing book."""

    print("\n--- UPDATE BOOK ---")

    title = input("Enter the current book title: ").strip()

    print("\nLeave a field empty to keep its current value.")

    new_title = input("New title: ").strip()
    new_author = input("New author: ").strip()
    new_category = input("New category: ").strip()

    updated_book = library.update_book(
        title,
        new_title=new_title if new_title else None,
        new_author=new_author if new_author else None,
        new_category=new_category if new_category else None
    )

    if updated_book:
        print("\nBook updated successfully!")
        display_books([updated_book])
    else:
        print("\nBook not found.")


def delete_book_menu(library):
    """Delete an existing book."""

    print("\n--- DELETE BOOK ---")

    title = input("Enter the book title: ").strip()

    confirmation = input(
        f"Are you sure you want to delete '{title}'? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("Deletion cancelled.")
        return

    deleted = library.delete_book(title)

    if deleted:
        print("\nBook deleted successfully!")
    else:
        print("\nBook not found.")


def sort_books_menu(library):
    """Sort books by different criteria."""

    print("\n--- SORT BOOKS ---")

    print("1. Sort by title")
    print("2. Sort by category")
    print("3. Sort by date added")

    choice = input("Select sorting field: ").strip()

    sorting_options = {
        "1": "title",
        "2": "category",
        "3": "date_added"
    }

    if choice not in sorting_options:
        print("Invalid sorting option.")
        return

    order = input(
        "Descending order? (yes/no): "
    ).strip().lower()

    descending = order == "yes"

    sorted_books = library.sort_books(
        sort_by=sorting_options[choice],
        descending=descending
    )

    display_books(sorted_books)


def main():
    """Run the library management application."""

    library = Library()

    while True:

        display_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book_menu(library)

        elif choice == "2":
            view_books_menu(library)

        elif choice == "3":
            search_book_menu(library)

        elif choice == "4":
            update_book_menu(library)

        elif choice == "5":
            delete_book_menu(library)

        elif choice == "6":
            sort_books_menu(library)

        elif choice == "0":
            print("\nThank you for using the Library System!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
