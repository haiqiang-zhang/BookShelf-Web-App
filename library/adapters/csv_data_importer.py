import csv
from pathlib import Path
from datetime import date, datetime

from werkzeug.security import generate_password_hash

from library.adapters.jsondatareader import BooksJSONReader
from library.adapters.repository import AbstractRepository
from library.domain.model import *



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



def load_books_and_author(data_path: Path, repo: AbstractRepository):
    book_path = str(Path(data_path) / "comic_books_excerpt.json")
    author_path = str(Path(data_path) / "book_authors_excerpt.json")
    JSONReader = BooksJSONReader(book_path, author_path)
    JSONReader.read_json_files(repo)
    for book in JSONReader.dataset_of_books:
        repo.add_book(book)

def load_tags(data_path: Path, repo: AbstractRepository):
    tag_path = str(Path(data_path) / "tags.csv")
    for data_row in read_csv_file(tag_path):
        tag = Tag(data_row[0])
        repo.add_tag(tag)


def load_users(data_path: Path, repo: AbstractRepository):
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


def load_reviews(data_path: Path, repo: AbstractRepository, users):
    review_filename = str(Path(data_path) / "reviews.csv")
    for data_row in read_csv_file(review_filename):
        review = make_review(
            review_text=data_row[3],
            user=users[data_row[1]],
            book=repo.get_book(int(data_row[2])),
            rating=int(data_row[5])
        )
        repo.add_review(review)

