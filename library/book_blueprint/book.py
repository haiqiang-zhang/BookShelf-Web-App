from flask import Blueprint, render_template, url_for, request, redirect
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms import IntegerField, SubmitField
from wtforms.fields.html5 import SearchField
from wtforms.validators import DataRequired
from library.adapters.repository import repo_instance
from library.adapters.repository import AbstractRepository
from library.book_blueprint.services import form_book_list

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
    books_list = repo_instance.get_all_books()
    target_page = request.args.get('page')
    books, pages, prev_url, next_url, target_page = form_book_list(target_page, books_list)

    return render_template(
        'books_list.html',
        books=books,
        pages=pages,
        prev=prev_url,
        next=next_url,
        target_page=target_page
    )


@book_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    error = None
    if form.validate_on_submit():
        search_content = form.search_content.data
        select_items = form.select.data
        books = []
        if select_items == "Book ID":
            try:
                book = repo_instance.get_book(int(search_content))
                if book is None:
                    raise KeyError
                books.append(book)
            except ValueError:
                error = "Invalid Input!"
                return render_template('search.html',
                                       handler_url=url_for('book_bp.search'),
                                       error=error,
                                       form=form)
            except KeyError:
                error = "There are no search results!"
                return render_template('search.html',
                                       handler_url=url_for('book_bp.search'),
                                       error=error,
                                       form=form)

            target_page = request.args.get('page')
            books, pages, prev_url, next_url, target_page = form_book_list(target_page, books)
            return render_template(
                'books_list.html',
                books=books,
                pages=pages,
                prev=prev_url,
                next=next_url,
                target_page=target_page
            )

    return render_template('search.html',
                           handler_url=url_for('book_bp.search'),
                           error=error,
                           form=form)


class SearchForm(FlaskForm):
    select = SelectField('Search mode', choices=["Book Name", "Book ID", "Author", "Release Year"])
    search_content = SearchField('Search Content')
    search_submit = SubmitField('')
