import random

from library.adapters.repository import AbstractRepository
from library.domain.model import *


def get_rec_book(user: User):
    tag_list = user.tags
    books = []
    for tag in tag_list:
        for book in tag.tagged_books:
            if (book not in books) and (book not in user.favourite) and (book not in user.read_books):
                books.append(book)
    return books


def get_random_books(quantity, repo: AbstractRepository) -> List[Book]:
    book_count = repo.get_number_of_books()
    if book_count > 0:
        if quantity > book_count:
            quantity = book_count - 1
        random_ids = random.sample(range(0, book_count), quantity)
        books = repo.get_books_by_index(random_ids)
        return books



def get_random_books_by_given_list(book_list:List[Book]):
    if len(book_list) > 0:
        book_id = random.randint(0,len(book_list)-1)
        return book_list[book_id]
    return None



def print_tags(tags):
    tags_list = []
    for tag in tags:
        tags_list.append(tag.tag_name)
    return ", ".join(tags_list)