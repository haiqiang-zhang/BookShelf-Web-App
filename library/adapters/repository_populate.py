from pathlib import Path

from library.adapters.repository import AbstractRepository
from library.adapters.csv_data_importer import *


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    load_tags(data_path, repo)

    load_books_and_author(data_path, repo, database_mode)

    users = load_users(data_path, repo)

    load_reviews(data_path, repo, users)