from flask import Blueprint, render_template, url_for, request, redirect, session

from library.adapters.repository import AbstractRepository
from library.adapters.memory_repository import get_book_by_id_and_given_list, get_books_by_title_and_given_list,get_books_by_author_and_given_list,get_books_by_year_and_given_list

def get_search_books(request_search_scope:str, repo_instance:AbstractRepository):

    if "/books_list" in request_search_scope:
        list_book = "books_list"
        scope_text = "All Books"
    elif "/read_book" in request_search_scope:
        user_name = session["user_name"]
        list_book = repo_instance.get_user(user_name).read_books
        scope_text = "Read Books"
    elif "/favourite_book" in request_search_scope:
        user_name = session["user_name"]
        list_book = repo_instance.get_user(user_name).favourite
        scope_text = "Favourite Books"
    else:
        list_book = "books_list"
        scope_text = "All Books"
    return list_book, scope_text

def search_book(repo_instance:AbstractRepository, select_items, search_content, list_book):
    books = []
    if list_book == "books_list":
        if select_items == "Book ID":
            book = repo_instance.get_book(int(search_content))
            if book is None:
                raise KeyError
            books.append(book)
        elif select_items == "Book Name":
            books = repo_instance.get_books_by_title(search_content)
            if not books:
                raise KeyError
        elif select_items == "Author":
            books = repo_instance.get_books_by_authors(search_content)
            if not books:
                raise KeyError
        else:
            books = repo_instance.get_books_by_release_year(int(search_content))
            if not books:
                raise KeyError

    else:
        if select_items == "Book ID":
            book = get_book_by_id_and_given_list(list_book, int(select_items))
            if book is None:
                raise KeyError
            books.append(book)
        elif select_items == "Book Name":
            books = get_books_by_title_and_given_list(list_book, select_items)
            if not books:
                raise KeyError
        elif select_items == "Author":
            books = get_books_by_author_and_given_list(list_book, select_items)
            if not books:
                raise KeyError
        else:
            books = get_books_by_year_and_given_list(list_book,int(select_items))
            if not books:
                raise KeyError
    return books



