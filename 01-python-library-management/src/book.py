from datetime import datetime


class Book:
    def __init__(self, title, author, category):
        self.title = title
        self.author = author
        self.category = category
        self.date_added = datetime.now().isoformat()

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "date_added": self.date_added
        }
