from flask import Blueprint, render_template, url_for, request, redirect

def form_book_list(target_page, books_list):
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
        prev_url = url_for('book_bp.books_list', page=target_page - 1)

    if target_page == book_page[-1][1]:
        next_url = None
    else:
        next_url = url_for('book_bp.books_list', page=target_page + 1)
    return books, pages, prev_url, next_url, target_page
