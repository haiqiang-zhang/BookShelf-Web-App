import csv
from datetime import date, datetime
from typing import List
from pathlib import Path

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import User, Author, Book, Review, Tag


class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self.__books = list()
        self.__books_index = dict()
        self.__tags = list()
        self.__users = list()
        self.__comments = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def add_book(self, book: Book):
        insort_left(self.__books, book)
        self.__books_index[Book.book_id] = book

    def get_book(self, id: int) -> Book:
        book = None

        try:
            book = self.__books[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return book

    def get_Books_by_year(self, year: int) -> List[Book]:
        matching_book = list()

        try:
            for book in self.__books:
                if book.release_year == year:
                    matching_book.append(book)
                else:
                    break
        except ValueError:
            # No articles for specified date. Simply return an empty list.
            pass

        return matching_book

    def get_number_of_books(self) -> int:
        return len(self.__books)

    def get_book_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Article ids in the repository.
        existing_ids = [id for id in id_list if id in self.__books_index]

        # Fetch the Articles.
        books = [self.__books_index[id] for id in existing_ids]
        return books




    def get_book_ids_for_tag(self, tag_name: str):
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        tag = next((tag for tag in self.__tags if tag.tag_name == tag_name), None)

        # Retrieve the ids of articles associated with the Tag.
        if tag is not None:
            book_ids = [book.book_id for book in tag.tagged_books]
        else:
            # No Tag with name tag_name, so return an empty list.
            book_ids = list()

        return book_ids

    def add_tag(self, tag: Tag):
        self.__tags.append(tag)

    def get_tags(self) -> List[Tag]:
        return self.__tags

    # Helper method to return article index.
    def book_index(self, book: Book):
        index = bisect_left(self.__books, book)
        if index != len(self.__books) and self.__books[index].title == book.title:
            return index
        raise ValueError


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row

def load_users(data_path: Path, repo: MemoryRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def create_book(data_path):
    from library.adapters import jsondatareader
    book_path = str(data_path / 'comic_books_excerpt.json')
    author_path = str(data_path / 'book_authors_excerpt.json')
    reader = jsondatareader.BooksJSONReader(book_path, author_path)
    reader.read_json_files()
    return reader.dataset_of_books
    print(reader.dataset_of_books[0])
    print(reader.dataset_of_books[10])
    print(reader.dataset_of_books[19])
    print(reader.dataset_of_books[4].publisher)
    print(reader.dataset_of_books[15].authors[0])


def populate(data_path: Path, repo: MemoryRepository):
    # Load articles and tags into the repository.
    create_book(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

