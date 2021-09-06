from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired
from library.adapters.repository import repo_instance
from library.adapters.repository import AbstractRepository

book_blueprint = Blueprint(
    'book_bp', __name__
)


# @book_blueprint.route('/')
# def home():
#     return render_template(
#         'home.html',
#         find_person_url=url_for('people_bp.find_person'),
#         list_people_url=url_for('people_bp.list_people')
#     )


@book_blueprint.route('/books_list')
def books_list():
    book_page = list()
    for index in range(len(repo_instance.get_all_books())):
        book_page.append((repo_instance.get_all_books()[index], (index // 7) + 1))
    target_page = request.args.get('page')
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


    return render_template(
        'books_list.html',
        books=books,
        pages=pages,
        prev=prev_url,
        next=next_url,
        target_page=target_page
    )
