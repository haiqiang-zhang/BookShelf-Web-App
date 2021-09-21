from typing import Iterable,List
import random

from library.adapters.repository import AbstractRepository
from library.domain.model import Book


def get_tag_names(repo: AbstractRepository):
    tags = repo.get_tags()
    tag_names = [tag.tag_name for tag in tags]

    return tag_names




# ============================================
# Functions to convert dicts to model entities
# ============================================

# def books_to_dict(book: Book):
#     book_dict = {
#         'year': book.release_year,
#         'title': book.title
#     }
#     return book_dict
#
#
# def books_to_dict(books: Iterable[Book]):
#     return [books_to_dict(book) for book in books]
