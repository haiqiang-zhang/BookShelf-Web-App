import csv
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from library.adapters.jsondatareader import BooksJSONReader
from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory, Tag, make_review


class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self.__books = list()
        self.__books_index = dict()
        self.__tags = list()
        self.__users = list()
        self.__reviews = list()
        self.__author = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_all_user(self) -> List[User]:
        return self.__users

    def get_user_num_of_read_book(self, user: User) -> int:
        return len(user.read_books)

    def get_user_read_book(self, user: User) -> List[Book]:
        return user.read_books

    def get_favourite(self, user: User):
        return user.favourite

    def add_book(self, book: Book):
        insort_left(self.__books, book)
        self.__books_index[book.book_id] = book

    def get_book(self, id: int) -> Book:
        book = None
        try:
            book = self.__books_index[id]

        except KeyError:
            book = None

        return book

    def get_all_books(self) -> List[Book]:
        return self.__books

    def get_books_by_release_year(self, release_year: int) -> List[Book]:
        matching_articles = list()
        try:
            for book in self.__books:
                if book.release_year == release_year:
                    matching_articles.append(book)
        except ValueError:
            pass
        return matching_articles

    def get_number_of_books(self) -> int:
        return len(self.__books)

    def get_books_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Article ids in the repository.
        existing_ids = [id for id in id_list if id in self.__books_index]

        # Fetch the Books.
        books = [self.__books_index[id] for id in existing_ids]
        return books

    def get_books_by_index(self, index: List[int]) -> List[Book]:
        return [self.__books[index] for index in index]

    def get_books_by_authors(self, author_input: str) -> List[Book]:
        matching_articles = list()
        try:
            for book in self.__books:
                for author in book.authors:
                    if author_input in author.full_name:
                        matching_articles.append(book)
        except ValueError:
            pass
        return matching_articles

    def get_books_by_publisher(self, publisher: Publisher) -> List[Book]:
        matching_articles = list()
        try:
            for book in self.__books:
                if book.publisher == publisher:
                    matching_articles.append(book)
        except ValueError:
            pass
        return matching_articles

    def get_books_by_title(self, title: str) -> List[Book]:
        matching_articles = list()
        try:
            for book in self.__books:
                if title in book.title:
                    matching_articles.append(book)
        except ValueError:
            pass
        return matching_articles

    def get_books_ids_for_tag(self, tag_name: str):
        # Linear search_blueprint, to find the first occurrence of a Tag with the name tag_name.
        tag = next((tag for tag in self.__tags if tag.tag_name == tag_name), None)

        # Retrieve the ids of articles associated with the Tag.
        if tag is not None:
            book_ids = [book.id for book in tag.tagged_books]
        else:
            # No Tag with name tag_name, so return an empty list.
            book_ids = list()

        return book_ids

    def add_tag(self, tag: Tag):
        self.__tags.append(tag)

    def get_tags(self) -> List[Tag]:
        return self.__tags

    def get_tag_by_name(self, name:str):
        for tag in self.__tags:
            if tag.tag_name == name:
                return tag
        return None

    def add_review(self, review: Review):
        # call parent class first, add_comment relies on implementation of code common to all derived classes
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews

    # Helper method to return article index.
    def book_index(self, book: Book):
        index = bisect_left(self.__books, book)
        if index != len(self.__books) and self.__books[index].book_id == book.book_id:
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


def load_books_and_author(data_path: Path, repo: MemoryRepository):
    book_path = str(Path(data_path) / "comic_books_excerpt.json")
    author_path = str(Path(data_path) / "book_authors_excerpt.json")
    JSONReader = BooksJSONReader(book_path, author_path)
    JSONReader.read_json_files()
    for book in JSONReader.dataset_of_books:
        repo.add_book(book)


def load_tags(data_path: Path, repo: MemoryRepository):
    tag_path = str(Path(data_path) / "tags.csv")
    for data_row in read_csv_file(tag_path):
        tag = Tag(data_row[0])
        repo.add_tag(tag)


def load_users(data_path: Path, repo: MemoryRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        id_list = data_row[3].strip().split(",")
        for id in id_list:
            if id != "":
                user.read_a_book(repo.get_book(int(id)))
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_reviews(data_path: Path, repo: MemoryRepository, users):
    review_filename = str(Path(data_path) / "reviews.csv")
    for data_row in read_csv_file(review_filename):
        review = make_review(
            review_text=data_row[3],
            user=users[data_row[1]],
            book=repo.get_book(int(data_row[2])),
            rating=int(data_row[5])
        )
        repo.add_review(review)


def populate(data_path: Path, repo: MemoryRepository):
    load_tags(data_path, repo)

    load_books_and_author(data_path, repo)

    users = load_users(data_path, repo)

    load_reviews(data_path, repo, users)


def get_book_by_id_and_given_list(list_book: List[Book], id: int):
    for book in list_book:
        if book.book_id == id:
            return book
    return None


def get_books_by_title_and_given_list(list_book: List[Book], title: str):
    matching_books = list()
    try:
        for book in list_book:
            if title in book.title:
                matching_books.append(book)
    except ValueError:
        pass
    return matching_books


def get_books_by_author_and_given_list(list_book: List[Book], author_input: str):
    matching_books = list()
    try:
        for book in list_book:
            for author in book.authors:
                if author_input in author.full_name:
                    matching_books.append(book)
    except ValueError:
        pass
    return matching_books


def get_books_by_year_and_given_list(list_book: List[Book], release_year: int):
    matching_books = list()
    try:
        for book in list_book:
            if book.release_year == release_year:
                matching_books.append(book)
    except ValueError:
        pass
    return matching_books



def write_user_to_csv(user_name, password):
    data_path = Path('library') / 'adapters' / 'data'
    users_filename = str(Path(data_path) / "users.csv")
    row_list = []
    for row in read_csv_file(users_filename):
        row_list = row

    read_csv_file(users_filename).close()

    last_id = int(row_list[0])
    with open(users_filename, 'a+', encoding='utf-8-sig', newline='') as infile:
        f_csv = csv.writer(infile)
        f_csv.writerow([last_id+1, user_name, password, ""])


