from flask import Blueprint, render_template, url_for, request, redirect

from library.adapters.repository import AbstractRepository
from library.domain.model import make_review, User
from library.adapters.memory_repository import count_fav_tag

class NonExistentArticleException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def form_book_list(target_page, books_list, url, tag_str = None):
    if not books_list or books_list is None:
        return [], [1], None, None, 1
    book_page = list()
    for index in range(len(books_list)):
        book_page.append((books_list[index], (index // 7) + 1))
    if target_page is None:
        target_page = 1
    target_page = int(target_page)
    books = []
    for index in range(len(book_page)):
        if book_page[index][1] == target_page:
            books.append(book_page[index][0])

    pages = [index for index in range(1, book_page[-1][1] + 1)]
    if target_page is None or target_page == 1:
        prev_url = None
    else:
        if tag_str is not None:
            prev_url = url_for(url, page=target_page - 1, tag=tag_str)
        else:
            prev_url = url_for(url, page=target_page - 1)
        # if list_title == "All Books": prev_url = url_for('book_bp.books_list', page=target_page - 1)
        # elif list_title == "Read Books": prev_url = url_for('book_bp.read_book', page=target_page - 1)
        # elif list_title == "Favourite Books": prev_url = url_for('book_bp.favourite_book', page=target_page - 1)
        # elif list_title == "Search Result": prev_url = url_for('search_bp.search_result', page=target_page - 1)

    if target_page == book_page[-1][1]:
        next_url = None
    else:
        if tag_str is not None:
            next_url = url_for(url, page=target_page + 1, tag=tag_str)
        else:
            next_url = url_for(url, page=target_page + 1)
        # if list_title == "All Books": next_url = url_for('book_bp.books_list', page=target_page + 1)
        # elif list_title == "Read Books": next_url = url_for('book_bp.read_book', page=target_page + 1)
        # elif list_title == "Favourite Books": next_url = url_for('book_bp.favourite_book', page=target_page + 1)
        # elif list_title == "Search Result": next_url = url_for('search_bp.search_result', page=target_page + 1)

    return books, pages, prev_url, next_url, target_page


def read_a_book_services(repo_instance, user_name, read_book_id):
    book_instance = repo_instance.get_book(int(read_book_id))
    user_instance = repo_instance.get_user(user_name)
    return book_instance, user_instance


def fav_a_book_services(repo_instance, user_name, fav_book_id):
    book_instance = repo_instance.get_book(int(fav_book_id))
    user_instance = repo_instance.get_user(user_name)
    return book_instance, user_instance


def add_review(book_id: int, review_text: str, user_name: str,rating , repo: AbstractRepository):
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentArticleException
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    review = make_review(review_text, user, book, rating)
    repo.add_review(review)


def get_review(book_id, repo_instance):
    book = get_book(int(book_id),repo_instance)

    review = book.reviews
    return review

def get_review_by_book(book):
    review = book.reviews
    return review



def get_book(book_id, repo_instance):
    book = repo_instance.get_book(int(book_id))
    if book is None:
        raise NonExistentArticleException
    return book


def auto_add_tag(user:User, repo_instance:AbstractRepository):
    tag_dict = count_fav_tag(user)
    for t_name in tag_dict:
        if tag_dict[t_name] >= 3:
            user.add_a_tag(repo_instance.get_tag(t_name))


def delete_fav_book_service(book_id:int, user_name:str, repo_instance:AbstractRepository):
    book = repo_instance.get_book(book_id)
    user = repo_instance.get_user(user_name)
    user.favourite.remove(book)


def delete_read_book_service(book_id:int, user_name:str, repo_instance:AbstractRepository):
    book = repo_instance.get_book(book_id)
    user = repo_instance.get_user(user_name)
    user.read_books.remove(book)



def get_tags(book, repo_instance):
    tags_list = []
    tags = repo_instance.get_tags()
    for tag in tags:
        if book in tag.tagged_books and tag.tag_name not in tags_list:
            tags_list.append(tag.tag_name)
    return tags_list


def get_rating(book):
    count = 0
    rating = 0
    for review in book.reviews:
        count += 1
        rating += review.get_rating
    if count == 0:
        return 0
    return round(rating / count, 2)

def get_rating_count(book):
    count = 0
    for review in book.reviews:
        count += 1
    return count