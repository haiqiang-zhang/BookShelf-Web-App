from flask import Blueprint, render_template, url_for, request, redirect, session
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
    session['search_field'] = "All Books"
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

@book_blueprint.route('/read_book')
def read_book():
    if 'user_name' in session:
        user = repo_instance.get_user(session['user_name'])
        books_list = repo_instance.get_user_read_book(user)
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

@book_blueprint.route('/favourite_book')
def favourite_book():
    if 'user_name' in session:
        user = repo_instance.get_user(session['user_name'])
        books_list = repo_instance.get_favourite(user)
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
        try:
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
        except ValueError:
            error = "Invalid Input!"
            return render_template('search.html', handler_url=url_for('book_bp.search'), error=error, form=form)
        except KeyError:
            error = "There are no search results!"
            return render_template('search.html', handler_url=url_for('book_bp.search'), error=error, form=form)
        target_page = request.args.get('page')
        books, pages, prev_url, next_url, target_page = form_book_list(target_page, books)
        return render_template('books_list.html', books=books, pages=pages, prev=prev_url, next=next_url, target_page=target_page)
    return render_template('search.html',
                           handler_url=url_for('book_bp.search'),
                           error=error,
                           form=form)

class SearchForm(FlaskForm):
    select = SelectField('Search mode', choices=["Book Name", "Book ID", "Author", "Release Year"])
    search_content = SearchField('Search Content')
    search_submit = SubmitField('')
